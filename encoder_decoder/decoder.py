from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import math
import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import data_utils, graph_utils, beam_search

class Decoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, dim, scope):
        """
        :param hyperparameters: Tellina model hyperparameters.
        :param dim: Decoder embedding dimension.
        :param scope: Scope of the decoder. (There might be multiple decoders
            with the same construction in the neural architecture.)
        """
        super(Decoder, self).__init__(hyperparameters)

        self.dim = dim
        self.scope = scope

        # variable sharing
        self.char_embedding_vars = False
        self.token_embedding_vars = False
        self.token_output_projection_vars = False

        self.beam_decoder = beam_search.BeamDecoder(
            self.target_vocab_size,
            data_utils.ROOT_ID, data_utils.EOS_ID,
            self.batch_size,
            self.beam_size,
            self.use_attention,
            self.alpha,
            locally_normalized=(
                self.training_algorithm != "bso"
        )) if self.decoding_algorithm == "beam_search" else None

        self.token_output_projection = self.token_output_projection()

    def char_embeddings(self):
        with tf.variable_scope(self.scope + "_char_embeddings",
                               reuse=self.char_embedding_vars):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding",
                [self.target_vocab_size, self.dim], initializer=initializer)
            self.char_embedding_vars = True
            return embeddings

    def token_embeddings(self):
        with tf.variable_scope(self.scope + "_token_embeddings",
                               reuse=self.token_embedding_vars):
            sqrt3 = math.sqrt(3)
            initializer = tf.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding",
                [self.target_vocab_size, self.dim], initializer=initializer)
            self.token_embedding_vars = True
            return embeddings

    def token_output_projection(self):
        with tf.variable_scope(self.scope + "_token_output_projection",
                               reuse=self.token_output_projection_vars):
            w = tf.get_variable("proj_w", [self.dim, self.target_vocab_size])
            b = tf.get_variable("proj_b", [self.target_vocab_size])
            self.token_output_projection_vars = True
        return (w, b)


class AttentionCellWrapper(tf.nn.rnn_cell.RNNCell):

    def __init__(self, cell, attention_states, encoder_attn_masks,
                 attention_input_keep, attention_output_keep, num_heads,
                 rnn_cell, num_layers):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param attention_input_keep: attention input state dropout
        :param attention_output_keep: attention hidden state dropout
        :param num_heads: Number of attention heads that read from from attention_states.
                          Dummy field if attention_states is None.
        :param rnn_cell: Type of rnn cells used.
        :param num_layers: Number of layers in the RNN cells.
        """
        attention_states = tf.nn.dropout(attention_states, attention_input_keep)
        attn_length = attention_states.get_shape()[1].value
        attn_vec_dim = attention_states.get_shape()[2].value
        attn_dim = attn_vec_dim 

        # To calculate W1 * h_t we use a 1-by-1 convolution
        hidden = tf.reshape(attention_states, [-1, attn_length, 1, attn_vec_dim])
        hidden_features = []
        v = []
        with tf.variable_scope("attention_cell_wrapper"):
            for a in xrange(num_heads):
                # k = tf.get_variable("AttnW_%d" % a, [1, 1, attn_vec_dim, attn_dim])
                # hidden_features.append(tf.nn.conv2d(hidden, k, [1,1,1,1], "SAME"))
                hidden_features.append(hidden)
                v.append(tf.get_variable("AttnV_%d" % a, [attn_vec_dim]))

        self.cell = cell
        self.encoder_attn_masks = encoder_attn_masks
        self.rnn_cell = rnn_cell
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.attn_vec_dim = attn_vec_dim
        self.attn_length = attn_length
        self.attn_dim = attn_dim
        self.attention_input_keep = attention_input_keep
        self.attention_output_keep = attention_output_keep
        self.hidden = hidden
        self.hidden_features = hidden_features
        self.v = v

    def attention(self, state):
        """Put attention masks on hidden using hidden_features and query."""
        ds = []  # Results of attention reads will be stored here.
        if nest.is_sequence(state):  # If the query is a tuple, flatten it.
            # query_list = nest.flatten(state)
            # for q in query_list:  # Check that ndims == 2 if specified.
            #   ndims = q.get_shape().ndims
            #   if ndims:
            #     assert ndims == 2
            # state = tf.concat(1, query_list)
            state = state[1]
        for a in xrange(self.num_heads):
            with tf.variable_scope("Attention_%d" % a):
                y = tf.reshape(state, [-1, 1, 1, self.attn_vec_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                # s = tf.reduce_sum(
                #     v[a] * tf.tanh(hidden_features[a] + y), [2, 3])
                # s = tf.reduce_sum(
                #     self.v[a] * tf.mul(self.hidden_features[a], y), [2, 3])
                s = tf.reduce_sum(tf.mul(self.hidden_features[a], y), [2, 3])
                s = s - (1 - self.encoder_attn_masks) * 1e12
                attn_alignment = tf.nn.softmax(s)
                # Now calculate the attention-weighted vector d.
                d = tf.reduce_sum(tf.reshape(attn_alignment, [-1, self.attn_length, 1, 1])
                                  * self.hidden_features[a], [1, 2])
                ds.append(tf.reshape(d, [-1, self.attn_dim]))
        attns = tf.concat(1, ds)
        attns.set_shape([None, self.num_heads * self.attn_dim])
        self.attention_vars = True
        return attns, attn_alignment

    def __call__(self, input_embedding, state, attn_alignments, scope=None):
        if nest.is_sequence(state):
            dim = state[1].get_shape()[1].value
        else:
            dim = state.get_shape()[1].value
        if self.num_layers > 1:
            dim /= self.num_layers

        with tf.variable_scope("AttnInputProjection"):
            _, state = self.cell(input_embedding, state, scope)
            # If multi-layer RNN cell is used, apply attention to the top layer.
            if self.num_layers > 1:
                if self.rnn_cell == 'gru':
                    top_state = tf.split(1, self.num_layers, state)[-1]
                elif self.rnn_cell == 'lstm':
                    raise NotImplementedError
                else:
                    raise AttributeError("Unrecognized RNN cell type.")
            else:
                top_state = state
            attns, attn_alignment = self.attention(top_state)

        with tf.variable_scope("AttnStateProjection"):
            attn_state = tf.tanh(tf.nn.rnn_cell._linear(
                [top_state, attns], dim, True))

        with tf.variable_scope("AttnOutputProjection"):
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear(
              tf.nn.dropout(attn_state, self.attention_output_keep), dim, True)

        self.attention_cell_vars = True
        attn_alignments.append(tf.expand_dims(attn_alignment, 1))
        return output, state, attn_alignments
