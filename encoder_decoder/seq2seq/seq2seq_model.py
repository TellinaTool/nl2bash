"""Sequence-to-sequence model with an attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from encoder_decoder import encoder
from encoder_decoder.framework import EncoderDecoderModel
from . import rnn_decoder


class Seq2SeqModel(EncoderDecoderModel):
    """Sequence-to-sequence model with attention and for multiple buckets.

    This class implements a multi-layer recurrent neural network as encoder,
    and an attention-based decoder. This is the same as the model described in
    this paper: http://arxiv.org/abs/1412.7449 - please look there for details,
    or into the seq2seq library for complete model implementation.
    This class also allows to use GRU cells in addition to LSTM cells, and
    sampled softmax to handle large output vocabulary size. A single-layer
    version of this model, but with bi-directional encoder, was presented in
      http://arxiv.org/abs/1409.0473
    and sampled softmax is described in Section 3 of the following paper.
      http://arxiv.org/abs/1412.2007
    """

    def __init__(self, hyperparams, buckets=None):
        super(Seq2SeqModel, self).__init__(hyperparams, buckets)


    def define_encoder(self, input_keep, output_keep):
        """
        Construct sequence encoder.
        """
        if self.encoder_topology == "rnn":
            self.encoder = encoder.RNNEncoder(
                self.hyperparams, input_keep, output_keep)
        elif self.encoder_topology == "birnn":
            self.encoder = encoder.BiRNNEncoder(
                self.hyperparams, input_keep, output_keep)
        else:
            raise ValueError("Unrecognized encoder type.")


    def define_decoder(self, dim, embedding_dim, use_attention,
            attention_function, input_keep, output_keep):
        """
        Construct sequence decoder.
        """
        if self.decoder_topology == "rnn":
            self.decoder = rnn_decoder.RNNDecoder(
                hyperparameters=self.hyperparams,
                scope='token_decoder', dim=dim,
                embedding_dim=embedding_dim,
                use_attention=use_attention,
                attention_function=attention_function,
                input_keep=input_keep,
                output_keep=output_keep,
                decoding_algorithm=self.token_decoding_algorithm
            )
        else:
            raise ValueError("Unrecognized decoder topology: {}.".format(
                self.decoder_topology))
