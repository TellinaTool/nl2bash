"""
Translation model that generates AST of program given natural language descriptions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import random
import sys
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
import seq2seq_model

import data_utils

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
tf.app.flags.DEFINE_integer("size", 200, "Size of each model layer.")
tf.app.flags.DEFINE_integer("num_layers", 1, "Number of layers in the model.")
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
tf.app.flags.DEFINE_boolean("lstm", False,
                            "Set to True for training with LSTM cells.")
tf.app.flags.DEFINE_boolean("eval", False,
                            "Set to True for quantitive evaluation.")
tf.app.flags.DEFINE_boolean("decode", False,
                            "Set to True for interactive decoding.")
tf.app.flags.DEFINE_boolean("bucket_selection", False,
                            "Run a bucket_selection if this is set to True.")
tf.app.flags.DEFINE_boolean("self_test", False,
                            "Run a self-test if this is set to True.")

FLAGS = tf.app.flags.FLAGS

def train(train_set, dev_set, num_iter):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:

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