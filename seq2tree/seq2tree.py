""" Library for creating sequence-to-tree models in TensorFlow.

* Full sequence-to-tree models.
    - basic_rnn_seq2tree: The most basic RNN
"""

# --- Dynamic Neural Network Construction ---
def basic_tree_rnn(cell, inputs, initial_state):
    """
    Implementation of dynamic tree RNN constructed in a depth-first order.
    :param cell: An instance of TreeRNNCell.
    :param inputs: A `Tensor` of shape [time, batch_size, input_size].
    :param initial_state: A `Tensor` of shape `[batch_size, state_size]`, or if
        `cell.state_size` is a tuple, then this should be a tuple of tensors
        having shapes `[batch_size, s] for s in cell.state_size`.

    :return:
        Tuple `(final_outputs, final_state)`.
        final_outputs:
            A `Tensor` of shape `[time, batch_size, cell.output_size]`,
    """