import tensorflow as tf

import graph_utils

class Decoder(graph_utils.NNModel):
    def __init__(self, hyperparameters, output_projection=None):
        super(Decoder, self).__init__(hyperparameters)
        self.output_projection = output_projection

        # variable sharing
        self.attention_vars = False
        self.attention_cell_vars = False
        self.attention_hidden_vars = False
        self.normal_cell_vars = False

    def attention_cell(self, cell, cell_scope, input_embedding, state, attns,
                       hidden_features, v, num_heads, hidden):
        with tf.variable_scope("AttnInputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on cell and hidden states
            attn_vec_dim = v[0].get_shape()[0].value
            attns.set_shape([self.batch_size, num_heads * attn_vec_dim])
            x = tf.nn.rnn_cell._linear([input_embedding] + [attns], self.dim, True)
            try:
                cell_output, state = cell(x, state, cell_scope)
            except ValueError, e:
                cell_scope.reuse_variables()
                cell_output, state = cell(x, state, cell_scope)
            attns, attn_mask = \
                self.attention(v, state, hidden_features, num_heads, hidden)
        with tf.variable_scope("AttnOutputProjection"):
            if self.attention_cell_vars:
                tf.get_variable_scope().reuse_variables()
            # attention mechanism on output state
            output = tf.nn.rnn_cell._linear([cell_output] + [attns], self.dim, True)
        self.attention_cell_vars = True
        return output, state, attns, attn_mask

    def attention(self, v, state, hidden_features, num_heads, hidden):
        assert(len(v) > 0)
        attn_vec_dim = v[0].get_shape()[0].value
        attn_length = hidden.get_shape()[1].value
        """Put attention masks on hidden using hidden_features and query."""
        ds = []  # Results of attention reads will be stored here.
        for a in xrange(num_heads):
            with tf.variable_scope("Attention_%d" % a):
                if self.attention_vars:
                    tf.get_variable_scope().reuse_variables()
                y = tf.nn.rnn_cell._linear(state, attn_vec_dim, True)
                y = tf.reshape(y, [-1, 1, 1, attn_vec_dim])
                # Attention mask is a softmax of v^T * tanh(...).
                s = tf.reduce_sum(
                    v[a] * tf.tanh(hidden_features[a] + y), [2, 3])
                attn_mask = tf.nn.softmax(s)
                # Now calculate the attention-weighted vector d.
                d = tf.reduce_sum(
                    tf.reshape(attn_mask, [-1, attn_length, 1, 1]) * hidden,
                    [1, 2])
                ds.append(tf.reshape(d, [-1, attn_vec_dim]))
        attns = tf.concat(1, ds)
        attns.set_shape([self.batch_size, num_heads * attn_vec_dim])
        self.attention_vars = True
        return attns, attn_mask

    def attention_hidden_layer(self, attention_states, num_heads):
        """
        Hidden layer above attention states.
        :param attention_states: 3D Tensor [batch_size x attn_length x attn_dim].
        :param num_heads: Number of attention heads that read from from attention_states.
                         Dummy field if attention_states is None.
        """
        attn_length = attention_states.get_shape()[1].value
        attn_vec_dim = attention_states.get_shape()[2].value

        # To calculate W1 * h_t we use a 1-by-1 convolution
        hidden = tf.reshape(attention_states, [-1, attn_length, 1, attn_vec_dim])
        hidden_features = []
        v = []
        with tf.variable_scope("attention_hidden_layer"):
            if self.attention_hidden_vars:
                tf.get_variable_scope().reuse_variables()
            for i in xrange(num_heads):
                k = tf.get_variable("AttnW_%d" % i, [1, 1, attn_vec_dim, attn_vec_dim])
                hidden_features.append(tf.nn.conv2d(hidden, k, [1,1,1,1], "SAME"))
                v.append(tf.get_variable("AttnV_%d" % i, [attn_vec_dim]))
        self.attention_hidden_vars = True
        return hidden, hidden_features, v


    def normal_cell(self, cell, scope, input, state):
        try:
            output, state = cell(input, state, scope)
        except ValueError, e:
            scope.reuse_variables()
            output, state = cell(input, state, scope)
        return output, state