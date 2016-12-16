"""A set of encoder modules used in the encoder-decoder framework."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import graph_utils


class Encoder(graph_utils.NNModel):
    def __init__(self, hyperparameters):
        super(Encoder, self).__init__(hyperparameters)


class RNNEncoder(Encoder):
    def __init__(self, hyperparameters):
        super(RNNEncoder, self).__init__(hyperparameters)
        self.cell, _ = self.encoder_cell()

        # variable sharing
        self.encoder_rnn_vars = False

    def define_graph(self, encoder_inputs, embeddings):
        self.embeddings = embeddings
        input_embeddings = [tf.nn.embedding_lookup(self.embeddings, encoder_input)
                            for encoder_input in encoder_inputs]
        with tf.variable_scope("encoder_rnn"):
            if self.encoder_rnn_vars:
                tf.get_variable_scope().reuse_variables()
            encoder_outputs, encoder_state = \
                tf.nn.rnn(self.cell, input_embeddings, dtype=tf.float32)
            self.encoder_rnn_vars = True
        return encoder_outputs, encoder_state

    def encoder_cell(self):
        """RNN cell for the encoder."""
        with tf.variable_scope("encoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                                                      self.dim, self.num_layers)
            self.encoder_cell_vars = True
        return cell, scope


class BiRNNEncoder(Encoder):
    def __init__(self, hyperparameters):
        super(BiRNNEncoder, self).__init__(hyperparameters)
        self.fw_cell, _ = self.forward_cell()
        self.bw_cell, _ = self.backward_cell()

        # variable sharing
        self.forward_rnn_vars = False
        self.backward_rnn_vars = False

    def define_graph(self, encoder_inputs, embeddings):
        self.embeddings = embeddings
        input_embeddings = [tf.nn.embedding_lookup(self.embeddings, encoder_input)
                            for encoder_input in encoder_inputs]
        outputs, state_fw, state_bw = tf.rnn.bidirectional_rnn(self.fw_cell,
                                                               self.bw_cell,
                                                               input_embeddings)
        if self.rnn_cell == "gru":
            state = outputs[-1]
        elif self.rnn_cell == "lstm":
            raise NotImplementedError
        else:
            raise AttributeError("Unrecognized RNN cell type.")

        return outputs, state

    # Each rnn in the bi-directional encoder have dimension which is half of the decoder
    # the hidden states of the two rnns are concatenated as the hidden states of
    # the bi-directional encoder
    def forward_cell(self):
        """RNN cell for the forward RNN."""
        with tf.variable_scope("forward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                                                      self.dim/2, self.num_layers,
                                                      self.encoder_input_keep,
                                                      self.encoder_output_keep)
        return cell, scope


    def backward_cell(self):
        """RNN cell for the backward RNN."""
        with tf.variable_scope("backward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                                                      self.dim/2, self.num_layers,
                                                      self.encoder_input_keep,
                                                      self.encoder_output_keep)
        return cell, scope


    @graph_utils.deprecated
    def output_projection(self):
        with tf.variable_scope("birnn_output_projection"):
            w = tf.get_variable("proj_w", [self.dim * 2, self.dim])
            b = tf.get_variable("proj_b", [self.dim])
        return (w, b)
