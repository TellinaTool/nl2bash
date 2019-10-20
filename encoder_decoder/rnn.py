"""Customized Tensorflow RNNs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from tensorflow.python.util import nest
import tensorflow as tf

from encoder_decoder.graph_utils import nest_map_dual


def create_multilayer_cell(rnn_cell, scope, dim, num_layers,
        input_keep_prob=1, output_keep_prob=1, variational_recurrent=True,
        input_dim=-1, batch_normalization=True, forward_only=None):
    """
    Create the multi-layer RNN cell.
    :param type: Type of RNN cell.
    :param scope: Variable scope.
    :param dim: Dimension of hidden layers.
    :param num_layers: Number of layers of cells.
    :param input_keep_prob: Proportion of input to keep in dropout.
    :param output_keep_prob: Proportion of output to keep in dropout.
    :param variational_recurrent: If set, use variational recurrent dropout.
        (cf. https://arxiv.org/abs/1512.05287)
    :param input_dim: RNN input dimension, must be specified if it is
        different from the cell state dimension.
    :param batch_normalization: If set, use recurrent batch normalization.
        (cf. https://arxiv.org/abs/1603.09025)
    :param forward_only: If batch_normalization is set, inform the cell about
        the batch normalization process.
    :return: RNN cell as specified.
    """
    with tf.compat.v1.variable_scope(scope):
        if rnn_cell == "lstm":
            if batch_normalization:
                print("-- using recurrent batch normalization")
                cell = BNLSTMCell(
                    dim, forward_only=forward_only, state_is_tuple=True)
            else:
                cell = tf.compat.v1.nn.rnn_cell.LSTMCell(dim, state_is_tuple=True)
        elif rnn_cell == "gru":
            cell = tf.compat.v1.nn.rnn_cell.GRUCell(dim)
        elif rnn_cell == 'ran':
            cell = RANCell(dim)
        else:
            raise ValueError("Unrecognized RNN cell type: {}.".format(type))

        assert(input_keep_prob >= 0 and output_keep_prob >= 0)
        if input_keep_prob < 1 or output_keep_prob < 1:
            if input_dim == -1:
                input_dim = dim
            print("-- rnn dropout input keep probability: {}".format(input_keep_prob))
            print("-- rnn dropout output keep probability: {}".format(output_keep_prob))
            if variational_recurrent:
                print("-- using variational dropout")
            cell = tf.compat.v1.nn.rnn_cell.DropoutWrapper(cell,
                input_keep_prob=input_keep_prob,
                output_keep_prob=output_keep_prob,
                variational_recurrent=variational_recurrent,
                input_size=input_dim, dtype=tf.float32)

        if num_layers > 1:
            cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell(
                [cell] * num_layers, state_is_tuple=(rnn_cell=="lstm"))
    return cell


class BNLSTMCell(tf.compat.v1.nn.rnn_cell.RNNCell):
  """
  Batch Normalized Long short-term memory unit (LSTM) recurrent network cell.

  cf. Recurrent Batch Normalization
    https://arxiv.org/abs/1603.09025

  cf. A Gentle Guide to Using Batch Normalization in TensorFlow
    http://ruishu.io/2016/12/27/batchnorm/
  """

  def __init__(self, num_units, forward_only, gamma_c=1.0, gamma_h=1.0,
               gamma_x=1.0, beta_c=0.0, beta_h=0.0, beta_x=0.0, 
               input_size=None, use_peepholes=False, cell_clip=None,
               initializer=None, num_proj=None,
               num_unit_shards=1, num_proj_shards=1,
               forget_bias=1.0, state_is_tuple=False,
               activation=tf.tanh):
    """Initialize the parameters for an LSTM cell.

    Args:
      num_units: int, The number of units in the LSTM cell
      forward_only:
        If False (training):
          1. Normalize layer activations according to mini-batch statistics.
          2. During the training step, update population statistics
             approximation via moving average of mini-batch statistics.
        If True (testing):
          1. Normalize layer activations according to estimated population
             statistics.
          2. No update of population statistics according to mini-batch
             statistcs from test data.
      gamma_c: Scale of cell state normalization
      beta_c: Offset of cell state normalization
      gamma_h: Scale of hidden state normalization
      beta_h: Offset of hidden state normalization
        (set to 0 to avoid redundancy)
      gamma_x: Scale of input normalization
      beta_x: Offset of input normalization
        (set to 0 to avoid redundancy)
      input_size: Deprecated and unused.
      use_peepholes: bool, Set True to enable diagonal/peephole connections.
      cell_clip: (optional) A float value, if provided the cell state is clipped
        by this value prior to the cell output activation.
      initializer: (optional) The initializer to use for the weight and
        projection matrices.
      num_proj: (optional) int, The output dimensionality for the projection
        matrices.  If None, no projection is performed.
      num_unit_shards: How to split the weight matrix.  If >1, the weight
        matrix is stored across num_unit_shards.
      num_proj_shards: How to split the projection matrix.  If >1, the
        projection matrix is stored across num_proj_shards.
      forget_bias: Biases of the forget gate are initialized by default to 1
        in order to reduce the scale of forgetting at the beginning of
        the training.
      state_is_tuple: If True, accepted and returned states are 2-tuples of
        the `c_state` and `m_state`.  By default (False), they are concatenated
        along the column axis.  This default behavior will soon be deprecated.
      activation: Activation function of the inner states.
    """
    if not state_is_tuple:
      logging.warn(
          "%s: Using a concatenated state is slower and will soon be "
          "deprecated.  Use state_is_tuple=True." % self)
    if input_size is not None:
      logging.warn("%s: The input_size parameter is deprecated." % self)
    self._num_units = num_units
    self.forward_only = forward_only
    self._gamma_c = gamma_c
    self._beta_c = beta_c
    self._gamma_h = gamma_h
    self._beta_h = beta_h
    self._gamma_x = gamma_x
    self._beta_x = beta_x
    self._use_peepholes = use_peepholes
    self._cell_clip = cell_clip
    self._initializer = initializer
    self._num_proj = num_proj
    self._num_unit_shards = num_unit_shards
    self._num_proj_shards = num_proj_shards
    self._forget_bias = forget_bias
    self._state_is_tuple = state_is_tuple
    self._activation = activation

    if num_proj:
      self._state_size = (
          tf.compat.v1.nn.rnn_cell.LSTMStateTuple(num_units, num_proj)
          if state_is_tuple else num_units + num_proj)
      self._output_size = num_proj
    else:
      self._state_size = (
          tf.compat.v1.nn.rnn_cell.LSTMStateTuple(num_units, num_units)
          if state_is_tuple else 2 * num_units)
      self._output_size = num_units

  @property
  def state_size(self):
    return self._state_size

  @property
  def output_size(self):
    return self._output_size

  def __call__(self, inputs, state, scope=None):
    """Run one step of LSTM.

    Args:
      inputs: input Tensor, 2D, batch x num_units.
      state: if `state_is_tuple` is False, this must be a state Tensor,
        `2-D, batch x state_size`.  If `state_is_tuple` is True, this must be a
        tuple of state Tensors, both `2-D`, with column sizes `c_state` and
        `m_state`.
      scope: VariableScope for the created subgraph; defaults to "LSTMCell".

    Returns:
      A tuple containing:
      - A `2-D, [batch x output_dim]`, Tensor representing the output of the
        LSTM after reading `inputs` when previous state was `state`.
        Here output_dim is:
           num_proj if num_proj was set,
           num_units otherwise.
      - Tensor(s) representing the new state of LSTM after reading `inputs` when
        the previous state was `state`.  Same type and shape(s) as `state`.

    Raises:
      ValueError: If input size cannot be inferred from inputs via
        static shape inference.
    """
    num_proj = self._num_units if self._num_proj is None else self._num_proj

    if self._state_is_tuple:
      (c_prev, m_prev) = state
    else:
      c_prev = tf.slice(state, [0, 0], [-1, self._num_units])
      m_prev = tf.slice(state, [0, self._num_units], [-1, num_proj])

    dtype = inputs.dtype
    input_size = inputs.get_shape().with_rank(2)[1]
    if input_size.value is None:
      raise ValueError("Could not infer input size from inputs.get_shape()[-1]")
    with tf.compat.v1.variable_scope(scope or type(self).__name__,
                           initializer=self._initializer):  # "LSTMCell"
      w_h = tf.compat.v1.get_variable("W_h", [num_proj, 4 * self._num_units],
                            dtype=tf.float32)
      w_x = tf.compat.v1.get_variable("W_x", [input_size.value, 4 * self._num_units],
                            dtype=tf.float32)

      b = tf.compat.v1.get_variable(
          "B", shape=[4 * self._num_units],
          initializer=tf.compat.v1.zeros_initializer, dtype=dtype)

      # i = input_gate, j = new_input, f = forget_gate, o = output_gate
      hidden_matrix = tf.matmul(m_prev, w_h)
      bn_hidden_matrix = tf.compat.v1.layers.batch_normalization(hidden_matrix, 
        momentum=0.99,
        beta_initializer=tf.compat.v1.constant_initializer(self._beta_h), 
        gamma_initializer=tf.compat.v1.constant_initializer(self._gamma_h), 
        training=(not self.forward_only),
        name='bn_hidden_matrix', reuse=None)
      input_matrix = tf.matmul(inputs, w_x)
      bn_input_matrix = tf.compat.v1.layers.batch_normalization(input_matrix, 
        momentum=0.99,
        beta_initializer=tf.compat.v1.constant_initializer(self._beta_x), 
        gamma_initializer=tf.compat.v1.constant_initializer(self._gamma_x), 
        training=(not self.forward_only), 
        name='bn_input_matrix', reuse=None)
      lstm_matrix = tf.nn.bias_add(
          tf.add(bn_input_matrix, bn_hidden_matrix), b)
      i, j, f, o = tf.split(lstm_matrix, num_or_size_splits=4, axis=1)

      # Diagonal connections
      if self._use_peepholes:
        w_f_diag = tf.compat.v1.get_variable(
            "W_F_diag", shape=[self._num_units], dtype=dtype)
        w_i_diag = tf.compat.v1.get_variable(
            "W_I_diag", shape=[self._num_units], dtype=dtype)
        w_o_diag = tf.compat.v1.get_variable(
            "W_O_diag", shape=[self._num_units], dtype=dtype)

      if self._use_peepholes:
        c = (tf.sigmoid(f + self._forget_bias + w_f_diag * c_prev) * c_prev +
             tf.sigmoid(i + w_i_diag * c_prev) * self._activation(j))
      else:
        c = (tf.sigmoid(f + self._forget_bias) * c_prev + tf.sigmoid(i) *
             self._activation(j))

      if self._cell_clip is not None:
        # pylint: disable=invalid-unary-operand-type
        c = tf.clip_by_value(c, -self._cell_clip, self._cell_clip)
        # pylint: enable=invalid-unary-operand-type

      bn_c = tf.compat.v1.layers.batch_normalization(c, 
        momentum=0.99,
        beta_initializer=tf.compat.v1.constant_initializer(self._beta_c),
        gamma_initializer=tf.compat.v1.constant_initializer(self._gamma_c), 
        training=(not self.forward_only), 
        name='bn_cell', reuse=None)
      if self._use_peepholes:
        m = tf.sigmoid(o + w_o_diag * bn_c) * self._activation(bn_c)
      else:
        m = tf.sigmoid(o) * self._activation(bn_c)

      if self._num_proj is not None:
        concat_w_proj = tf.nn.rnn_cell._get_concat_variable(
            "W_P", [self._num_units, self._num_proj],
            dtype, self._num_proj_shards)

        m = tf.matmul(m, concat_w_proj)

    new_state = (tf.compat.v1.nn.rnn_cell.LSTMStateTuple(c, m) if self._state_is_tuple
                 else tf.concat(1, [c, m]))
    return m, new_state


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

  if not isinstance(cell, tf.compat.v1.nn.rnn_cell.RNNCell):
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
  with tf.compat.v1.variable_scope(scope or "RNN") as varscope:
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
      batch_size = tf.shape(input=inputs[0])[0]
    if initial_state is not None:
      state = initial_state
    else:
      if not dtype:
        raise ValueError("If no initial_state is provided, "
                           "dtype must be specified")
      state = cell.zero_state(batch_size, dtype)

    if sequence_length is not None:  # Prepare variables
      sequence_length = tf.cast(sequence_length, dtype=tf.int32)
      zero_output = tf.zeros(
          tf.stack([batch_size, cell.output_size]), inputs[0].dtype)
      zero_output.set_shape(
          tf.tensor_shape.TensorShape([fixed_batch_size.value,
                                       cell.output_size]))
      min_sequence_length = tf.reduce_min(input_tensor=sequence_length)
      max_sequence_length = tf.reduce_max(input_tensor=sequence_length)

    for time, input_ in enumerate(inputs):
      if time > 0: varscope.reuse_variables()
      # pylint: disable=cell-var-from-loop
      call_cell = lambda: cell(input_, state)
      # pylint: enable=cell-var-from-loop
      if sequence_length is not None:
        (output, state) = tf.nn.rnn._rnn_step(
            time=time, sequence_length=sequence_length,
            min_sequence_length=min_sequence_length,
            max_sequence_length=max_sequence_length,
            zero_output=zero_output, state=state,
            call_cell=call_cell, state_size=cell.state_size)
      else:
        (output, state) = call_cell()

      outputs.append(output)
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
    A tuple (outputs, output_states) where:
      outputs is a length `T` list of outputs (one for each input), which
        are depth-concatenated forward and backward outputs.
      output_states is a length `T` list of hidden states (one for each step),
        which are depth-concatenated forward and backward states.

  Raises:
    TypeError: If `cell_fw` or `cell_bw` is not an instance of `RNNCell`.
    ValueError: If inputs is None or an empty list.
  """

  if not isinstance(cell_fw, tf.compat.v1.nn.rnn_cell.RNNCell):
    raise TypeError("cell_fw must be an instance of RNNCell")
  if not isinstance(cell_bw, tf.compat.v1.nn.rnn_cell.RNNCell):
    raise TypeError("cell_bw must be an instance of RNNCell")
  if not isinstance(inputs, list):
    raise TypeError("inputs must be a list")
  if not inputs:
    raise ValueError("inputs must not be empty")

  name = scope or "BiRNN"
  # Forward direction
  with tf.compat.v1.variable_scope(name + "_FW") as fw_scope:
    output_fw, states_fw = RNNModel(cell_fw, inputs, initial_state_fw,
      dtype, sequence_length, num_cell_layers=num_cell_layers, scope=fw_scope)

  # Backward direction
  with tf.compat.v1.variable_scope(name + "_BW") as bw_scope:
    tmp, tmp_states = RNNModel(cell_bw, _reverse_seq(inputs, sequence_length),
      initial_state_bw, dtype, sequence_length,
      num_cell_layers=num_cell_layers, scope=bw_scope)
  output_bw = _reverse_seq(tmp, sequence_length)
  states_bw = _reverse_seq(tmp_states, sequence_length)

  # Concat each of the forward/backward outputs
  outputs = [tf.concat(axis=1, values=[fw, bw]) for fw, bw in zip(output_fw, output_bw)]

  # Notice that the computation of the encoder final state uses the final state
  # of the backward RNN without reverse!!!
  if nest.is_sequence(cell_fw.state_size):
    output_states = [nest_map_dual(lambda x, y: tf.concat(axis=1, values=[x, y]), fw, bw)
                     for fw, bw in zip(states_fw, tmp_states)]
  else:
    if num_cell_layers > 1:
      output_states = []
      for fw, bw in zip(states_fw, tmp_states):
        output_states.append(tf.concat(axis=1, values=[tf.concat(axis=1, values=[l_fw, l_bw])
          for l_fw, l_bw in zip(tf.split(axis=1, num_or_size_splits=num_cell_layers, value=fw),
            tf.split(axis=1, num_or_size_splits=num_cell_layers, value=bw))]))
    else:
      output_states = [tf.concat(axis=1, values=[fw, bw])
                       for fw, bw in zip(states_fw, tmp_states)]

  return (outputs, output_states)


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
  s_joined = tf.stack(input_seq)

  # TODO(schuster, ebrevdo): Remove cast when reverse_sequence takes int32
  if lengths is not None:
    lengths = tf.cast(lengths, dtype=tf.int64)

  # Reverse along dimension 0
  s_reversed = tf.reverse_sequence(input=s_joined, seq_lengths=lengths, seq_axis=0, batch_axis=1)
  # Split again into list
  result = tf.unstack(s_reversed)
  for r in result:
    r.set_shape(input_shape)
  return result

# --- Tensorflow v1.2 tensorflow/python/ops/rnn_cell_impl.py --- #

def linear(args,
            output_size,
            bias,
            bias_initializer=None,
            kernel_initializer=None):
  """Linear map: sum_i(args[i] * W[i]), where W[i] is a variable.
  Args:
    args: a 2D Tensor or a list of 2D, batch x n, Tensors.
    output_size: int, second dimension of W[i].
    bias: boolean, whether to add a bias term or not.
    bias_initializer: starting value to initialize the bias
      (default is all zeros).
    kernel_initializer: starting value to initialize the weight.
  Returns:
    A 2D Tensor with shape [batch x output_size] equal to
    sum_i(args[i] * W[i]), where W[i]s are newly created matrices.
  Raises:
    ValueError: if some of the arguments has unspecified or wrong shape.
  """
  if args is None or (nest.is_sequence(args) and not args):
    raise ValueError("`args` must be specified")
  if not nest.is_sequence(args):
    args = [args]

  # Calculate the total size of arguments on dimension 1.
  total_arg_size = 0
  shapes = [a.get_shape() for a in args]
  for shape in shapes:
    if shape.ndims != 2:
      raise ValueError("linear is expecting 2D arguments: %s" % shapes)
    if shape[1].value is None:
      raise ValueError("linear expects shape[1] to be provided for shape %s, "
                       "but saw %s" % (shape, shape[1]))
    else:
      total_arg_size += shape[1].value

  dtype = [a.dtype for a in args][0]

  # Now the computation.
  scope = tf.compat.v1.get_variable_scope()
  with tf.compat.v1.variable_scope(scope) as outer_scope:
    weights = tf.compat.v1.get_variable(
        "bias", [total_arg_size, output_size],
        dtype=dtype,
        initializer=kernel_initializer)
    if len(args) == 1:
      res = tf.matmul(args[0], weights)
    else:
      res = tf.matmul(tf.concat(args, 1), weights)
    if not bias:
      return res
    with tf.compat.v1.variable_scope(outer_scope) as inner_scope:
      inner_scope.set_partitioner(None)
      if bias_initializer is None:
        bias_initializer = tf.compat.v1.constant_initializer(0.0, dtype=dtype)
      biases = tf.compat.v1.get_variable(
          "kernel", [output_size],
          dtype=dtype,
          initializer=bias_initializer)
    return tf.nn.bias_add(res, biases)


class RANCell(tf.compat.v1.nn.rnn_cell.RNNCell):
  """[Experimental] Recurrent Additive Network cell
     (cf. http://www.kentonl.com/pub/llz.2017.pdf)."""

  def __init__(self, num_units, bias=1.0, input_size=None, activation=tf.tanh):
    if input_size is not None:
      print("%s: The input_size parameter is deprecated." % self)
    self._num_units = num_units
    self.bias = bias
    self._activation = activation

  @property
  def state_size(self):
    return self._num_units

  @property
  def output_size(self):
    return self._num_units

  def __call__(self, inputs, state, scope=None):
    """Recurrent Additive Network (RAN) with nunits cells."""
    with tf.compat.v1.variable_scope(scope or type(self).__name__):  # "RANCell"
      with tf.compat.v1.variable_scope("Input_projection"):
        c_tilde = linear(inputs, self._num_units, True)
      with tf.compat.v1.variable_scope("Gates"):  # input gate and forget gate.
        i, f = tf.split(axis=1, num_or_size_splits=2,
            value=linear([inputs, state], 2 * self._num_units, True, self.bias))
        i, f = tf.sigmoid(i), tf.sigmoid(f)
      with tf.compat.v1.variable_scope("Context"):
        new_c = self._activation(i * c_tilde + f * state)
    return new_c, new_c
