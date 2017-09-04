"""Utility functions related to graph construction."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import os

import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import data_utils


def define_model(FLAGS, session, model_constructor, buckets, forward_only):
    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')
    params = collections.defaultdict()

    params["source_vocab_size"] = FLAGS.sc_vocab_size
    params["target_vocab_size"] = FLAGS.tg_vocab_size
    params["max_source_length"] = FLAGS.max_sc_length
    params["max_target_length"] = FLAGS.max_tg_length
    params["max_source_token_size"] = FLAGS.max_sc_token_size
    params["max_target_token_size"] = FLAGS.max_tg_token_size
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

    params["tg_token_use_attention"] = FLAGS.tg_token_use_attention

    params["sc_token"] = FLAGS.sc_token
    params["sc_token_dim"] = FLAGS.sc_token_dim
    params["sc_char"] = FLAGS.sc_char
    # params["sc_char_vocab_size"] = FLAGS.sc_char_vocab_size
    # params["sc_char_dim"] = FLAGS.sc_char_dim
    # params["sc_char_composition"] = FLAGS.sc_char_composition
    # params["sc_char_rnn_cell"] = FLAGS.sc_char_rnn_cell
    # params["sc_char_rnn_num_layers"] = FLAGS.sc_char_rnn_num_layers
    # params["sc_token_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.token.feature.npy".format(source))
    # params["sc_char_features_path"] = os.path.join(
    #     FLAGS.data_dir, "{}.vocab.char.feature.npy".format(source))

    params["tg_token"] = FLAGS.tg_token
    params["tg_char"] = FLAGS.tg_char
    # params["tg_char_vocab_size"] = FLAGS.tg_char_vocab_size
    # params["tg_char_composition"] = FLAGS.tg_char_composition
    # params["tg_char_use_attention"] = FLAGS.tg_char_use_attention
    # params["tg_char_rnn_cell"] = FLAGS.tg_char_rnn_cell
    # params["tg_char_rnn_num_layers"] = FLAGS.tg_char_rnn_num_layers
    # params["tg_char_rnn_input_keep"] = FLAGS.tg_char_rnn_input_keep
    # params["tg_char_rnn_output_keep"] = FLAGS.tg_char_rnn_output_keep
    # params["tg_token_features_path"] = os.path.join(
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

    params["tg_token_attn_fun"] = FLAGS.tg_token_attn_fun
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
    model_subdir, decode_sig = get_decode_signature(FLAGS)
    setattr(FLAGS, 'model_dir', os.path.join(FLAGS.model_root_dir,
                                             model_subdir))
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
        else:
            clean_dir(FLAGS.model_dir)
        if FLAGS.pretrained_model_subdir:
            # load pre-trained parameteres for advanced training algorithms
            pretrain_dir = os.path.join(
                FLAGS.model_root_dir, FLAGS.pretrained_model_subdir)
            print("Initialize the graph with pre-trained parameters from {}"
                  .format(pretrain_dir))
            pretrain_ckpt = tf.train.get_checkpoint_state(pretrain_dir)
            model.saver.restore(session, pretrain_ckpt.model_checkpoint_path)
            session.run(model.learning_rate.assign(tf.constant(FLAGS.learning_rate)))
        else:
            print("Initialize the graph with random parameters.")
            session.run(tf.global_variables_initializer())

    return model


def get_decode_signature(FLAGS):
    """
    Model signature is used to locate the trained parameters and
    prediction results of a particular model.
    """

    # The model directory is stamped with training hyperparameter information.
    model_subdir = FLAGS.dataset
    if FLAGS.explain:
        model_subdir += '-expl'
    if FLAGS.channel == 'char':
        model_subdir += '--char'
    elif FLAGS.channel == 'partial.token':
        model_subdir += '--partial'
    else:
        if FLAGS.sc_token:
            model_subdir += '-T'
        if FLAGS.sc_char:
            model_subdir += '-C'
        if FLAGS.tg_char:
            model_subdir += '-TC'
            model_subdir += '-{}'.format(FLAGS.gamma)
    model_subdir += '-{}'.format(FLAGS.min_vocab_frequency)
    model_subdir += '-{}'.format(FLAGS.encoder_topology)
    model_subdir += '-{}'.format(FLAGS.rnn_cell)
    model_subdir += '-{}'.format(FLAGS.training_algorithm)
    if FLAGS.tg_token_use_attention:
        model_subdir += '-attention'
        model_subdir += '-{}'.format(FLAGS.attention_input_keep)
        model_subdir += '-{}'.format(FLAGS.attention_output_keep)
        model_subdir += '-{}'.format(FLAGS.beta)
    if FLAGS.use_copy:
        model_subdir += '-copy'
        model_subdir += '-{}'.format(FLAGS.chi)
    model_subdir += '-{}'.format(FLAGS.batch_size)
    if FLAGS.sc_token:
        model_subdir += '-{}'.format(FLAGS.sc_token_dim)
    if FLAGS.sc_char:
        model_subdir += '-{}'.format(FLAGS.sc_char_dim)
    model_subdir += '-{}'.format(FLAGS.num_layers)
    if FLAGS.recurrent_batch_normalization:
        model_subdir += '-rbc'
    model_subdir += '-{}'.format(FLAGS.learning_rate)
    model_subdir += '-{}'.format(FLAGS.adam_epsilon)
    model_subdir += '-{}'.format(FLAGS.sc_input_keep)
    model_subdir += '-{}'.format(FLAGS.sc_output_keep)
    model_subdir += '-{}'.format(FLAGS.tg_input_keep)
    model_subdir += '-{}'.format(FLAGS.tg_output_keep)
    if FLAGS.canonical:
        model_subdir += '.canonical'
    elif FLAGS.normalized:
        model_subdir += '.normalized'

    # The prediction file of a particular model is stamped with decoding 
    # hyperparameter information.
    decode_sig = FLAGS.token_decoding_algorithm
    if FLAGS.token_decoding_algorithm == 'beam_search': 
        decode_sig += ".{}".format(FLAGS.beam_size)
    if FLAGS.fill_argument_slots:
        decode_sig += '.slot.filler'
    decode_sig += (".test" if FLAGS.test else ".dev")
    return model_subdir, decode_sig


def clean_dir(dir):
    for f_name in os.listdir(dir):
        if f_name.startswith('prediction'):
            continue
        f_path = os.path.join(dir, f_name)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception as e:
            print(e)


def softmax_loss(output_project, num_samples, target_vocab_size):
    w, b = output_project
    if num_samples > 0 and num_samples < target_vocab_size:
        print("loss function = sampled_softmax_loss ({})".format(num_samples))
        w_t = tf.transpose(w)
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
    return -tf.reduce_sum(logits * tf.one_hot(targets, logits.get_shape()[1]), 1)


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


class InfPerplexityError(Exception):
    pass


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
    def tg_token_use_attention(self):
        return self.hyperparams["tg_token_use_attention"]

    @property
    def tg_token_attn_fun(self):
        return self.hyperparams["tg_token_attn_fun"]

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
    def recurrent_batch_normalization(self):
        return self.hyperparams["recurrent_batch_normalization"]

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
    def sc_token(self):
        return self.hyperparams["sc_token"]

    @property
    def sc_token_dim(self):
        """
        Source token channel embedding dimension.
        """
        return self.hyperparams["sc_token_dim"]

    @property
    def sc_input_keep(self):
        return self.hyperparams["sc_input_keep"]

    @property
    def sc_output_keep(self):
        return self.hyperparams["sc_output_keep"]

    @property
    def sc_token_features_path(self):
        return self.hyperparams["sc_token_features_path"]

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
    def tg_token_features_path(self):
        return self.hyperparams["tg_token_features_path"]

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
