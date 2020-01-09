"""Utility functions related to graph construction."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os

import tensorflow as tf
from tensorflow.python.util import nest

import src.utils as utils


def define_model(FLAGS, session, model_constructor, buckets, forward_only):
    params = collections.defaultdict()

    params["source_vocab_size"] = FLAGS.nl_vocab_size
    params["target_vocab_size"] = FLAGS.cm_vocab_size
    params["max_source_length"] = FLAGS.max_nl_seq_len
    params["max_target_length"] = FLAGS.max_cm_seq_len
    params["max_source_token_size"] = FLAGS.max_nl_token_size
    params["max_target_token_size"] = FLAGS.max_cm_token_size
    params["rnn_cell"] = FLAGS.rnn_cell
    params["batch_size"] = FLAGS.batch_size
    params["num_layers"] = FLAGS.num_layers
    params["num_samples"] = FLAGS.num_samples
    params["max_gradient_norm"] = FLAGS.max_gradient_norm
    params["variational_recurrent_dropout"] = \
        FLAGS.variational_recurrent_dropout

    params["recurrent_batch_normalization"] = \
        FLAGS.recurrent_batch_normalization
    params["gramma_c"] = FLAGS.gamma_c
    params["beta_c"] = FLAGS.beta_c
    params["gramma_h"] = FLAGS.gamma_h
    params["beta_h"] = FLAGS.beta_h
    params["gramma_x"] = FLAGS.gamma_x
    params["beta_x"] = FLAGS.beta_x

    params["cm_token_use_attention"] = FLAGS.cm_token_use_attention

    params["nl_token"] = FLAGS.nl_token
    params["nl_token_dim"] = FLAGS.nl_token_dim
    params["sc_char"] = FLAGS.sc_char
    # params["sc_char_vocab_size"] = FLAGS.sc_char_vocab_size
    # params["sc_char_dim"] = FLAGS.sc_char_dim
    # params["sc_char_composition"] = FLAGS.sc_char_composition
    # params["sc_char_rnn_cell"] = FLAGS.sc_char_rnn_cell
    # params["sc_char_rnn_num_layers"] = FLAGS.sc_char_rnn_num_layers
    # params["nl_token_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.token.feature.npy".format(source))
    # params["sc_char_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.char.feature.npy".format(source))

    params["cm_token"] = FLAGS.cm_token
    params["tg_char"] = FLAGS.tg_char
    # params["tg_char_vocab_size"] = FLAGS.tg_char_vocab_size
    # params["tg_char_composition"] = FLAGS.tg_char_composition
    # params["tg_char_use_attention"] = FLAGS.tg_char_use_attention
    # params["tg_char_rnn_cell"] = FLAGS.tg_char_rnn_cell
    # params["tg_char_rnn_num_layers"] = FLAGS.tg_char_rnn_num_layers
    # params["tg_char_rnn_input_keep"] = FLAGS.tg_char_rnn_input_keep
    # params["tg_char_rnn_output_keep"] = FLAGS.tg_char_rnn_output_keep
    # params["cm_token_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.token.feature.npy".format(target))
    # params["tg_char_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.char.feature.npy".format(target))

    params["gamma"] = FLAGS.gamma

    params["optimizer"] = FLAGS.optimizer
    params["learning_rate"] = FLAGS.learning_rate
    params["learning_rate_decay_factor"] = FLAGS.learning_rate_decay_factor
    params["adam_epsilon"] = FLAGS.adam_epsilon

    params["steps_per_epoch"] = FLAGS.steps_per_epoch
    params["num_epochs"] = FLAGS.num_epochs

    params["training_algorithm"] = FLAGS.training_algorithm
    if FLAGS.training_algorithm == "bso":
        assert(FLAGS.token_decoding_algorithm == "beam_search")
    params["margin"] = FLAGS.margin

    params["use_copy"] = FLAGS.use_copy
    params["copy_fun"] = FLAGS.copy_fun
    params["chi"] = FLAGS.chi

    params["cm_token_attn_fun"] = FLAGS.cm_token_attn_fun
    params["beta"] = FLAGS.beta

    params["encoder_topology"] = FLAGS.encoder_topology
    params["decoder_topology"] = FLAGS.decoder_topology

    params["sc_input_keep"] = FLAGS.sc_input_keep
    params["sc_output_keep"] = FLAGS.sc_output_keep
    params["tg_input_keep"] = FLAGS.tg_input_keep
    params["tg_output_keep"] = FLAGS.tg_output_keep
    params["attention_input_keep"] = FLAGS.attention_input_keep
    params["attention_output_keep"] = FLAGS.attention_output_keep

    params["token_decoding_algorithm"] = FLAGS.token_decoding_algorithm
    params["char_decoding_algorithm"] = FLAGS.char_decoding_algorithm
    params["beam_size"] = FLAGS.beam_size
    params["alpha"] = FLAGS.alpha
    params["top_k"] = FLAGS.top_k

    params["forward_only"] = forward_only
    params["force_reading_input"] = FLAGS.force_reading_input

    # construct model directory
    model_subdir, decode_sig = utils.get_decode_signature(FLAGS)
    FLAGS.model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    params["model_dir"] = FLAGS.model_dir
    params["decode_sig"] = decode_sig
    print("model_dir={}".format(FLAGS.model_dir))
    print("decode_sig={}".format(decode_sig))

    if forward_only:
        # Set batch_size to 1 for decoding.
        params["batch_size"] = 1
        # Reset dropout probabilities for decoding.
        params["attention_input_keep"] = 1.0
        params["attention_output_keep"] = 1.0
        params["sc_input_keep"] = 1.0
        params["sc_output_keep"] = 1.0
        params["tg_input_keep"] = 1.0
        params["tg_output_keep"] = 1.0

    if FLAGS.gen_slot_filling_training_data:
        FLAGS.batch_size = 1
        params["batch_size"] = 1
        FLAGS.beam_size = 1
        params["beam_size"] = 1
        FLAGS.learning_rate = 0
        params["learning_rate"] = 0
        params["force_reading_input"] = True
        params["create_fresh_params"] = False

    if FLAGS.explain:
        FLAGS.grammatical_only = False

    model = model_constructor(params, buckets)
    if forward_only or FLAGS.gen_slot_filling_training_data or \
            not FLAGS.create_fresh_params:
        ckpt = tf.train.get_checkpoint_state(
            os.path.join(FLAGS.model_root_dir, FLAGS.model_dir))
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        if not os.path.exists(FLAGS.model_dir):
            print("Making model_dir...")
            os.mkdir(FLAGS.model_dir)
        # else:
        #     clean_dir(FLAGS.model_dir)
        if FLAGS.pretrained_model_subdir:
            # load pre-trained parameteres for advanced training algorithms
            pretrain_dir = os.path.join(
                FLAGS.model_root_dir, FLAGS.pretrained_model_subdir)
            print("Initialize the graph with pre-trained parameters from {}"
                  .format(pretrain_dir))
            pretrain_ckpt = tf.train.get_checkpoint_state(pretrain_dir)
            model.saver.restore(session, pretrain_ckpt.model_checkpoint_path)
            session.run(model.learning_rate.assign(
                tf.constant(FLAGS.learning_rate)))
        else:
            print("Initialize the graph with random parameters.")
            session.run(tf.compat.v1.global_variables_initializer())

    return model


def softmax_loss(output_project, num_samples, target_vocab_size):
    w, b = output_project
    if num_samples > 0 and num_samples < target_vocab_size:
        print("loss function = sampled_softmax_loss ({})".format(num_samples))
        w_t = tf.transpose(a=w)
        def sampled_loss(outputs, labels):
            labels = tf.reshape(labels, [-1, 1])
            return tf.nn.sampled_softmax_loss(
                w_t, b, labels, outputs, num_samples, target_vocab_size)
        loss_function = sampled_loss
    else:
        print("loss function = softmax_loss")
        def loss(outputs, labels):
            logits = tf.matmul(outputs, w) + b
            return tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=logits, labels=labels)
        loss_function = loss
    return loss_function


def wrap_inputs(beam_decoder, inputs):
    return [beam_decoder.wrap_input(input) for input in inputs]


def sparse_cross_entropy(logits, targets):
    return -tf.reduce_sum(input_tensor=logits * tf.one_hot(targets, logits.get_shape()[1]), axis=1)


def nest_map(func, nested):
    """
    Apply function to each element in a nested list.

    :param func: The function to apply.
    :param nested: The nested list to which the function is going to be applied.

    :return: A list with the same structue as nested where the each element
        is the output of applying func to the corresponding element in nest.
    """
    if not nest.is_sequence(nested):
        return func(nested)
    flat = nest.flatten(nested)
    return nest.pack_sequence_as(nested, list(map(func, flat)))


def nest_map_dual(func, nested1, nested2):
    if not nest.is_sequence(nested1):
        return func(nested1, nested2)
    flat1 = nest.flatten(nested1)
    flat2 = nest.flatten(nested2)
    output = [func(x, y) for x, y in zip(flat1, flat2)]
    return nest.pack_sequence_as(nested1, list(output))


def create_multilayer_cell(rnn_cell, scope, dim, num_layers, input_keep_prob=1,
                           output_keep_prob=1, variational_recurrent=True, input_dim=-1):
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
            cell = tf.compat.v1.nn.rnn_cell.LSTMCell(dim, state_is_tuple=True)
        elif rnn_cell == "gru":
            cell = tf.compat.v1.nn.rnn_cell.GRUCell(dim)
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
    output_fw, states_fw = RNNModel(cell_fw, inputs, initial_state_fw, dtype,
                                    sequence_length, scope=fw_scope)

  # Backward direction
  with tf.compat.v1.variable_scope(name + "_BW") as bw_scope:
    tmp, tmp_states = RNNModel(cell_bw, _reverse_seq(inputs, sequence_length),
      initial_state_bw, dtype, sequence_length, scope=bw_scope)
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


def RNNModel(cell, inputs, initial_state=None, dtype=None, sequence_length=None, scope=None):
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
      if input_size is None:
        raise ValueError(
            "Input size (second dimension of inputs[0]) must be accessible via "
            "shape inference, but saw value None.")
    else:
      fixed_batch_size = inputs[0].get_shape().with_rank_at_least(1)[0]

    if fixed_batch_size:
      batch_size = fixed_batch_size
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
    if shape[1] is None:
      raise ValueError("linear expects shape[1] to be provided for shape %s, "
                       "but saw %s" % (shape, shape[1]))
    else:
      total_arg_size += shape[1]

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


class NNModel(object):
    def __init__(self, hyperparams, buckets=None):
        self.hyperparams = hyperparams
        self.buckets = buckets

    # --- model architecture hyperparameters --- #

    @property
    def encoder_topology(self):
        return self.hyperparams["encoder_topology"]

    @property
    def decoder_topology(self):
        return self.hyperparams["decoder_topology"]

    @property
    def num_layers(self):
        return self.hyperparams["num_layers"]

    # --- training algorithm hyperparameters --- #

    @property
    def training_algorithm(self):
        return self.hyperparams["training_algorithm"]

    @property
    def use_sampled_softmax(self):
        return self.num_samples > 0 and \
               self.num_samples < self.target_vocab_size

    @property
    def num_samples(self):
        return self.hyperparams["num_samples"]

    @property
    def batch_size(self):
        return self.hyperparams["batch_size"]

    @property
    def num_epochs(self):
        return self.hyperparams["num_epochs"]

    @property
    def steps_per_epoch(self):
        return self.hyperparams["steps_per_epoch"]

    @property
    def max_gradient_norm(self):
        return self.hyperparams["max_gradient_norm"]

    @property
    def optimizer(self):
        return self.hyperparams["optimizer"]

    @property
    def margin(self):
        return self.hyperparams["margin"]

    @property
    def adam_epsilon(self):
        return self.hyperparams["adam_epsilon"]

    @property
    def cm_token_use_attention(self):
        return self.hyperparams["cm_token_use_attention"]

    @property
    def cm_token_attn_fun(self):
        return self.hyperparams["cm_token_attn_fun"]

    @property
    def variational_recurrent_dropout(self):
        return self.hyperparams["variational_recurrent_dropout"]

    @property
    def attention_input_keep(self):
        return self.hyperparams["attention_input_keep"]

    @property
    def attention_output_keep(self):
        return self.hyperparams["attention_output_keep"]

    @property
    def rnn_cell(self):
        return self.hyperparams["rnn_cell"]

    @property
    def gamma_c(self):
        return self.hyperparams["gamma_c"]

    @property
    def beta_c(self):
        return self.hyperparams["beta_c"]

    @property
    def gamma_h(self):
        return self.hyperparams["gamma_h"]

    @property
    def beta_h(self):
        return self.hyperparams["beta_h"]

    @property
    def gamma_x(self):
        return self.hyperparams["gamma_x"]

    @property
    def beta_x(self):
        return self.hyperparams["beta_x"]


    @property
    def source_vocab_size(self):
        return self.hyperparams["source_vocab_size"]

    @property
    def target_vocab_size(self):
        return self.hyperparams["target_vocab_size"]

    @property
    def max_source_length(self):
        return self.hyperparams["max_source_length"]

    @property
    def max_target_length(self):
        return self.hyperparams["max_target_length"]

    @property
    def max_source_token_size(self):
        return self.hyperparams["max_source_token_size"]

    @property
    def max_target_token_size(self):
        return self.hyperparams["max_target_token_size"]

    @property
    def decode_sig(self):
        return self.hyperparams["decode_sig"]

    @property
    def model_dir(self):
        return self.hyperparams["model_dir"]

    @property
    def nl_token(self):
        return self.hyperparams["nl_token"]

    @property
    def nl_token_dim(self):
        """
        Source token channel embedding dimension.
        """
        return self.hyperparams["nl_token_dim"]

    @property
    def sc_input_keep(self):
        return self.hyperparams["sc_input_keep"]

    @property
    def sc_output_keep(self):
        return self.hyperparams["sc_output_keep"]

    @property
    def nl_token_features_path(self):
        return self.hyperparams["nl_token_features_path"]

    @property
    def sc_char(self):
        return self.hyperparams["sc_char"]

    @property
    def sc_char_vocab_size(self):
        return self.hyperparams["sc_char_vocab_size"]

    @property
    def sc_char_dim(self):
        """
        Source character channel embedding dimension.
        """
        return self.hyperparams["sc_char_dim"]

    @property
    def sc_char_composition(self):
        return self.hyperparams["sc_char_composition"]

    @property
    def sc_char_rnn_cell(self):
        return self.hyperparams["sc_char_rnn_cell"]

    @property
    def sc_char_rnn_num_layers(self):
        return self.hyperparams["sc_char_rnn_num_layers"]

    @property
    def sc_char_features_path(self):
        return self.hyperparams["sc_char_features_path"]

    @property
    def tg_input_keep(self):
        return self.hyperparams["tg_input_keep"]

    @property
    def tg_output_keep(self):
        return self.hyperparams["tg_output_keep"]

    @property
    def cm_token_features_path(self):
        return self.hyperparams["cm_token_features_path"]

    @property
    def tg_char(self):
        return self.hyperparams["tg_char"]

    @property
    def tg_char_vocab_size(self):
        return self.hyperparams["tg_char_vocab_size"]

    @property
    def tg_char_composition(self):
        return self.hyperparams["tg_char_composition"]

    @property
    def tg_char_rnn_cell(self):
        return self.hyperparams["tg_char_rnn_cell"]

    @property
    def tg_char_use_attention(self):
        return self.hyperparams["tg_char_use_attention"]

    @property
    def tg_char_rnn_num_layers(self):
        return self.hyperparams["tg_char_rnn_num_layers"]

    @property
    def tg_char_features_path(self):
        return self.hyperparams["tg_char_features_path"]

    @property
    def tg_char_rnn_input_keep(self):
        return self.hyperparams["tg_char_rnn_input_keep"]

    @property
    def tg_char_rnn_output_keep(self):
        return self.hyperparams["tg_char_rnn_output_keep"]

    @property
    def gamma(self):
        return self.hyperparams["gamma"]

    # -- copy mechanism -- #

    @property
    def use_copy(self):
        return self.hyperparams["use_copy"]

    @property
    def copy_fun(self):
        return self.hyperparams["copy_fun"]

    @property
    def copynet(self):
        return self.use_copy and self.copy_fun == 'copynet'

    @property
    def copy_vocab_size(self):
        return self.hyperparams["copy_vocab_size"]

    @property
    def chi(self):
        return self.hyperparams["chi"]

    # --- decoding algorithm hyperparameters --- #

    @property
    def forward_only(self):
        # If set, we do not construct the backward pass in the model.
        return self.hyperparams["forward_only"]

    @property
    def token_decoding_algorithm(self):
        return self.hyperparams["token_decoding_algorithm"]

    @property
    def char_decoding_algorithm(self):
        return self.hyperparams["char_decoding_algorithm"]

    @property
    def beam_size(self):
        return self.hyperparams["beam_size"]

    @property
    def beam_order(self):
        return self.hyperparams["beam_order"]

    @property
    def alpha(self):
        return self.hyperparams["alpha"]

    @property
    def beta(self):
        return self.hyperparams["beta"]

    @property
    def top_k(self):
        return self.hyperparams["top_k"]

    @property
    def force_reading_input(self):
        return self.hyperparams["force_reading_input"]


class InfPerplexityError(Exception):
    pass