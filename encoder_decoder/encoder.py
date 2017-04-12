"""A set of encoder modules used in the encoder-decoder framework."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import math
import numpy as np
import tensorflow as tf

from encoder_decoder import graph_utils, rnn


class Encoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(Encoder, self).__init__(hyperparameters)

        # variable reuse
        self.char_embedding_vars = False
        self.token_embedding_vars = False
        self.char_rnn_vars = False

        self.input_keep = input_keep
        self.output_keep = output_keep

        self.channels = []
        self.dim = 0
        if self.sc_token:
            self.channels.append('token')
            self.dim += self.sc_token_dim
        if self.sc_char:
            self.channels.append('char')
            self.dim += self.sc_char_dim

        assert(len(self.channels) > 0)

    def token_representations(self, channel_inputs):
        """
        Generate token representations based on multi-channel input.

        :param channel_inputs: an array of channel input indices
            1. batch token indices
            2. batch char indices
        """
        channel_embeddings = []
        if self.sc_token:
            token_channel_embeddings = [tf.nn.embedding_lookup(
                                        self.token_embeddings(), encoder_input[0])
                                        for encoder_input in channel_inputs[0]]
            channel_embeddings.append(token_channel_embeddings)
        if self.sc_char:
            char_channel_embeddings = \
                self.char_channel_embeddings(channel_inputs[1])
            channel_embeddings.append(char_channel_embeddings)
        if len(channel_embeddings) == 1:
            input_embeddings = channel_embeddings[0]
        else:
            input_embeddings = [tf.concat(0, [x, y])
                                for x, y in zip(channel_embeddings)]
        return input_embeddings

    def token_embeddings(self):
        """
        Generate token representations by plain table look-up

        :return: token embedding matrix [source_vocab_size, dim]
        """
        with tf.variable_scope("encoder_token_embeddings",
                               reuse=self.token_embedding_vars):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding",
                [self.source_vocab_size, self.sc_token_dim],
                initializer=initializer)
            self.token_embedding_vars = True
            return embeddings

    def char_embeddings(self):
        with tf.variable_scope("encoder_char_embeddings",
                               reuse=self.char_embedding_vars):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding", [self.source_vocab_size,
                                                       self.sc_char_dim],
                                         initializer=initializer)
            self.char_embedding_vars = True
            return embeddings

    def token_channel_embeddings(self):
        input = self.token_unk_free_index()
        return tf.nn.embedding_lookup(self.token_embeddings(), input)

    def char_channel_embeddings(self, channel_inputs):
        """
        Generate token representations by character composition.

        :param channel_inputs: batch input char indices
                [[batch, token_size], [batch, token_size], ...]
        :return: embeddings_char [source_vocab_size, char_channel_dim]
        """
        inputs = tf.split(1, self.max_source_token_size,
                          tf.concat(0, channel_inputs))
        embeddings = self.char_embeddings()
        input_embeddings = [embeddings[input] for input in inputs]
        if self.sc_char_composition == 'rnn':
            with tf.variable_scope("encoder_char_rnn",
                                   reuse=self.char_rnn_vars) as scope:
                cell = graph_utils.create_multilayer_cell(
                    self.sc_char_rnn_cell, scope, self.sc_char_dim,
                    self.sc_char_rnn_num_layers)
                rnn_outputs, rnn_states = rnn.RNNModel(cell, input_embeddings,
                    num_cell_layers=self.sc_char_rnn_num_layers, dtype=tf.float32)
                self.char_rnn_vars = True
        else:
            raise NotImplementedError
        return rnn_states[-1]

    def token_unk_free_index(self):
        return np.load(self.sc_token_features_path)

    def token_char_index_matrix(self):
        return np.load(self.sc_char_features_path)


class RNNEncoder(Encoder):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(RNNEncoder, self).__init__(hyperparameters,
                                         input_keep, output_keep)
        self.cell = self.encoder_cell()
        self.output_dim = self.dim

    def define_graph(self, encoder_inputs):
        # Compute the continuous input representations
        input_embeddings = self.token_representations(encoder_inputs)
        with tf.variable_scope("encoder_rnn"):
            encoder_outputs, encoder_states = \
                rnn.RNNModel(self.cell, input_embeddings,
                             num_cell_layers=self.num_layers, dtype=tf.float32)
        encoder_state = encoder_states[-1]
        return encoder_outputs, encoder_state

    def encoder_cell(self):
        """RNN cell for the encoder."""
        with tf.variable_scope("encoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep)
        return cell


class BiRNNEncoder(Encoder):
    def __init__(self, hyperparameters, input_keep, output_keep):
        super(BiRNNEncoder, self).__init__(hyperparameters,
                                           input_keep, output_keep)
        self.fw_cell = self.forward_cell()
        self.bw_cell = self.backward_cell()
        self.output_dim = 2 * self.dim
        print("encoder input dimension = {}".format(self.dim))
        print("encoder output dimension = {}".format(self.output_dim))

    def define_graph(self, encoder_inputs):
        # Each rnn in the bi-directional encoder have dimension which is half
        # of that of the decoder.
        # The hidden states of the two rnns are concatenated as the hidden
        # states of the bi-directional encoder.

        # Compute the continuous input representations
        input_embeddings = self.token_representations(encoder_inputs)
        outputs, states_fw, states_bw = rnn.BiRNNModel(
            self.fw_cell, self.bw_cell, input_embeddings,
            num_cell_layers=self.num_layers, dtype=tf.float32)
        if self.rnn_cell == "gru":
            if self.num_layers > 1:
                states = []
                for i in xrange(self.num_layers):
                    states.append(tf.concat(1, [states_fw[-1][i], states_bw[0][i]]))
                state = tf.concat(1, states)
            else:
                state = tf.concat(1, [states_fw[-1], states_bw[0]])
        elif self.rnn_cell == "lstm":
            raise NotImplementedError
        else:
            raise AttributeError("Unrecognized RNN cell type.")
        return outputs, state

    def forward_cell(self):
        """RNN cell for the forward RNN."""
        with tf.variable_scope("forward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep)
        return cell

    def backward_cell(self):
        """RNN cell for the backward RNN."""
        with tf.variable_scope("backward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope,
                self.dim, self.num_layers, self.input_keep, self.output_keep)
        return cell
