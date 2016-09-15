#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Translation model that generates AST of program given natural language descriptions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "eval"))

import time
import cPickle as pickle

import numpy as np
from tqdm import tqdm

import tensorflow as tf

import eval_tools
import data_utils, data_tools, graph_utils
import parse_args
from encoder_decoder import Seq2TreeModel

FLAGS = tf.app.flags.FLAGS

parse_args.define_input_flags()

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
_buckets = [(10, 20), (20, 30), (30, 40), (40, 50), (40, 64)]


def create_model(session, forward_only):
    """
    :param source_vocab_size: size of the source vocabulary.
    :param target_vocab_size: size of the target vocabulary.
    :param max_source_length: maximum length of the source sequence
        (necessary for static graph construction).
    :param max_target_length: maximum length of the target sequence
        (necessary for static graph construction).
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
    return graph_utils.create_model(session, FLAGS, Seq2TreeModel, _buckets,
                                    forward_only)


def train(train_set, dev_set, verbose=False):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model, global_epochs = create_model(sess, forward_only=False)

        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(_buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
        # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
        # the size if i-th training bucket, as used later.
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        loss, dev_loss, epoch_time = 0.0, 0.0, 0.0
        current_step = 0
        previous_losses = []
        previous_dev_losses = []

        # Load Vocabularies for evaluation on dev set at each checkpoint
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        # dev_set = train_set + dev_set
        for t in xrange(FLAGS.num_epochs):
            print("Epoch %d" % (t+1))

            start_time = time.time()

            # progress bar
            for _ in tqdm(xrange(FLAGS.steps_per_epoch)):
                time.sleep(0.01)
                random_number_01 = np.random.random_sample()
                bucket_id = min([i for i in xrange(len(train_buckets_scale))
                                 if train_buckets_scale[i] > random_number_01])
                formatted_example = model.get_batch(train_set, bucket_id)
                _, step_loss, _, _ = model.step(sess, formatted_example, bucket_id,
                                             forward_only=False)
                loss += step_loss
                current_step += 1

            epoch_time = time.time() - start_time

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.epochs_per_checkpoint == 0:

                # Print statistics for the previous epoch.
                loss /= FLAGS.steps_per_epoch
                ppx = math.exp(loss) if loss < 300 else float('inf')
                print("learning rate %.4f epoch-time %.2f perplexity %.2f" % (
                    model.learning_rate.eval(), epoch_time, ppx))

                # Decrease learning rate if no improvement of loss was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)

                checkpoint_path = os.path.join(FLAGS.train_dir, "translate.ckpt")
                # Save checkpoint and zero timer and loss.
                model.saver.save(sess, checkpoint_path, global_step=global_epochs+t+1,
                                 write_meta_graph=False)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0
                # Run evals on development set and print the metrics.
                for bucket_id in xrange(len(_buckets)):
                    if len(dev_set[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    formatted_example = model.get_batch(dev_set, bucket_id)
                    _, eval_loss, output_logits, _ = model.step(sess, formatted_example, bucket_id,
                                                             forward_only=True)
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))

                dev_perplexity = math.exp(dev_loss/len(_buckets)) if dev_loss < 300 else float('inf')
                print("global step %d learning rate %.4f dev_perplexity %.2f" 
                        % (global_epochs+t+1, model.learning_rate.eval(), dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    return False
           
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()
      
    return True


def eval(verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_tools.eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab,
                            FLAGS, verbose)


def manual_eval(num_eval):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_tools.manual_eval(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab,
                               FLAGS, num_eval)


def compare_models():
    model_paths = [
        os.path.join(os.path.dirname(__file__), "..", "model/seq2seq/rnn-gru-128"),
        os.path.join(os.path.dirname(__file__), "..", "model/seq2seq/rnn-gru-attention-128"),
        os.path.join(os.path.dirname(__file__), "..", "model/seq2tree.by.command/rnn-gru-16"),
        os.path.join(os.path.dirname(__file__), "..", "model/seq2tree.by.command/rnn-gru-attention-16")
    ]

    sessions = []
    models = []
    for model_path in model_paths:
        FLAGS.train_dir = model_path
        with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
            model, _ = create_model(sess, forward_only=True)
            sessions.append(sess)
            models.append(model)

    # Load vocabularies.
    nl_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.nl" % FLAGS.nl_vocab_size)
    cm_vocab_path = os.path.join(FLAGS.data_dir,
                                 "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
    _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
    _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
    _, dev_set, _ = load_data()

    eval_tools.compare_models(sessions, models, dev_set, rev_nl_vocab, rev_cm_vocab,
                              FLAGS, num_eval=50)


def interactive_decode():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm.ast" % FLAGS.cm_vocab_size)
        nl_vocab, _ = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        eval_tools.interactive_decode(sess, model, nl_vocab, rev_cm_vocab,
                                      FLAGS)


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)

    with open(FLAGS.data_dir + "data.by.%s.dat" % FLAGS.data_split) as f:
        data = pickle.load(f)

    numFolds = len(data)
    print("%d folds" % numFolds)

    output_dir = os.path.join(FLAGS.data_dir, "seq2tree.by.%s" % FLAGS.data_split)
    data_utils.prepare_data(data, output_dir, FLAGS.nl_vocab_size, FLAGS.cm_vocab_size)


def load_data(sample_size=-1, use_buckets=True):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = FLAGS.data_dir
    nl_train = os.path.join(data_dir, "train") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_train = os.path.join(data_dir, "train") + ".seq%d.cm" % FLAGS.cm_vocab_size
    nl_dev = os.path.join(data_dir, "dev") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_dev = os.path.join(data_dir, "dev") + ".seq%d.cm" % FLAGS.cm_vocab_size
    nl_test = os.path.join(data_dir, "test") + ".ids%d.nl" % FLAGS.nl_vocab_size
    cm_test = os.path.join(data_dir, "test") + ".seq%d.cm" % FLAGS.cm_vocab_size

    buckets = _buckets if use_buckets else None

    train_set = data_utils.read_data(nl_train, cm_train, buckets, FLAGS.max_train_data_size)
    dev_set = data_utils.read_data(nl_dev, cm_dev, buckets)
    test_set = data_utils.read_data(nl_test, cm_test, buckets)

    return train_set, dev_set, test_set


def data_statistics():
    train_set, dev_set, test_set = load_data(use_buckets=False)
    print(len(data_utils.group_data_by_nl(train_set)))
    print(len(data_utils.group_data_by_nl(dev_set)))
    print(len(data_utils.group_data_by_nl(test_set)))

    print("data count = %d" % len(data_utils.group_data_by_cm(train_set)))
    print("data count = %d" % len(data_utils.group_data_by_cm(dev_set)))
    print("data count = %d" % len(data_utils.group_data_by_cm(test_set)))


def main(_):
    # set GPU device
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.gpu

    if FLAGS.eval:
        eval()
    elif FLAGS.manual_eval:
        manual_eval(50)
    elif FLAGS.decode:
        interactive_decode()
    elif FLAGS.process_data:
        process_data()
    elif FLAGS.data_stats:
        data_statistics()
    elif FLAGS.compare_models:
        compare_models()
    elif FLAGS.sample_train:
        train_set, dev_set, _ = load_data(FLAGS.sample_size)
        train(train_set, dev_set)
    else:
        train_set, dev_set, _ = load_data()
        train(train_set, dev_set, verbose=False)


if __name__ == "__main__":
    tf.app.run()
