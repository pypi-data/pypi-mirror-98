"""Lemmatizer models."""
from typing import Optional, Dict, List, Union

import torch
import torch.nn as nn
from allennlp import data, nn as allen_nn, modules
from allennlp.common import checks

from unidic_combo.models import base, dilated_cnn, utils


@base.Predictor.register("combo_lemma_predictor_from_vocab", constructor="from_vocab")
class LemmatizerModel(base.Predictor):
    """Lemmatizer model."""

    def __init__(self,
                 num_embeddings: int,
                 embedding_dim: int,
                 dilated_cnn_encoder: dilated_cnn.DilatedCnnEncoder,
                 input_projection_layer: base.Linear):
        super().__init__()
        self.char_embed = nn.Embedding(
            num_embeddings=num_embeddings,
            embedding_dim=embedding_dim,
        )
        self.dilated_cnn_encoder = modules.TimeDistributed(dilated_cnn_encoder)
        self.input_projection_layer = input_projection_layer

    def forward(self,
                x: Union[torch.Tensor, List[torch.Tensor]],
                mask: Optional[torch.BoolTensor] = None,
                labels: Optional[Union[torch.Tensor, List[torch.Tensor]]] = None,
                sample_weights: Optional[Union[torch.Tensor, List[torch.Tensor]]] = None) -> Dict[str, torch.Tensor]:
        encoder_emb, chars = x

        encoder_emb = self.input_projection_layer(encoder_emb)
        char_embeddings = self.char_embed(chars)

        BATCH_SIZE, _, MAX_WORD_LENGTH, CHAR_EMB = char_embeddings.size()
        encoder_emb = encoder_emb.unsqueeze(2).repeat(1, 1, MAX_WORD_LENGTH, 1)

        x = torch.cat((char_embeddings, encoder_emb), dim=-1).transpose(2, 3)
        x = self.dilated_cnn_encoder(x).transpose(2, 3)
        output = {
            "prediction": x.argmax(-1),
            "probability": x
        }

        if labels is not None:
            if mask is None:
                mask = encoder_emb.new_ones(encoder_emb.size()[:-2])
            if sample_weights is None:
                sample_weights = labels.new_ones(BATCH_SIZE)
            mask = mask.unsqueeze(2).repeat(1, 1, MAX_WORD_LENGTH).bool()
            output["loss"] = self._loss(x, labels, mask, sample_weights)

        return output

    @staticmethod
    def _loss(pred: torch.Tensor, true: torch.Tensor, mask: torch.BoolTensor,
              sample_weights: torch.Tensor) -> torch.Tensor:
        BATCH_SIZE, SENTENCE_LENGTH, MAX_WORD_LENGTH, CHAR_CLASSES = pred.size()
        pred = pred.reshape(-1, CHAR_CLASSES)

        true = true.reshape(-1)
        mask = true.gt(0)
        loss = utils.masked_cross_entropy(pred, true, mask)
        loss = loss.reshape(BATCH_SIZE, -1) * sample_weights.unsqueeze(-1)
        valid_positions = mask.sum()
        return loss.sum() / valid_positions

    @classmethod
    def from_vocab(cls,
                   vocab: data.Vocabulary,
                   char_vocab_namespace: str,
                   lemma_vocab_namespace: str,
                   embedding_dim: int,
                   input_projection_layer: base.Linear,
                   filters: List[int],
                   kernel_size: List[int],
                   stride: List[int],
                   padding: List[int],
                   dilation: List[int],
                   activations: List[allen_nn.Activation],
                   ):
        assert char_vocab_namespace in vocab.get_namespaces()
        assert lemma_vocab_namespace in vocab.get_namespaces()

        if len(filters) + 1 != len(kernel_size):
            raise checks.ConfigurationError(
                f"len(filters) ({len(filters):d}) + 1 != kernel_size ({len(kernel_size):d})"
            )
        filters = filters + [vocab.get_vocab_size(lemma_vocab_namespace)]

        dilated_cnn_encoder = dilated_cnn.DilatedCnnEncoder(
            input_dim=embedding_dim + input_projection_layer.get_output_dim(),
            filters=filters,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            activations=activations,
        )
        return cls(num_embeddings=vocab.get_vocab_size(char_vocab_namespace),
                   embedding_dim=embedding_dim,
                   dilated_cnn_encoder=dilated_cnn_encoder,
                   input_projection_layer=input_projection_layer)
