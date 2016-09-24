"""Utility functions related to graph construction."""

import collections
import functools
import os
import warnings

import tensorflow as tf

import data_utils

def create_model(session, FLAGS, model_constructor, buckets, forward_only,
                 construct_model_dir=True):
    params = collections.defaultdict()
    params["source_vocab_size"] = FLAGS.nl_vocab_size
    params["target_vocab_size"] = FLAGS.cm_vocab_size
    params["max_source_length"] = FLAGS.max_nl_length \
        if not buckets else buckets[-1][0]
    params["max_target_length"] = FLAGS.max_cm_length \
        if not buckets else buckets[-1][1]
    params["dim"] = FLAGS.dim
    params["rnn_cell"] = FLAGS.rnn_cell
    params["num_layers"] = FLAGS.num_layers
    params["max_gradient_norm"] = FLAGS.max_gradient_norm
    params["batch_size"] = FLAGS.batch_size
    params["num_samples"] = FLAGS.num_samples
    params["encoder_input_keep"] = FLAGS.encoder_input_keep
    params["encoder_output_keep"] = FLAGS.encoder_output_keep
    params["decoder_input_keep"] = FLAGS.decoder_input_keep
    params["decoder_output_keep"] = FLAGS.decoder_output_keep
    params["optimizer"] = FLAGS.optimizer
    params["learning_rate"] = FLAGS.learning_rate
    params["learning_rate_decay_factor"] = FLAGS.learning_rate_decay_factor
    params["use_attention"] = FLAGS.use_attention
    params["use_copy"] = FLAGS.use_copy

    params["encoder_topology"] = FLAGS.encoder_topology
    params["decoder_topology"] = FLAGS.decoder_topology

    params["decoding_algorithm"] = FLAGS.decoding_algorithm
    params["beam_size"] = FLAGS.beam_size
    params["top_k"] = FLAGS.top_k

    # construct model directory
    if construct_model_dir:
        model_dir = os.path.join(FLAGS.train_dir, FLAGS.encoder_topology)
        model_dir += '-{}'.format(FLAGS.rnn_cell)
        if FLAGS.use_attention:
            model_dir += '-attention'
        model_dir += '-{}'.format(FLAGS.batch_size)
        model_dir += '-{}'.format(FLAGS.encoder_input_keep)
        model_dir += '-{}'.format(FLAGS.encoder_output_keep)
        model_dir += '-{}'.format(FLAGS.decoder_input_keep)
        model_dir += '-{}'.format(FLAGS.decoder_output_keep)
        setattr(FLAGS, "train_dir", model_dir)
    else:
        if FLAGS.train_dir.endswith('/'):
            model_dir = FLAGS.train_dir[:-1].split('/')[-1]
        else:
            model_dir = FLAGS.train_dir.split('/')[-1]
    params["model_dir"] = model_dir

    if forward_only:
        params["batch_size"] = 1
        params["encoder_input_keep"] = 1.0
        params["encoder_output_keep"] = 1.0
        params["decoder_input_keep"] = 1.0
        params["decoder_output_keep"] = 1.0

    model = model_constructor(params, buckets, forward_only)

    ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
    global_epochs = int(ckpt.model_checkpoint_path.rsplit('-')[-1]) if ckpt else 0

    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path):
        if not forward_only and FLAGS.create_fresh_params:
            data_utils.clean_dir(FLAGS.train_dir)
            print("Created model with fresh parameters.")
            global_epochs = 0
            session.run(tf.initialize_all_variables())
        else:
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        if not os.path.exists(FLAGS.train_dir):
            print("Making train dir {}".format(FLAGS.train_dir))
            os.mkdir(FLAGS.train_dir)
        print("Created model with fresh parameters.")
        session.run(tf.initialize_all_variables())

    return model, global_epochs


def create_multilayer_cell(type, scope, dim, num_layers, input_keep_prob=1, output_keep_prob=1):
    """
    Create the multi-layer RNN cell.
    :param type: Type of RNN cell.
    :param scope: Variable scope.
    :param dim: Dimension of hidden layers.
    :param num_layers: Number of layers of cells.
    :param input_keep_prob: Proportion of input to keep in dropout.
    :param output_keep_prob: Proportion of output to keep in dropout.
    :return: RNN cell as specified.
    """
    with tf.variable_scope(scope):
        if type == "lstm":
            cell = tf.nn.rnn_cell.BasicLSTMCell(dim, state_is_tuple=True)
        elif type == "gru":
            cell = tf.nn.rnn_cell.GRUCell(dim)
        else:
            raise ValueError("Unrecognized RNN cell type: {}.".format(type))

        if num_layers > 1:
            cell = tf.nn.rnn_cell.MultiRNNCell([cell] * num_layers,
                                               state_is_tuple = (type == "lstm"))

        assert(input_keep_prob >= 0 and output_keep_prob >= 0)
        if input_keep_prob < 1 or output_keep_prob < 1:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=input_keep_prob,
                                                 output_keep_prob=output_keep_prob)
    return cell


def switch_mask(mask, candidates):
    """
    :param mask: A 2D binary matrix of size [batch_size, num_options].
                 Each row of mask has exactly one non-zero entry.
    :param candidates: A list of 2D matrices with length num_options.
    :return: selections concatenated as a new batch.
    """
    assert(len(candidates) > 1)
    threed_mask = tf.tile(tf.expand_dims(mask, 2),
                          [1, 1, candidates[0].get_shape()[1].value])
    threed_mask = tf.cast(threed_mask, candidates[0].dtype)
    expanded_candidates = [tf.expand_dims(c, 1) for c in candidates]
    candidate = tf.concat(1, expanded_candidates)
    return tf.reduce_sum(tf.mul(threed_mask, candidate), 1)


def map_fn(fn, elems, batch_size):
    """Pesudo multi-ariti scan."""
    results = []
    elem_lists = [tf.split(0, batch_size, elem) for elem in elems]
    for i in xrange(batch_size):
        args = [tf.squeeze(elem_lists[0][i], squeeze_dims=[0])] + \
               [elem_list[i] for elem_list in elem_lists[1:]]
        results.append(fn(args))
    _results = tf.concat(0, results)
    return _results


def sequence_loss(logits, targets, target_weights, loss_function):
    targets = targets[:len(logits)]
    weights = target_weights[:len(logits)]

    with tf.variable_scope("sequence_loss"):
        log_perp_list = []
        for logit, target, weight in zip(logits, targets, weights):
            crossent = loss_function(logit, target)
            log_perp_list.append(crossent * weight)
        log_perps = tf.add_n(log_perp_list)
        total_size = tf.add_n(weights)
        total_size += 1e-12  # Just to avoid division by 0 for all-0 weights.
        log_perps /= total_size

    batch_size = logits[0].get_shape()[0].value
    avg_log_perps = tf.reduce_sum(log_perps) / tf.cast(batch_size, dtype=tf.float32)

    return avg_log_perps


def softmax_loss(output_projection, num_samples, target_vocab_size):
    if num_samples > 0:
        w, b = output_projection
        w_t = tf.transpose(w)

        def sampled_loss(inputs, labels):
            labels = tf.reshape(labels, [-1, 1])
            return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels, num_samples,
                                              target_vocab_size)

        loss_function = sampled_loss
    else:
        loss_function = tf.nn.softmax_cross_entropy_with_logits
    return loss_function


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)     #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)    #reset filter
        return func(*args, **kwargs)

    return new_func
