"""
Translation model that generates AST of program given natural language descriptions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math, random
import os, sys
sys.path.append("../bashlex")
sys.path.append("../eval")

import time
import cPickle as pickle

import numpy as np

from bash import basic_tokenizer, bash_tokenizer
from token_overlap import TokenOverlap
from random import shuffle

from six.moves import xrange  # pylint: disable=redefined-builtin

import tensorflow as tf
from seq2tree_model import Seq2TreeModel

import data_utils

tf.app.flags.DEFINE_integer("nl_vocab_size", 4000, "English vocabulary size.")
tf.app.flags.DEFINE_integer("cm_vocab_size", 4000, "Bash vocabulary size.")
tf.app.flags.DEFINE_string("data_dir", "/tmp", "Data directory")
tf.app.flags.DEFINE_string("train_dir", "/tmp", "Training directory.")

tf.app.flags.DEFINE_string("decoder", "greedy", "Type of decoder to use.")
tf.app.flags.DEFINE_integer("beam_size", 3, "Size of beam for beam search.")

tf.app.flags.DEFINE_integer("max_train_data_size", 0,
                            "Limit on the size of training data (0: no limit).")
tf.app.flags.DEFINE_integer("iters_per_checkpoint", 1,
                            "How many training steps to do per checkpoint.")
tf.app.flags.DEFINE_integer("iters_per_milestone", 1,
                            "How many training steps to do per dev-set evaluation")
tf.app.flags.DEFINE_integer("num_milestones", 10,
                            "How many dev-set evaluation to be performed during training")

tf.app.flags.DEFINE_integer("gpu", 0, "GPU device where the computation is going to be placed.")
tf.app.flags.DEFINE_boolean("log_device_placement", False,
                            "Set to True for logging device placement.")

tf.app.flags.DEFINE_boolean("eval", False,
                            "Set to True for quantitive evaluation.")
tf.app.flags.DEFINE_boolean("decode", False,
                            "Set to True for interactive decoding.")
tf.app.flags.DEFINE_boolean("bucket_selection", False,
                            "Run a bucket_selection if this is set to True.")
tf.app.flags.DEFINE_boolean("self_test", False,
                            "Run a self-test if this is set to True.")

# learning hyperparameters
tf.app.flags.DEFINE_string("optimizer", "adam")
tf.app.flags.DEFINE_float("learning_rate", 0.5, "Learning rate.")
tf.app.flags.DEFINE_float("learning_rate_decay_factor", 0.99,
                          "Learning rate decays by this much.")
tf.app.flags.DEFINE_float("input_keep_prob", 1.0,
                          "Dropout: proportion of input units to keep.")
tf.app.flags.DEFINE_float("output_keep_prob", 1.0,
                          "Dropout: proportion of output units to keep.")
tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
                          "Clip gradients to this norm.")
tf.app.flags.DEFINE_integer("batch_size", 64,
                            "Batch size to use during training.")
tf.app.flags.DEFINE_integer("num_samples", 512,
                            "Number of samples for sampled softmax.")
tf.app.flags.DEFINE_integer("input_keep_prob", 1.0,
                            "Proportion of input to keep if dropout is used.")
tf.app.flags.DEFINE_integer("output_keep_prob", 1.0,
                            "Proportion of output to keep if dropout is used.")
tf.app.flags.DEFINE_integer("size", 200, "Size of each model layer.")
tf.app.flags.DEFINE_integer("num_layers", 1, "Number of layers in the model.")
tf.app.flags.DEFINE_boolean("attention", True, "If set, use attention decoder.")


FLAGS = tf.app.flags.FLAGS

def create_model(session, forward_only):
    """
    :param source_vocab_size: size of the source vocabulary.
    :param target_vocab_size: size of the target vocabulary.
    :param dim: dimension of each layer in the model.
    :param num_layers: number of layers in the model.
    :param max_gradient_norm: gradients are clipped to maximally this norm.
    :param batch_size: the size of the batches used during training or decoding.
    :param learning_rate: learning rate to start with.
    :param learning_rate_decay_factor: decay learning rate by this much when needed.
            not import if the adam optimizer is used.
    :param input_keep_prob: proportion of input to keep if dropout is used.
    :param output_keep_prob: proportion of output to keep if dropout is used.
    :param num_samples: number of samples for sampled softmax.

    :param decoder_topology: topology of the tree rnn decoder.
    :param decoding_algorithm: decoding algorithm used.
    :param
    """
    params = collections.defaultdict()
    params["source_vocab_size"] = FLAGS.source_vocab_size
    params["target_vocab_size"] = FLAGS.target_vocab_size
    params["dim"] = FLAGS.dim
    params["num_layers"] = FLAGS.num_layers
    params["max_gradient_norm"] = FLAGS.max_gradient_norm
    params["batch_size"] = FLAGS.batch_size
    params["num_samples"] = FLAGS.num_samples
    params["input_keep_prob"] = FLAGS.input_keep_prob
    params["output_keep_prob"] = FLAGS.output_keep_prob
    params["optimizer"] = FLAGS.optimizer
    params["learning_rate"] = FLAGS.learning_rate
    params["learning_rate_decay_factor"] = FLAGS.learning_rate_decay_factor
    params["attention"] = FLAGS.attention

    params["decoder_topology"] = FLAGS.decoder_topology
    params["decoding_algorithm"] = FLAGS.decoding_algorithm
    model = Seq2TreeModel(params, forward_only=forward_only)

    ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print("Created model with fresh parameters.")
        session.run(tf.initialize_all_variables())
    return model

def train(train_set, dev_set, num_iter):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model = create_model(sess, False)

        step_time, loss = 0.0, 0.0
        current_step = 0
        previous_dev_losses = []

        # Load Vocabularies for evaluation on dev set at each checkpoint
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        for t in xrange(num_iter):

            # shuffling training examples
            shuffle(train_set)

            for i in xrange(len(train_set)):
                nl, tree = train_set[i]

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.iters_per_checkpoint == 0:

                # Print statistics for the previous epoch.

                # Save checkpoint and zero timer and loss.

                # Run evals on development set and print the metrics.

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.


def train_and_eval(train_set, dev_set):
    num_iter = FLAGS.steps_per_milestone
    for i in xrange(FLAGS.num_milestones):
        is_learning = train(train_set, dev_set, num_iter)
        tf.reset_default_graph()
        eval(False)
        tf.reset_default_graph()

        if not is_learning:
            print("Training stopped early for no improvement observed on dev set.")
            break

def main(_):
    # set GPU device
    with tf.device('/gpu:%d' % FLAGS.gpu):
        if FLAGS.eval:
            eval()
        elif FLAGS.decode:
            decode()
        else:
            train_set, dev_set, _ = process_data()
            train_and_eval(train_set, dev_set)


if __name__ == "__main__":
    tf.app.run()