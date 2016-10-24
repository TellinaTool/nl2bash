import tensorflow as tf

import graph_utils

class Decoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, output_projection=None):
        super(Decoder, self).__init__(hyperparameters)
        self.output_projection = output_projection


class AttentionCellWrapper(tf.nn.rnn_cell.RNNCell):

    def __init__(self, cell, attention_states, encoder_attn_masks, attention_input_keep,
                 attention_output_keep, num_heads=1, reuse_variables=False):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param attention_input_keep: attention input state dropout
        :param attention_output_keep: attention hidden state dropout
        :param num_heads: Number of attention heads that read from from attention_states.
            Dummy field if attention_states is None.
        :param reuse_variables: reuse variables in scope.
        """
        attention_states = tf.nn.dropout(attention_states, attention_input_keep)
        attn_length = attention_states.get_shape()[1].value
        attn_vec_dim = attention_states.get_shape()[2].value
        attn_dim = attn_vec_dim 

        # To calculate W1 * h_t we use a 1-by-1 convolution
        hidden = tf.reshape(attention_states, [-1, attn_length, 1, attn_vec_dim])
        hidden_features = []
        v = []
        with tf.variable_scope("attention_cell_wrapper") as scope:
            if reuse_variables:
                scope.reuse_variables()
            for a in xrange(num_heads):
                # k = tf.get_variable("AttnW_%d" % a, [1, 1, attn_vec_dim, attn_dim])
                # hidden_features.append(tf.nn.conv2d(hidden, k, [1,1,1,1], "SAME"))
                hidden_features.append(hidden)
                v.append(tf.get_variable("AttnV_%d" % a, [attn_vec_dim]))

        self.cell = cell
        self.encoder_attn_masks = encoder_attn_masks
        self.num_heads = num_heads
        self.attn_vec_dim = attn_vec_dim
        self.attn_length = attn_length
        self.attn_dim = attn_dim
        self.attention_input_keep = attention_input_keep
        self.attention_output_keep = attention_output_keep
        self.hidden = hidden
        self.hidden_features = hidden_features
        self.v = v

        # variable sharing
        self.attention_vars = False
        self.attention_cell_vars = False

    def attention(self, state):
        """Put attention masks on hidden using hidden_features and query."""
        ds = []  # Results of attention reads will be stored here.
        for a in xrange(self.num_heads):
            with tf.variable_scope("Attention_%d" % a):
                if self.attention_vars:
                    tf.get_variable_scope().reuse_variables()
                # y = tf.nn.rnn_cell._linear(state, attn_vec_dim, True)
                y = state
                y = tf.reshape(y, [-1, 1, 1, self.attn_vec_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                # s = tf.reduce_sum(
                #     v[a] * tf.tanh(hidden_features[a] + y), [2, 3])
                # s = tf.reduce_sum(
                #     self.v[a] * tf.mul(self.hidden_features[a], y), [2, 3])
                s = tf.reduce_sum(tf.mul(self.hidden, y), [2, 3])
                s = s - (1 - self.encoder_attn_masks) * 1e10
                attn_mask = tf.nn.softmax(s)
                attn_mask = tf.mul(self.encoder_attn_masks, attn_mask)
                # Now calculate the attention-weighted vector d.
                d = tf.reduce_sum(tf.reshape(attn_mask, [-1, self.attn_length, 1, 1])
                                  * self.hidden_features[a], [1, 2])
                ds.append(tf.reshape(d, [-1, self.attn_dim]))
        attns = tf.concat(1, ds)
        attns.set_shape([None, self.num_heads * self.attn_dim])
        self.attention_vars = True
        return attns, attn_mask

    def __call__(self, input_embedding, state, attn_masks, scope=None):
        dim = state.get_shape()[1].value
        with tf.variable_scope("AttnInputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            _, state = self.cell(input_embedding, state, scope)
            attns, attn_mask = self.attention(state)

        with tf.variable_scope("AttnStateProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            attn_state = tf.tanh(tf.nn.rnn_cell._linear([state, attns], dim, True))

        with tf.variable_scope("AttnOutputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear(
                tf.nn.dropout(attn_state, self.attention_output_keep), dim, True)

        self.attention_cell_vars = True

        attn_masks = tf.concat(1, [attn_masks, tf.expand_dims(attn_mask, 1)])
        return output, state, attn_masks
