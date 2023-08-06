"""Embeddings."""
from typing import Optional, Dict, Any

import torch
import torch.nn as nn
from allennlp import nn as allen_nn, data, modules
from allennlp.modules import token_embedders
from allennlp.nn import util
from overrides import overrides

from unidic_combo.models import base, dilated_cnn


@token_embedders.TokenEmbedder.register("char_embeddings")
@token_embedders.TokenEmbedder.register("char_embeddings_from_config", constructor="from_config")
class CharacterBasedWordEmbeddings(token_embedders.TokenEmbedder):
    """Character-based word embeddings."""

    def __init__(self,
                 num_embeddings: int,
                 embedding_dim: int,
                 dilated_cnn_encoder: dilated_cnn.DilatedCnnEncoder):
        super().__init__()
        self.char_embed = nn.Embedding(
            num_embeddings=num_embeddings,
            embedding_dim=embedding_dim,
        )
        self.dilated_cnn_encoder = modules.TimeDistributed(dilated_cnn_encoder)
        self.output_dim = embedding_dim

    def forward(self,
                x: torch.Tensor,
                char_mask: Optional[torch.BoolTensor] = None) -> torch.Tensor:
        if char_mask is None:
            char_mask = x.new_ones(x.size())

        x = self.char_embed(x)
        x = x * char_mask.unsqueeze(-1).float()
        x = self.dilated_cnn_encoder(x.transpose(2, 3))
        return torch.max(x, dim=-1)[0]

    @overrides
    def get_output_dim(self) -> int:
        return self.output_dim

    @classmethod
    def from_config(cls,
                    embedding_dim: int,
                    vocab: data.Vocabulary,
                    dilated_cnn_encoder: dilated_cnn.DilatedCnnEncoder,
                    vocab_namespace: str = "token_characters"):
        assert vocab_namespace in vocab.get_namespaces()
        return cls(
            embedding_dim=embedding_dim,
            num_embeddings=vocab.get_vocab_size(vocab_namespace),
            dilated_cnn_encoder=dilated_cnn_encoder
        )


@token_embedders.TokenEmbedder.register("embeddings_projected")
class ProjectedWordEmbedder(token_embedders.Embedding):
    """Word embeddings."""

    def __init__(self,
                 embedding_dim: int,
                 num_embeddings: int = None,
                 weight: torch.FloatTensor = None,
                 padding_index: int = None,
                 trainable: bool = True,
                 max_norm: float = None,
                 norm_type: float = 2.0,
                 scale_grad_by_freq: bool = False,
                 sparse: bool = False,
                 vocab_namespace: str = "tokens",
                 pretrained_file: str = None,
                 vocab: data.Vocabulary = None,
                 projection_layer: Optional[base.Linear] = None):
        super().__init__(
            embedding_dim=embedding_dim,
            num_embeddings=num_embeddings,
            weight=weight,
            padding_index=padding_index,
            trainable=trainable,
            max_norm=max_norm,
            norm_type=norm_type,
            scale_grad_by_freq=scale_grad_by_freq,
            sparse=sparse,
            vocab_namespace=vocab_namespace,
            pretrained_file=pretrained_file,
            vocab=vocab
        )
        self._projection = projection_layer
        self.output_dim = embedding_dim if projection_layer is None else projection_layer.out_features

    @overrides
    def get_output_dim(self) -> int:
        return self.output_dim


@token_embedders.TokenEmbedder.register("transformers_word_embeddings")
class TransformersWordEmbedder(token_embedders.PretrainedTransformerMismatchedEmbedder):
    """
    Transformers word embeddings as last hidden state + optional projection layers.

    Tested with Bert (but should work for other models as well).
    """

    def __init__(self,
                 model_name: str,
                 projection_dim: int = 0,
                 projection_activation: Optional[allen_nn.Activation] = lambda x: x,
                 projection_dropout_rate: Optional[float] = 0.0,
                 freeze_transformer: bool = True,
                 tokenizer_kwargs: Optional[Dict[str, Any]] = None,
                 transformer_kwargs: Optional[Dict[str, Any]] = None):
        super().__init__(model_name,
                         train_parameters=not freeze_transformer,
                         tokenizer_kwargs=tokenizer_kwargs,
                         transformer_kwargs=transformer_kwargs)
        if projection_dim:
            self.projection_layer = base.Linear(in_features=super().get_output_dim(),
                                                out_features=projection_dim,
                                                dropout_rate=projection_dropout_rate,
                                                activation=projection_activation)
            self.output_dim = projection_dim
        else:
            self.projection_layer = None
            self.output_dim = super().get_output_dim()

    @overrides
    def forward(
            self,
            token_ids: torch.LongTensor,
            mask: torch.BoolTensor,
            offsets: torch.LongTensor,
            wordpiece_mask: torch.BoolTensor,
            type_ids: Optional[torch.LongTensor] = None,
            segment_concat_mask: Optional[torch.BoolTensor] = None,
    ) -> torch.Tensor:  # type: ignore
        x = super().forward(token_ids, mask, offsets, wordpiece_mask, type_ids, segment_concat_mask)
        if self.projection_layer:
            x = self.projection_layer(x)
        return x

    @overrides
    def get_output_dim(self):
        return self.output_dim


@token_embedders.TokenEmbedder.register("feats_embedding")
class FeatsTokenEmbedder(token_embedders.Embedding):

    def __init__(self,
                 embedding_dim: int,
                 num_embeddings: int = None,
                 weight: torch.FloatTensor = None,
                 padding_index: int = None,
                 trainable: bool = True,
                 max_norm: float = None,
                 norm_type: float = 2.0,
                 scale_grad_by_freq: bool = False,
                 sparse: bool = False,
                 vocab_namespace: str = "feats",
                 pretrained_file: str = None,
                 vocab: data.Vocabulary = None):
        super().__init__(
            embedding_dim=embedding_dim,
            num_embeddings=num_embeddings,
            weight=weight,
            padding_index=padding_index,
            trainable=trainable,
            max_norm=max_norm,
            norm_type=norm_type,
            scale_grad_by_freq=scale_grad_by_freq,
            sparse=sparse,
            vocab_namespace=vocab_namespace,
            pretrained_file=pretrained_file,
            vocab=vocab
        )

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        # (batch_size, sentence_length, features_vocab_length)
        mask = tokens.gt(0)
        # (batch_size, sentence_length, features_vocab_length, embedding_dim)
        x = super().forward(tokens)
        # (batch_size, sentence_length, embedding_dim)
        return x.sum(dim=-2) / (
            (mask.sum(dim=-1) + util.tiny_value_of_dtype(torch.float)).unsqueeze(dim=-1)
        )
