"""Customized Tensorflow RNNs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import hashlib
import numbers
import six

from tensorflow.python.util import nest
import tensorflow as tf


def RNNModel(cell, inputs, initial_state=None, dtype=None,
        sequence_length=None, num_cell_layers=None, scope=None):
  """Creates a recurrent neural network specified by RNNCell `cell`.

  The simplest form of RNN network generated is:
    state = cell.zero_state(...)
    outputs = []
    for input_ in inputs:
      output, state = cell(input_, state)
      outputs.append(output)
    return (outputs, state)

  However, a few other options are available:

  An initial state can be provided.
  If the sequence_length vector is provided, dynamic calculation is performed.
  This method of calculation does not compute the RNN steps past the maximum
  sequence length of the minibatch (thus saving computational time),
  and properly propagates the state at an example's sequence length
  to the final state output.

  The dynamic calculation performed is, at time t for batch row b,
    (output, state)(b, t) =
      (t >= sequence_length(b))
        ? (zeros(cell.output_size), states(b, sequence_length(b) - 1))
        : cell(input(b, t), state(b, t - 1))

  Args:
    cell: An instance of RNNCell.
    inputs: A length T list of inputs, each a tensor of shape
      [batch_size, input_size].
    initial_state: (optional) An initial state for the RNN.
      If `cell.state_size` is an integer, this must be
      a tensor of appropriate type and shape `[batch_size x cell.state_size]`.
      If `cell.state_size` is a tuple, this should be a tuple of
      tensors having shapes `[batch_size, s] for s in cell.state_size`.
    dtype: (optional) The data type for the initial state.  Required if
      initial_state is not provided.
    sequence_length: Specifies the length of each sequence in inputs.
      An int32 or int64 vector (tensor) size `[batch_size]`, values in `[0, T)`.
    num_cell_layers: Num of layers of the RNN cell. (Mainly used for generating
      output state representations for multi-layer RNN cells.)
    scope: VariableScope for the created subgraph; defaults to "RNN".

  Returns:
    A pair (outputs, state) where:
      - outputs is a length T list of outputs (one for each step)
      - states is a length T list of hidden states (one for each step)

  Raises:
    TypeError: If `cell` is not an instance of RNNCell.
    ValueError: If `inputs` is `None` or an empty list, or if the input depth
      (column size) cannot be inferred from inputs via shape inference.
  """

  if not isinstance(cell, tf.nn.rnn_cell.RNNCell):
    raise TypeError("cell must be an instance of RNNCell")
  if not isinstance(inputs, list):
    raise TypeError("inputs must be a list")
  if not inputs:
    raise ValueError("inputs must not be empty")

  outputs = []
  states = []
  # Create a new scope in which the caching device is either
  # determined by the parent scope, or is set to place the cached
  # Variable using the same placement as for the rest of the RNN.
  with tf.variable_scope(scope or "RNN") as varscope:
    if varscope.caching_device is None:
      varscope.set_caching_device(lambda op: op.device)

    # Temporarily avoid EmbeddingWrapper and seq2seq badness
    # TODO(lukaszkaiser): remove EmbeddingWrapper
    if inputs[0].get_shape().ndims != 1:
      (fixed_batch_size, input_size) = inputs[0].get_shape().with_rank(2)
      if input_size.value is None:
        raise ValueError(
            "Input size (second dimension of inputs[0]) must be accessible via "
            "shape inference, but saw value None.")
    else:
      fixed_batch_size = inputs[0].get_shape().with_rank_at_least(1)[0]

    if fixed_batch_size.value:
      batch_size = fixed_batch_size.value
    else:
      batch_size = tf.shape(inputs[0])[0]
    if initial_state is not None:
      state = initial_state
    else:
      if not dtype:
        raise ValueError("If no initial_state is provided, "
                           "dtype must be specified")
      state = cell.zero_state(batch_size, dtype)

    if sequence_length is not None:  # Prepare variables
      sequence_length = tf.to_int32(sequence_length)
      zero_output = tf.zeros(
          tf.pack([batch_size, cell.output_size]), inputs[0].dtype)
      zero_output.set_shape(
          tf.tensor_shape.TensorShape([fixed_batch_size.value, cell.output_size]))
      min_sequence_length = tf.reduce_min(sequence_length)
      max_sequence_length = tf.reduce_max(sequence_length)

    for time, input_ in enumerate(inputs):
      if time > 0: varscope.reuse_variables()
      # pylint: disable=cell-var-from-loop
      call_cell = lambda: cell(input_, state)
      # pylint: enable=cell-var-from-loop
      if sequence_length is not None:
        (output, state) = tf.nn.rnn._rnn_step(
            time=time,
            sequence_length=sequence_length,
            min_sequence_length=min_sequence_length,
            max_sequence_length=max_sequence_length,
            zero_output=zero_output,
            state=state,
            call_cell=call_cell,
            state_size=cell.state_size)
      else:
        (output, state) = call_cell()

      outputs.append(output)
      if num_cell_layers > 1:
        if _is_sequence(state):
            raise NotImplementedError
        else:
            states.append(tf.split(1, num_cell_layers, state))
      else:
        states.append(state)
    return (outputs, states)


def BiRNNModel(cell_fw, cell_bw, inputs, initial_state_fw=None,
               initial_state_bw=None, dtype=None, sequence_length=None,
               num_cell_layers=None, scope=None):
  """Creates a bidirectional recurrent neural network.

  Similar to the unidirectional case above (rnn) but takes input and builds
  independent forward and backward RNNs with the final forward and backward
  outputs depth-concatenated, such that the output will have the format
  [time][batch][cell_fw.output_size + cell_bw.output_size]. The input_size of
  forward and backward cell must match. The initial state for both directions
  is zero by default (but can be set optionally) and no intermediate states are
  ever returned -- the network is fully unrolled for the given (passed in)
  length(s) of the sequence(s) or completely unrolled if length(s) is not given.

  Args:
    cell_fw: An instance of RNNCell, to be used for forward direction.
    cell_bw: An instance of RNNCell, to be used for backward direction.
    inputs: A length T list of inputs, each a tensor of shape
      [batch_size, input_size].
    initial_state_fw: (optional) An initial state for the forward RNN.
      This must be a tensor of appropriate type and shape
      `[batch_size x cell_fw.state_size]`.
      If `cell_fw.state_size` is a tuple, this should be a tuple of
      tensors having shapes `[batch_size, s] for s in cell_fw.state_size`.
    initial_state_bw: (optional) Same as for `initial_state_fw`, but using
      the corresponding properties of `cell_bw`.
    dtype: (optional) The data type for the initial state.  Required if
      either of the initial states are not provided.
    sequence_length: (optional) An int32/int64 vector, size `[batch_size]`,
      containing the actual lengths for each of the sequences.
    num_cell_layers: Num of layers of the RNN cell. (Mainly used for generating
      output state representations for multi-layer RNN cells.)
    scope: VariableScope for the created subgraph; defaults to "BiRNN"

  Returns:
    A tuple (outputs, output_state_fw, output_state_bw) where:
      outputs is a length `T` list of outputs (one for each input), which
        are depth-concatenated forward and backward outputs.
      output_state_fw is the final state of the forward rnn.
      output_state_bw is the final state of the backward rnn.

  Raises:
    TypeError: If `cell_fw` or `cell_bw` is not an instance of `RNNCell`.
    ValueError: If inputs is None or an empty list.
  """

  if not isinstance(cell_fw, tf.nn.rnn_cell.RNNCell):
    raise TypeError("cell_fw must be an instance of RNNCell")
  if not isinstance(cell_bw, tf.nn.rnn_cell.RNNCell):
    raise TypeError("cell_bw must be an instance of RNNCell")
  if not isinstance(inputs, list):
    raise TypeError("inputs must be a list")
  if not inputs:
    raise ValueError("inputs must not be empty")

  name = scope or "BiRNN"
  # Forward direction
  with tf.variable_scope(name + "_FW") as fw_scope:
    output_fw, output_states_fw = RNNModel(cell_fw, inputs, initial_state_fw, dtype,
                       sequence_length, num_cell_layers=num_cell_layers, scope=fw_scope)

  # Backward direction
  with tf.variable_scope(name + "_BW") as bw_scope:
    tmp, tmp_states = RNNModel(cell_bw, _reverse_seq(inputs, sequence_length),
                         initial_state_bw, dtype, sequence_length,
                         num_cell_layers=num_cell_layers, scope=bw_scope)
  output_bw = _reverse_seq(tmp, sequence_length)
  output_states_bw = _reverse_seq(tmp_states, sequence_length)

  # Concat each of the forward/backward outputs
  outputs = [tf.concat(1, [fw, bw])
             for fw, bw in zip(output_fw, output_bw)]

  return (outputs, output_states_fw, output_states_bw)


def _reverse_seq(input_seq, lengths):
  """Reverse a list of Tensors up to specified lengths.

  Args:
    input_seq: Sequence of seq_len tensors of dimension (batch_size, depth)
    lengths:   A tensor of dimension batch_size, containing lengths for each
               sequence in the batch. If "None" is specified, simply reverses
               the list.

  Returns:
    time-reversed sequence
  """
  if lengths is None:
    return list(reversed(input_seq))

  input_shape = tf.tensor_shape.matrix(None, None)
  for input_ in input_seq:
    input_shape.merge_with(input_.get_shape())
    input_.set_shape(input_shape)

  # Join into (time, batch_size, depth)
  s_joined = tf.pack(input_seq)

  # TODO(schuster, ebrevdo): Remove cast when reverse_sequence takes int32
  if lengths is not None:
    lengths = tf.to_int64(lengths)

  # Reverse along dimension 0
  s_reversed = tf.reverse_sequence(s_joined, lengths, 0, 1)
  # Split again into list
  result = tf.unpack(s_reversed)
  for r in result:
    r.set_shape(input_shape)
  return result


def _is_sequence(seq):
  return (isinstance(seq, collections.Sequence)
          and not isinstance(seq, six.string_types))


class DropoutWrapper(tf.nn.rnn_cell.RNNCell):
  """Operator adding dropout to inputs and outputs of the given cell."""

  def __init__(self, cell, input_keep_prob=1.0, output_keep_prob=1.0,
               state_keep_prob=1.0, variational_recurrent=False,
               input_size=None, dtype=None, seed=None):
    """Create a cell with added input, state, and/or output dropout.
    If `variational_recurrent` is set to `True` (**NOT** the default behavior),
    then the same dropout mask is applied at every step, as described in:
    Y. Gal, Z Ghahramani.  "A Theoretically Grounded Application of Dropout in
    Recurrent Neural Networks".  https://arxiv.org/abs/1512.05287
    Otherwise a different dropout mask is applied at every time step.
    Args:
      cell: an RNNCell, a projection to output_size is added to it.
      input_keep_prob: unit Tensor or float between 0 and 1, input keep
        probability; if it is constant and 1, no input dropout will be added.
      output_keep_prob: unit Tensor or float between 0 and 1, output keep
        probability; if it is constant and 1, no output dropout will be added.
      state_keep_prob: unit Tensor or float between 0 and 1, output keep
        probability; if it is constant and 1, no output dropout will be added.
        State dropout is performed on the *output* states of the cell.
      variational_recurrent: Python bool.  If `True`, then the same
        dropout pattern is applied across all time steps per run call.
        If this parameter is set, `input_size` **must** be provided.
      input_size: (optional) (possibly nested tuple of) `TensorShape` objects
        containing the depth(s) of the input tensors expected to be passed in to
        the `DropoutWrapper`.  Required and used **iff**
         `variational_recurrent = True` and `input_keep_prob < 1`.
      dtype: (optional) The `dtype` of the input, state, and output tensors.
        Required and used **iff** `variational_recurrent = True`.
      seed: (optional) integer, the randomness seed.
    Raises:
      TypeError: if cell is not an RNNCell.
      ValueError: if any of the keep_probs are not between 0 and 1.
    """
    if not isinstance(cell, tf.nn.rnn_cell.RNNCell):
      raise TypeError("The parameter cell is not a RNNCell.")
    with tf.name_scope("DropoutWrapperInit"):
      def tensor_and_const_value(v):
        tensor_value = tf.convert_to_tensor(v)
        const_value = tf.contrib.util.constant_value(tensor_value)
        return (tensor_value, const_value)
      for prob, attr in [(input_keep_prob, "input_keep_prob"),
                         (state_keep_prob, "state_keep_prob"),
                         (output_keep_prob, "output_keep_prob")]:
        tensor_prob, const_prob = tensor_and_const_value(prob)
        if const_prob is not None:
          if const_prob < 0 or const_prob > 1:
            raise ValueError("Parameter %s must be between 0 and 1: %d"
                             % (attr, const_prob))
          setattr(self, "_%s" % attr, float(const_prob))
        else:
          setattr(self, "_%s" % attr, tensor_prob)

    # Set cell, variational_recurrent, seed before running the code below
    self._cell = cell
    self._variational_recurrent = variational_recurrent
    self._seed = seed

    self._recurrent_input_noise = None
    self._recurrent_state_noise = None
    self._recurrent_output_noise = None

    if variational_recurrent:
      if dtype is None:
        raise ValueError(
            "When variational_recurrent=True, dtype must be provided")

      def convert_to_batch_shape(s):
        # Prepend a 1 for the batch dimension; for recurrent
        # variational dropout we use the same dropout mask for all
        # batch elements.
        return tf.concat(
            ([1], tf.shape(s).as_list()), 0)

      def batch_noise(s, inner_seed):
        shape = convert_to_batch_shape(s)
        return tf.random_uniform(shape, seed=inner_seed, dtype=dtype)

      if (not isinstance(self._input_keep_prob, numbers.Real) or
          self._input_keep_prob < 1.0):
        if input_size is None:
          raise ValueError(
              "When variational_recurrent=True and input_keep_prob < 1.0 or "
              "is unknown, input_size must be provided")
        self._recurrent_input_noise = _enumerated_map_structure(
            lambda i, s: batch_noise(s, inner_seed=self._gen_seed("input", i)),
            input_size)
      self._recurrent_state_noise = _enumerated_map_structure(
          lambda i, s: batch_noise(s, inner_seed=self._gen_seed("state", i)),
          cell.state_size)
      self._recurrent_output_noise = _enumerated_map_structure(
          lambda i, s: batch_noise(s, inner_seed=self._gen_seed("output", i)),
          cell.output_size)

  def _gen_seed(self, salt_prefix, index):
    if self._seed is None:
      return None
    salt = "%s_%d" % (salt_prefix, index)
    string = (str(self._seed) + salt).encode("utf-8")
    return int(hashlib.md5(string).hexdigest()[:8], 16) & 0x7FFFFFFF

  @property
  def state_size(self):
    return self._cell.state_size

  @property
  def output_size(self):
    return self._cell.output_size

  def zero_state(self, batch_size, dtype):
    with tf.name_scope(type(self).__name__ + "ZeroState", values=[batch_size]):
      return self._cell.zero_state(batch_size, dtype)

  def _variational_recurrent_dropout_value(
      self, index, value, noise, keep_prob):
    """Performs dropout given the pre-calculated noise tensor."""
    # uniform [keep_prob, 1.0 + keep_prob)
    random_tensor = keep_prob + noise

    # 0. if [keep_prob, 1.0) and 1. if [1.0, 1.0 + keep_prob)
    binary_tensor = tf.floor(random_tensor)
    ret = tf.div(value, keep_prob) * binary_tensor
    ret.set_shape(value.get_shape())
    return ret

  def _dropout(self, values, salt_prefix, recurrent_noise, keep_prob):
    """Decides whether to perform standard dropout or recurrent dropout."""
    if not self._variational_recurrent:
      def dropout(i, v):
        return tf.nn.dropout(
            v, keep_prob=keep_prob, seed=self._gen_seed(salt_prefix, i))
      return _enumerated_map_structure(dropout, values)
    else:
      def dropout(i, v, n):
        return self._variational_recurrent_dropout_value(i, v, n, keep_prob)
      return _enumerated_map_structure(dropout, values, recurrent_noise)

  def __call__(self, inputs, state, scope=None):
    """Run the cell with the declared dropouts."""
    def _should_dropout(p):
      return (not isinstance(p, float)) or p < 1

    if _should_dropout(self._input_keep_prob):
      inputs = self._dropout(inputs, "input",
                             self._recurrent_input_noise,
                             self._input_keep_prob)
    output, new_state = self._cell(inputs, state, scope)
    if _should_dropout(self._state_keep_prob):
      new_state = self._dropout(new_state, "state",
                                self._recurrent_state_noise,
                                self._state_keep_prob)
    if _should_dropout(self._output_keep_prob):
      output = self._dropout(output, "output",
                             self._recurrent_output_noise,
                             self._output_keep_prob)
    return output, new_state

def _enumerated_map_structure(map_fn, *args, **kwargs):
  ix = [0]
  def enumerated_fn(*inner_args, **inner_kwargs):
    r = map_fn(ix[0], *inner_args, **inner_kwargs)
    ix[0] += 1
    return r
  return nest.map_structure(enumerated_fn, *args, **kwargs)
