"""
A class of neural tree search algorithms in Tensorflow.
"""

from tensorflow.python.ops import array_ops
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import variable_scope as vs

from encoder_decoder import rnn

class TreeRNNCell(object):
    """Abstract object representing a tree-RNN cell.

    self.input_size = D
    self.state_size = H
    self.output_size = N
    A tree RNN cell has a state and performs some operation that takes a matrix
    of inputs (batch_size x D). This operation results in an output matrix (batch_size x N).

    This module is a common interface to implementations of a number of commonly
    used recurrent architecture, such as LSTM (Long Short Term Memory) or GRU (
    Gated Recurrent Unit), and a number of operators that allow dropouts, projections, or
    embeddings for inputs.
    """

    def __call__(self, inputs, parent_state, cyc_state, scope=None):
        """
        :param inputs: `2-D` tensor with shape `[batch_size x D]`.
        :param parent_state: hidden_state of parent cell,
            `2-D` tensor with shape `[batch_size x H]`
        :param cyc_state: hidden state of current youngest child cell,
            `2-D` tensor with shape `[batch_size x H]`
        :param scope: VariableScope for the created subgraph; defaults to class name.

        :return:
            A pair containing:
            - output: A `2-D` tensor with shape `[batch_size x N]`
            - new state: A `2-D` tensor with shape `[batch_size x H]`.
        """
        raise NotImplementedError("Abstract method")

    @property
    def state_size(self):
        raise NotImplementedError("Abstract method")

    @property
    def output_size(self):
        raise NotImplementedError("Abstract method")

    def zero_state(self, batch_size, dtype):
        """Return zero-filled state tensor(s).

        Args:
          batch_size: int, float, or unit Tensor representing the batch size.
          dtype: the data type to use for the state.

        Returns:
          If `state_size` is an int, then the return value is a `2-D` tensor of
          shape `[batch_size x state_size]` filled with zeros.

          If `state_size` is a nested list or tuple, then the return value is
          a nested list or tuple (of the same structure) of `2-D` tensors with
        the shapes `[batch_size x s]` for each s in `state_size`.
        """
        state_size = self.state_size
        state_size_flat = rnn_cell._unpacked_state(state_size)
        zeros_flat = [
            array_ops.zeros(array_ops.pack([batch_size, s]), dtype=dtype)
            for s in state_size_flat]
        for s, z in zip(state_size_flat, zeros_flat):
            z.set_shape([None, s])
        zeros = rnn_cell._packed_state(structure=state_size, state=zeros_flat)

        return zeros

class BasicTreeLSTMCell(TreeRNNCell):
    """Basic tree LSTM recurrent neural network cell.

       The implementation is based on BasicLSTMCell in rnn_cell.py.
    """
    def __init__(self, num_units, forget_bias=1.0, activation=False):
        """
        Initialize the basic tree LSTM cell.

        :param num_units: The number of units in the tree LSTM cell.
                          = input_size
                          = output_size
                          = state_size
        :param forget_bias: float, The bias added to forget gates.
        :param activation: Activation function of the inner states.
        """
        self._num_units = num_units
        self._forget_bias = forget_bias
        self._activation = activation

    @property
    def state_size(self):
        return rnn_cell.LSTMStateTuple(self._num_units, self._num_units)

    @property
    def output_size(self):
        return self._num_units

    def __call__(self, inputs, parent_state, cyc_state, scope=None):
        """Modified Long short-term memory for tree structure"""
        with vs.variable_scope(scope or type(self).__name__):   # "BasicTreeLSTMCell"
            # parameters of gates are concatenated into one multiply for efficiency
            parent_c, parent_h = parent_state
            cyc_c, cyc_h = cyc_state
            c = rnn.linear([parent_c, cyc_c], self._num_units, True)
            concat = rnn.linear([inputs, parent_h, cyc_h], 4 * self._num_units, True)

            # i = input_gate, j = new_input, f = forget_gate, o = output_gate
            i, j, f, o = array_ops.split(1, 4, concat)

            new_c = [c * rnn_cell.sigmoid(f + self._forget_bias)
                     + rnn_cell.sigmoid(i) * self._activation(j)]
            new_h = self._activation(new_c) * rnn_cell.sigmoid(o)

            new_state = rnn_cell.LSTMStateTuple(new_c, new_h)

            return new_h, new_state

