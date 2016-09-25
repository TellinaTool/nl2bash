"""Sequence-to-tree model with an attention mechanism."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import tensorflow as tf

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from encoder_decoder import EncoderDecoderModel
import encoder
import decoder


class Seq2TreeModel(EncoderDecoderModel):
    """Sequence-to-tree models.
    """
    def __init__(self, hyperparams, buckets=None, forward_only=False):
        """
        Create the model.
        :param hyperparams: learning hyperparameters
        :param buckets: if not None, train bucket model.
        :param forward_only: if set, we do not construct the backward pass.
        """
        super(Seq2TreeModel, self).__init__(hyperparams, buckets, forward_only)

        self.global_epoch = tf.Variable(0, trainable=False)

        self.define_graph(forward_only)


    def define_encoder(self):
        """Construct sequence encoders."""
        if self.encoder_topology == "rnn":
            self.encoder = encoder.RNNEncoder(self.dim, self.rnn_cell, self.num_layers,
                                              self.encoder_input_keep, self.encoder_output_keep)
        elif self.encoder_topology == "birnn":
            self.encoder = encoder.BiRNNEncoder(self.dim, self.rnn_cell, self.num_layers)
        else:
            raise ValueError("Unrecognized encoder type.")


    def define_decoder(self):
        """Construct tree decoders."""
        if self.decoder_topology == "basic_tree":
            self.decoder = decoder.BasicTreeDecoder(self.dim, self.batch_size, self.rnn_cell, self.num_layers,
                                                    self.decoder_input_keep, self.decoder_output_keep,
                                                    self.use_attention, self.use_copy,
                                                    self.output_projection())
        else:
            raise ValueError("Unrecognized decoder topology: {}."
                             .format(self.decoder_topology))
