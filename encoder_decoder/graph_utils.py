"""Utility functions related to graph construction."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import os, sys
import warnings
if sys.version_info > (3, 0):
    from six.moves import xrange

import tensorflow as tf

from encoder_decoder import data_utils


def create_model(session, FLAGS, model_constructor, buckets, forward_only,
                 construct_model_dir=True, construct_slot_filling=False):
    params = collections.defaultdict()
    params["source_vocab_size"] = FLAGS.sc_vocab_size
    params["target_vocab_size"] = FLAGS.tg_vocab_size
    params["max_source_length"] = FLAGS.max_sc_length \
        if not buckets else buckets[-1][0]
    params["max_target_length"] = FLAGS.max_tg_length \
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

    params["steps_per_epoch"] = FLAGS.steps_per_epoch
    params["num_epochs"] = FLAGS.num_epochs

    params["training_algorithm"] = FLAGS.training_algorithm
    if FLAGS.training_algorithm == "bso":
        assert(FLAGS.decoding_algorithm == "beam_search")
    params["margin"] = FLAGS.margin

    params["use_copy"] = FLAGS.use_copy

    params["use_attention"] = FLAGS.use_attention
    params["attention_input_keep"] = FLAGS.attention_input_keep
    params["attention_output_keep"] = FLAGS.attention_output_keep
    params["beta"] = FLAGS.beta

    params["encoder_topology"] = FLAGS.encoder_topology
    params["decoder_topology"] = FLAGS.decoder_topology

    params["decoding_algorithm"] = FLAGS.decoding_algorithm
    params["beam_size"] = FLAGS.beam_size
    params["alpha"] = FLAGS.alpha
    params["top_k"] = FLAGS.top_k

    params["force_reading_input"] = False

    # construct model directory
    model_subdir, model_sig = get_model_signature(FLAGS, construct_slot_filling)
    params["model_sig"] = model_sig

    model_root_dir = FLAGS.model_dir
    if construct_model_dir:
        setattr(FLAGS, "model_dir", os.path.join(FLAGS.model_dir, model_subdir))
    print("model_dir={}".format(FLAGS.model_dir))
    print("model_sig={}".format(model_sig))

    if forward_only:
        # In our experience using large batch size for decoding doesn't
        # significantly improve computing efficiency.
        FLAGS.batch_size = 1
        params["batch_size"] = 1
        params["attention_input_keep"] = 1.0
        params["attention_output_keep"] = 1.0
        params["encoder_input_keep"] = 1.0
        params["encoder_output_keep"] = 1.0
        params["decoder_input_keep"] = 1.0
        params["decoder_output_keep"] = 1.0

    if FLAGS.gen_slot_filling_training_data:
        FLAGS.batch_size = 1
        params["batch_size"] = 1
        FLAGS.beam_size = 1
        params["beam_size"] = 1
        FLAGS.learning_rate = 0
        params["learning_rate"] = 0
        params["force_reading_input"] = True

    if FLAGS.explain:
        FLAGS.grammatical_only = False

    model = model_constructor(params, buckets, forward_only)

    ckpt = tf.train.get_checkpoint_state(FLAGS.model_dir)
    global_epochs = int(ckpt.model_checkpoint_path.rsplit('-')[-1]) \
        if ckpt else 0

    if forward_only or not FLAGS.create_fresh_params:
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        if not os.path.exists(FLAGS.model_dir):
            print("Making model_dir...")
            os.mkdir(FLAGS.model_dir)
        else:
            data_utils.clean_dir(FLAGS.model_dir)
        if FLAGS.pretrained_model_subdir:
            # load pre-trained parameteres for advanced training algorithms
            pretrain_dir = os.path.join(model_root_dir, FLAGS.pretrained_model_subdir)
            print("Reading pre-trained model parameters from {}".format(pretrain_dir))
            pretrain_ckpt = tf.train.get_checkpoint_state(pretrain_dir)
            model.saver.restore(session, pretrain_ckpt.model_checkpoint_path)
            session.run(model.learning_rate.assign(tf.constant(FLAGS.learning_rate)))
        else:
            print("Created model with fresh parameters.")
            session.run(tf.initialize_all_variables())

    return model, global_epochs


def get_model_signature(FLAGS, construct_slot_filling=False):
    model_subdir = FLAGS.dataset
    if FLAGS.explain:
        model_subdir += '-expl'
    model_subdir += '-{}'.format(FLAGS.encoder_topology)
    model_subdir += '-{}'.format(FLAGS.rnn_cell)
    model_subdir += '-{}'.format(FLAGS.training_algorithm)
    if FLAGS.use_attention:
        model_subdir += '-attention'
        model_subdir += '-{}'.format(FLAGS.attention_input_keep)
        model_subdir += '-{}'.format(FLAGS.attention_output_keep)
        model_subdir += '-{}'.format(FLAGS.beta)
    model_subdir += '-{}'.format(FLAGS.batch_size)
    model_subdir += '-{}'.format(FLAGS.dim)
    model_subdir += '-{}'.format(FLAGS.num_layers)
    model_subdir += '-{}'.format(FLAGS.learning_rate)
    model_subdir += '-{}'.format(FLAGS.encoder_input_keep)
    model_subdir += '-{}'.format(FLAGS.encoder_output_keep)
    model_subdir += '-{}'.format(FLAGS.decoder_input_keep)
    model_subdir += '-{}'.format(FLAGS.decoder_output_keep)
    if FLAGS.canonical:
        model_subdir += '.canonical'
    elif FLAGS.normalized:
        model_subdir += '.normalized'
    if construct_slot_filling:
        model_subdir += '.slot.filler'

    model_sig = model_subdir + "-{}".format(FLAGS.decoding_algorithm)
    if FLAGS.decoding_algorithm == 'beam_search': 
        model_sig += "-{}".format(FLAGS.beam_size)
    model_sig += ("-test" if FLAGS.test else "-dev")
    return model_subdir, model_sig


def create_multilayer_cell(type, scope, dim, num_layers, input_keep_prob=1,
                           output_keep_prob=1):
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
            cell = tf.nn.rnn_cell.LSTMCell(dim, state_is_tuple=True)
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


def get_buckets(FLAGS):
    # We use a number of buckets and pad to the closest one for efficiency.
    if FLAGS.dataset.startswith("bash"):
        if FLAGS.decoder_topology in ['basic_tree']:
            buckets = [(30, 72)] if not FLAGS.explain else [(72, 30)]
        elif FLAGS.decoder_topology in ['rnn']:
            buckets = [(30, 40)] if not FLAGS.explain else [(40, 30)]
    elif FLAGS.dataset == "dummy":
        buckets = [(20, 95), (30, 95), (45, 95)] if not FLAGS.explain else \
            [(95, 20), (95, 30), (95, 45)]
    elif FLAGS.dataset == "jobs":
        buckets = [(20, 45)] if not FLAGS.explain else [(45, 20)]
    elif FLAGS.dataset == "geo":
        buckets = [(20, 70)] if not FLAGS.explain else [(70, 20)]
    elif FLAGS.dataset == "atis":
        buckets = [(20, 95), (30, 95), (40, 95)] if not FLAGS.explain else \
            [(95, 20), (95, 30), (95, 40)]
    return buckets


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


def attention_reg(attn_masks):
    diff = tf.reduce_sum(attn_masks, 1) - 1
    return tf.reduce_mean(tf.square(diff))


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

    avg_log_perps = tf.reduce_mean(log_perps)

    return avg_log_perps


def softmax_loss(output_projection, num_samples, target_vocab_size):
    if num_samples > 0:
        w, b = output_projection
        w_t = tf.transpose(w)
        def sampled_loss(inputs, labels):
            labels = tf.reshape(labels, [-1, 1])
            return tf.nn.sampled_softmax_loss(w_t, b, inputs, labels,
                                              num_samples, target_vocab_size)
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


class NNModel(object):
    def __init__(self, hyperparams, buckets=None):
        self.hyperparams = hyperparams
        self.buckets = buckets
        # self.learning_rate = tf.Variable(float(hyperparams["learning_rate"]),
        #                                  trainable=False)
        # self.learning_rate_decay_op = self.learning_rate.assign(
        #     self.learning_rate * hyperparams["learning_rate_decay_factor"])

    @property
    def use_sampled_softmax(self):
        return self.num_samples > 0 and self.num_samples < self.target_vocab_size

    @property
    def use_attention(self):
        return self.hyperparams["use_attention"]

    @property
    def use_copy(self):
        return self.hyperparams["use_copy"]

    @property
    def encoder_topology(self):
        return self.hyperparams["encoder_topology"]

    @property
    def decoder_topology(self):
        return self.hyperparams["decoder_topology"]

    @property
    def dim(self):
        return self.hyperparams["dim"]

    @property
    def batch_size(self):
        return self.hyperparams["batch_size"]

    @property
    def attention_input_keep(self):
        return self.hyperparams["attention_input_keep"]

    @property
    def attention_output_keep(self):
        return self.hyperparams["attention_output_keep"]

    @property
    def encoder_input_keep(self):
        return self.hyperparams["encoder_input_keep"]

    @property
    def encoder_output_keep(self):
        return self.hyperparams["encoder_output_keep"]

    @property
    def decoder_input_keep(self):
        return self.hyperparams["decoder_input_keep"]

    @property
    def decoder_output_keep(self):
        return self.hyperparams["decoder_output_keep"]

    @property
    def rnn_cell(self):
        return self.hyperparams["rnn_cell"]

    @property
    def max_gradient_norm(self):
        return self.hyperparams["max_gradient_norm"]

    @property
    def num_samples(self):
        return self.hyperparams["num_samples"]

    @property
    def num_layers(self):
        return self.hyperparams["num_layers"]

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
    def training_algorithm(self):
        return self.hyperparams["training_algorithm"]

    @property
    def decoding_algorithm(self):
        return self.hyperparams["decoding_algorithm"]

    @property
    def optimizer(self):
        return self.hyperparams["optimizer"]

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
    def model_sig(self):
        return self.hyperparams["model_sig"]

    @property
    def margin(self):
        return self.hyperparams["margin"]

    # -- training parameters -- #

    @property
    def num_epochs(self):
        return self.hyperparams["num_epochs"]

    @property
    def steps_per_epoch(self):
        return self.hyperparams["steps_per_epoch"]

    @property
    def force_reading_input(self):
        return self.hyperparams["force_reading_input"]
