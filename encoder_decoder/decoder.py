from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import math
import numpy as np
import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import data_utils, graph_utils, beam_search

class Decoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, scope, vocab_size, dim, use_attention,
        attention_function, input_keep, output_keep, decoding_algorithm,
        use_token_features=False):
        """
        :param hyperparameters: Tellina model hyperparameters.
        :param scope: Scope of the decoder. (There might be multiple decoders
            with the same construction in the neural architecture.)
        :param vocab_size: Output vocabulary size.
        :param dim: Decoder Embedding dimension.
        :param use_attention: Set to True to use attention for decoding.
        :param attention_function: The attention function used.
        :param input_keep: Dropout parameter for the input of the attention layer.
        :param output_keep: Dropout parameter for the output of the attention layer.
        :param decoding_algorithm
        """
        super(Decoder, self).__init__(hyperparameters)

        self.scope = scope
        self.vocab_size = vocab_size
        self.dim = dim
        self.use_attention = use_attention
        self.attention_function = attention_function
        self.input_keep = input_keep
        self.output_keep = output_keep
        self.decoding_algorithm = decoding_algorithm
        self.use_token_features = use_token_features

        # variable sharing
        self.embedding_vars = False
        self.output_project_vars = False

        self.beam_decoder = beam_search.BeamDecoder(
            self.vocab_size,
            data_utils.ROOT_ID,
            data_utils.EOS_ID,
            self.batch_size,
            self.beam_size,
            self.use_attention,
            self.use_copy,
            self.copy_fun,
            self.alpha,
            locally_normalized=(self.training_algorithm != "bso")
        ) if self.decoding_algorithm == "beam_search" else None

        # Mask out words not in the target vocab when computing generation
        # probabilities
        if self.use_copy and self.copy_fun != 'supervised':
            self.generation_mask = np.load(self.generation_mask_path)

        self.output_project = self.output_project()

    def embeddings(self):
        with tf.variable_scope(self.scope + "_embeddings", reuse=self.embedding_vars):
            print("target token vocabulary size = {}".format(self.vocab_size))
            sqrt3 = math.sqrt(3)
            initializer = tf.random_uniform_initializer(-sqrt3, sqrt3)
            embeddings = tf.get_variable("embedding",
                [self.vocab_size, self.dim], initializer=initializer)
            self.embedding_vars = True
            if self.use_token_features:
                return tf.nn.embedding_lookup(embeddings, self.token_features())
            else:
                return embeddings

    def token_features(self):
        return np.load(self.tg_token_features_path)

    def output_project(self):
        with tf.variable_scope(self.scope + "_output_project",
                               reuse=self.output_project_vars):
            w = tf.get_variable("proj_w", [self.dim, self.vocab_size])
            b = tf.get_variable("proj_b", [self.vocab_size])
            self.output_project_vars = True
        return (w, b)


class CopyCellWrapper(tf.nn.rnn_cell.RNNCell):
    def __init__(self, cell, output_project, num_layers, encoder_inputs,
                 tg_vocab_size, generation_mask):
        self.cell = cell
        self.output_project = output_project
        self.num_layers = num_layers
        self.tg_vocab_size = tg_vocab_size

        self.vocab_indices = tf.diag(tf.ones([tg_vocab_size], dtype=tf.float32))
        # self.vocab_indices = tf.zeros([tg_vocab_size, tg_vocab_size])
        self.encoder_size = len(encoder_inputs)
        encoder_inputs = tf.concat(1,
            [tf.expand_dims(x, 1) for x in encoder_inputs])
        self.encoder_inputs_3d = tf.nn.embedding_lookup(
            self.vocab_indices, encoder_inputs)
        self.generation_mask = generation_mask

        print("CopyCellWrapper added!")

    def __call__(self, input_embedding, state, attn_alignments=None, scope=None):
        assert(attn_alignments is not None)

        output, state, _ = self.cell(
            input_embedding, state, attn_alignments, scope)

        # Compute generation/copying mixture
        # TODO: compute the same loss function for LSTMs
        # generation probability
        W, b = self.output_project
        gen_logit = tf.exp(tf.matmul(output, W) + b) * self.generation_mask
        
        # copying probability
        pointers = attn_alignments[-1][1]
        copy_logit = tf.squeeze(tf.matmul(tf.expand_dims(tf.exp(pointers), 1),
                                          self.encoder_inputs_3d), 1)
        unk_mask = np.ones([1, self.tg_vocab_size])
        unk_mask[0, data_utils.UNK_ID] = 0
        copy_logit = copy_logit * unk_mask

        logit = gen_logit + copy_logit

        return logit, state, attn_alignments


class AttentionCellWrapper(tf.nn.rnn_cell.RNNCell):
    def __init__(self, cell, attention_states, encoder_attn_masks,
                 encoder_inputs, attention_function, attention_input_keep,
                 attention_output_keep, num_heads, num_layers, use_copy,
                 tg_vocab_size=-1):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param encoder_attn_masks: encoder input masks, used for masking out
            padded contents in the encoder inputs
        :param encoder_inputs: encoder input indices, used for generating masks
            for copying probabilities
        :param attention_input_keep: attention input state dropout
        :param attention_output_keep: attention hidden state dropout
        :param num_heads: Number of attention heads that read from from
            attention_states. Dummy field if attention_states is None.
        :param rnn_cell: Type of rnn cells used.
        :param num_layers: Number of layers in the RNN cells.

        :param use_copy: Copy source tokens to the target.
        :param copy_fun: Parameterization of the copying function.
        """
        attention_states = tf.nn.dropout(attention_states, attention_input_keep)
        attn_length = attention_states.get_shape()[1].value
        attn_vec_dim = attention_states.get_shape()[2].value
        attn_dim = attn_vec_dim

        self.cell = cell
        self.encoder_attn_masks = encoder_attn_masks
        self.encoder_size = len(encoder_inputs)
        self.vocab_indices = tf.diag(tf.ones(tg_vocab_size))
        encoder_inputs = tf.concat(1, [tf.expand_dims(x, 1)
                                       for x in encoder_inputs])
        self.encoder_inputs_3d = tf.nn.embedding_lookup(
            self.vocab_indices, encoder_inputs)
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.attn_vec_dim = attn_vec_dim
        self.attn_length = attn_length
        self.attn_dim = attn_dim
        self.attention_function = attention_function
        self.attention_input_keep = attention_input_keep
        self.attention_output_keep = attention_output_keep

        hidden = attention_states
        hidden_features = []
        v = []
        with tf.variable_scope("attention_cell_wrapper"):
            for a in xrange(num_heads):
                hidden_features.append(hidden)
        self.hidden = hidden
        self.hidden_features = hidden_features
        self.v = v

        self.use_copy = use_copy

        print("AttentionCellWrapper added!")

    def attention(self, state):
        """Put attention masks on hidden using hidden_features and query."""
        ds = []             # Results of attention reads will be stored here.
        alignments = []     # Alignment values for each attention head.
        if nest.is_sequence(state):  # If the query is a tuple, flatten it.
            # TODO: implement attention with LSTM cells
            query_list = nest.flatten(state)
            for q in query_list:  # Check that ndims == 2 if specified.
                ndims = q.get_shape().ndims
                if ndims:
                    assert ndims == 2
            state = tf.concat(1, query_list)

        for a in xrange(self.num_heads):
            with tf.variable_scope("Attention_%d" % a):
                y = tf.reshape(state, [-1, 1, 1, self.attn_vec_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                if self.attention_function == 'non-linear':
                    k = tf.get_variable("AttnW_%d" % a,
                                        [1, 1, 2*self.attn_vec_dim, self.attn_vec_dim])
                    l = tf.get_variable("Attnl_%d" % a,
                                        [1, 1, 1, self.attn_vec_dim])
                    z = tf.reshape(self.hidden_features[a],
                                   [-1, self.attn_length, 1, self.attn_vec_dim])
                    v = tf.concat(3, [z, tf.tile(y, [1, self.attn_length, 1, 1])])
                    s = tf.reduce_sum(
                        l * tf.tanh(tf.nn.conv2d(v, k, [1,1,1,1], "SAME")), [2, 3])
                elif self.attention_function == 'inner_product':
                    s = tf.reduce_sum(tf.mul(self.hidden_features[a], y), [2])
                else:
                    raise NotImplementedError

                # Apply attention masks
                s = s - (1 - self.encoder_attn_masks) * 1e9
                alignment = tf.nn.softmax(s)
                if a == 0:
                    alignments.append(alignment)
                else:
                    alignments.append(s)

                # Now calculate the attention-weighted vector d.
                d = tf.reduce_sum(
                        tf.reshape(alignment, [-1, self.attn_length, 1])
                            * self.hidden_features[a], [1])
                context = tf.reshape(d, [-1, self.attn_dim])
                ds.append(context)
        # attns = tf.concat(1, ds)

        self.attention_vars = True
        return ds, alignments

    def __call__(self, input_embedding, state, attn_alignments=None,
                 scope=None):
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
                if nest.is_sequence(state):
                    raise NotImplementedError
                else:
                    top_state = tf.split(1, self.num_layers, state)[-1]
            else:
                top_state = state
            attns, alignments = self.attention(top_state)

        with tf.variable_scope("AttnStateProjection"):
            attn_state = tf.tanh(tf.nn.rnn_cell._linear(
                [top_state, attns[0]], dim, True))

        with tf.variable_scope("AttnOutputProjection"):
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear(
                tf.nn.dropout(attn_state, self.attention_output_keep),
                dim, True)

        self.attention_cell_vars = True
        attn_alignments.append(alignments)

        return output, state, attn_alignments
