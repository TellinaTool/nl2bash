"""Sequence-to-sequence model with an attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys

from encoder_decoder.framework import EncoderDecoderModel
from encoder_decoder import encoder
try:
    from . import rnn_decoder
except ImportError:
    from seq2seq import rnn_decoder


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

    def __init__(self, hyperparams, buckets=None, forward_only=False):
        super(Seq2SeqModel, self).__init__(hyperparams, buckets, forward_only)


    def define_encoder(self):
        """Construct sequence encoders."""
        if self.encoder_topology == "rnn":
            self.encoder = encoder.RNNEncoder(self.hyperparams)
        elif self.encoder_topology == "birnn":
            self.encoder = encoder.BiRNNEncoder(self.hyperparams)
        else:
            raise ValueError("Unrecognized encoder type.")


    def define_decoder(self):
        """Construct sequence decoders."""
        if self.decoder_topology == "rnn":
            self.decoder = rnn_decoder.RNNDecoder(self.hyperparams,
                                                  self.output_projection())
        else:
            raise ValueError("Unrecognized decoder topology: {}."
                             .format(self.decoder_topology))
