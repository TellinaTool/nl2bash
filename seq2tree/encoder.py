"""A set of encoder modules used in the encoder-decoder framework."""

import tensorflow as tf
import graph_utils

from tensorflow.python.util import nest

class RNNEncoder(object):
    def __init__(self, dim, rnn_cell, max_num_steps, num_layers):
        self.dim = dim
        self.rnn_cell = rnn_cell
        self.max_num_steps = max_num_steps
        self.num_layers = num_layers
        self.cell, _ = self.encoder_cell()

    def define_graph(self, encoder_inputs):
        encoder_cell = tf.nn.rnn_cell.EmbeddingWrapper(
            self.cell, embedding_classes=self.max_num_steps, embedding_size=self.dim)
        encoder_outputs, encoder_state = \
            tf.nn.rnn(encoder_cell, encoder_inputs, dtype=tf.float32)
        return encoder_outputs, encoder_state

    def encoder_cell(self):
        """RNN cell for the encoder."""
        with tf.variable_scope("encoder_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope, self.dim, self.num_layers)
        return cell, scope


class BiRNNEncoder(object):
    def __init__(self, dim, rnn_cell, max_num_steps, num_layers):
        self.dim = dim
        self.rnn_cell = rnn_cell
        self.max_num_steps = max_num_steps
        self.num_layers = num_layers
        self.fw_cell, _ = self.forward_cell()
        self.bw_cell, _ = self.backward_cell()

    def define_graph(self, encoder_inputs, embeddings):
        self.embeddings = embeddings
        input_embeddings = [tf.nn.embedding_lookup(self.embeddings, encoder_input)
                            for encoder_input in encoder_inputs]

        with tf.variable_scope("forward_rnn") as scope:
            output_fw, state_fw = tf.nn.rnn(self.fw_cell, input_embeddings, dtype=tf.float32,
                                            scope=scope)

        with tf.variable_scope("backward_rnn") as scope:
            reversed_input_embeddings = [input in reversed(input_embeddings)]
            output_bw, state_bw = tf.nn.rnn(self.bw_cell, reversed_input_embeddings, dtype=tf.float32,
                                            scope=scope)

        output_bw = reversed(output_bw)

        # Concat each of the forward/backward outputs
        flat_output_fw = nest.flatten(output_fw)
        flat_output_bw = nest.flatten(output_bw)
        flat_outputs = tuple(tf.concat(1, [fw, bw]) for fw, bw in zip(flat_output_fw, flat_output_bw))
        outputs = nest.pack_sequence_as(structure=output_fw,
                                        flat_sequence=flat_outputs)

        W, b = self.output_projection()
        projected_outputs = [tf.matmul(output, W) + b for output in outputs]

        if self.rnn_cell == "gru":
            state = tf.concat(1, [state_fw, state_bw])
            projected_state = tf.matmul(state, W) + b
        elif self.rnn_cell == "lstm":
            cell_fw, hidden_fw = state_fw
            cell_bw, hidden_bw = state_bw
            cell = tf.concat(1, [cell_fw, cell_bw])
            hidden = tf.concat(1, [hidden_fw, hidden_bw])
            projected_cell = tf.matmul(cell, W) + b
            projected_hidden = tf.matmul(hidden, W) + b
            projected_state = tf.nn.rnn_cell.LSTMStateTuple(projected_cell,
                                                            projected_hidden)
        else:
            raise AttributeError("Unrecognized RNN cell type.")

        return projected_outputs, projected_state


    def forward_cell(self):
        """RNN cell for the forward RNN."""
        with tf.variable_scope("forward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope, self.dim, self.num_layers)
        return cell, scope

    def backward_cell(self):
        """RNN cell for the backward RNN."""
        with tf.variable_scope("backward_cell") as scope:
            cell = graph_utils.create_multilayer_cell(self.rnn_cell, scope, self.dim, self.num_layers)
        return cell, scope

    def output_projection(self):
        with tf.variable_scope("birnn_output_projection"):
            w = tf.get_variable("proj_w", [self.dim * 2, self.dim])
            b = tf.get_variable("proj_b", [self.dim])
        return (w, b)



