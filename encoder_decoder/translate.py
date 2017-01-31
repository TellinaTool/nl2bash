#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Translation model that generates bash commands given natural language descriptions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import itertools
import math
import numpy as np
import random
import time
from tqdm import tqdm

import tensorflow as tf
from tensorflow.python.util import nest

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import data_utils, graph_utils, decode_tools, hyperparam_range, parse_args
    from eval import eval_tools
    from classifiers import BinaryLogisticRegressionModel
    from seq2seq.seq2seq_model import Seq2SeqModel
    from seq2tree.seq2tree_model import Seq2TreeModel
else:
    from encoder_decoder import data_utils, graph_utils, decode_tools
    from encoder_decoder import hyperparam_range, parse_args
    from eval import eval_tools
    from .classifiers import BinaryLogisticRegressionModel
    from .seq2seq.seq2seq_model import Seq2SeqModel
    from .seq2tree.seq2tree_model import Seq2TreeModel

FLAGS = tf.app.flags.FLAGS
parse_args.define_input_flags()

_buckets = graph_utils.get_buckets(FLAGS)


def create_model(session, forward_only, construct_model_dir=True, buckets=None):
    """
    Refer parse_args.py for model parameter explanations.
    """
    if buckets is None:
        buckets = _buckets

    if FLAGS.decoder_topology in ['basic_tree']:
        return graph_utils.create_model(session, FLAGS, Seq2TreeModel, buckets,
                                        forward_only, construct_model_dir)
    elif FLAGS.decoder_topology in ['rnn']:
        return graph_utils.create_model(session, FLAGS, Seq2SeqModel, buckets,
                                        forward_only, construct_model_dir)
    else:
        raise ValueError("Unrecognized decoder topology: {}."
                         .format(FLAGS.decoder_topology))


# --- Run/train slot-filling classifier --- #

def train_slot_filling_classifier(train_set, dev_set):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        seq2seq_model, global_epochs = graph_utils.create_model(sess, FLAGS,
            Seq2SeqModel, buckets=_buckets, forward_only=True)
        for bucket_id in xrange(len(_buckets)):
            formatted_example = seq2seq_model.get_bucket(train_set, bucket_id)
            encoder_outputs, decoder_outputs = \
                seq2seq_model.get_hidden_states(sess, formatted_example, bucket_id)
            print(encoder_outputs)
        model, _ = graph_utils.create_model(sess, FLAGS,
            BinaryLogisticRegressionModel, buckets=None, forward_only=False,
            construct_model_dir=False)
        model.train(sess, X, Y)
        model.eval(sess, X, Y)

# --- Run/train encoder-decoder models --- #

def train(train_set, dev_set, construct_model_dir=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model, global_epochs = create_model(sess, forward_only=False,
                                            construct_model_dir=construct_model_dir)

        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(_buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
        # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
        # the size if i-th training bucket, as used later.
        train_buckets_scale = [sum(train_bucket_sizes[:i+1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        loss, dev_loss, epoch_time = 0.0, 0.0, 0.0
        current_step = 0
        previous_losses = []
        previous_dev_losses = []

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
                _, step_loss, _, _ = model.step(sess, formatted_example,
                                                bucket_id, forward_only=False)
                loss += step_loss
                current_step += 1

            epoch_time = time.time() - start_time

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.epochs_per_checkpoint == 0:

                # Print statistics for the previous epoch.
                loss /= FLAGS.steps_per_epoch
                ppx = math.exp(loss) if loss < 300 else float('inf')
                print("learning rate %.4f epoch-time %.4f perplexity %.2f" % (
                    model.learning_rate.eval(), epoch_time, ppx))

                # Decrease learning rate if no improvement of loss was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)

                checkpoint_path = os.path.join(FLAGS.model_dir, "translate.ckpt")
                # Save checkpoint and zero timer and loss.
                model.saver.save(sess, checkpoint_path, global_step=global_epochs+t+1,
                                 write_meta_graph=False)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0
                # Run evals on development set and print the metrics.
                repeated_samples = range(len(_buckets)) * 10
                for bucket_id in repeated_samples:
                    if len(dev_set[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    formatted_example = model.get_batch(dev_set, bucket_id)
                    _, output_logits, eval_loss, _ = \
                        model.step(sess, formatted_example, bucket_id, forward_only=True)
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))

                dev_size = 10
                dev_loss = dev_loss / dev_size
                dev_perplexity = math.exp(dev_loss) if dev_loss < 1000 else float('inf')
                print("global step %d learning rate %.4f dev_perplexity %.2f" 
                        % (global_epochs+t+1, model.learning_rate.eval(), dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    return False
           
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()
    return True


def decode(data_set, construct_model_dir=True, verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True,
                                construct_model_dir=construct_model_dir)

        _, rev_sc_vocab, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)

        decode_tools.decode_set(sess, model, data_set,
                                rev_sc_vocab, rev_tg_vocab, FLAGS, verbose)
        return model.model_sig


def eval(data_set, model_sig=None, verbose=True):
    if model_sig is None:
        _, model_sig = graph_utils.get_model_signature(FLAGS)
    print("evaluate " + model_sig + "...")
    _, rev_sc_vocab, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)

    return eval_tools.eval_set(model_sig, data_set, rev_sc_vocab, FLAGS,
                               verbose=verbose)


def manual_eval(num_eval):
    # Create model and load parameters.
    _, model_sig = graph_utils.get_model_signature(FLAGS)
    _, rev_sc_vocab, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)
    _, dev_set, _ = load_data(use_buckets=False)

    eval_tools.manual_eval(model_sig, dev_set, rev_sc_vocab, FLAGS,
                           FLAGS.model_dir, num_eval)


def demo():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        sc_vocab, _, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)

        decode_tools.demo(sess, model, sc_vocab, rev_tg_vocab, FLAGS)


def train_and_eval(train_set, dev_set):
    train(train_set, dev_set, construct_model_dir=True)
    tf.reset_default_graph()
    decode(dev_set, construct_model_dir=False, verbose=False)
    temp_match_score, _, temp_dist, _ = eval(dev_set, verbose=False)
    tf.reset_default_graph()
    return temp_match_score, temp_dist


def cross_validation(train_set):
    num_folds = FLAGS.num_folds
    print("======== {}-fold Cross Validation ========".format(num_folds))

    match_scores = []
    dists = []

    # divide training data into N-folds
    train_folds = data_utils.fold_split_bucket(train_set, num_folds)
    for fold_id in xrange(num_folds):
        print("\nFold {}\n".format(fold_id))
        if _buckets:
            cv_train_set = [[] for _ in xrange(len(_buckets))]
        else:
            cv_train_set = []
        for i in xrange(num_folds):
            if i != fold_id:
                if _buckets:
                    for bucket_id in xrange(len(_buckets)):
                        cv_train_set[bucket_id] += train_folds[i][bucket_id]
                else:
                    cv_train_set += train_folds[i]
        cv_dev_set = train_folds[fold_id]
        train(cv_train_set, cv_dev_set)
        tf.reset_default_graph()
        model_sig = decode(cv_dev_set, construct_model_dir=False)
        tf.reset_default_graph()
        match_score, _, dist, _ = \
            eval(cv_dev_set, model_sig, verbose=False)
        match_scores.append(match_score)
        dists.append(dist)

    print("cross validation template match score = {}"
          .format(sum(match_scores) / num_folds))
    print("cross validation template distance = {}"
          .format(sum(dists) / num_folds))


def grid_search(train_set, dev_set):
    FLAGS.create_fresh_params = True

    hyperparameters = FLAGS.tuning.split(',')
    num_hps = len(hyperparameters)
    hp_range = hyperparam_range.hyperparam_range

    print("======== Grid Search ========")
    print("%d hyperparameters: " % num_hps)
    for i in xrange(num_hps):
        print("{}: {}".format(hyperparameters[i], hp_range[hyperparameters[i]]))
    print()

    grid = [v for v in hp_range[hyperparameters[0]]]
    for i in xrange(1, num_hps):
        grid = itertools.product(grid, hp_range[hyperparameters[i]])

    best_hp_set = [-1] * num_hps
    best_seed = -1
    best_temp_match_score = 0.0
    best_temp_dist = 100

    model_root_dir = FLAGS.model_dir

    for row in grid:
        row = nest.flatten(row)
        for i in xrange(num_hps):
            setattr(FLAGS, hyperparameters[i], row[i])
        FLAGS.model_dir = model_root_dir

        print("Trying parameter set: ")
        for i in xrange(num_hps):
            print("* {}: {}".format(hyperparameters[i], row[i]))

        num_trials = 5 if FLAGS.initialization else 1

        for t in xrange(num_trials):
            seed = random.getrandbits(32)
            tf.set_random_seed(seed)
            temp_match_score, temp_dist = \
                train_and_eval(train_set, dev_set)
            print("Parameter set: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], row[i]))
            print("random seed: {}".format(seed))
            print("template match score = {}".format(temp_match_score))
            print("template distance = {}".format(temp_dist))
            print("Best parameter set so far: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
            print("Best random seed so far: {}".format(best_seed))
            print("Best template match score so far = {}".format(best_temp_match_score))
            print("Best template distance so far = {}".format(best_temp_dist))
            # if temp_match_score > best_temp_match_score:
            if temp_dist < best_temp_dist:
                best_hp_set = row
                best_seed = seed
                best_temp_match_score = temp_match_score
                best_temp_dist = temp_dist
                print("☺ New best parameter setting found")

    print()
    print("*****************************")
    print("Best parameter set: ")
    for i in xrange(num_hps):
        print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
    print("Best seed = {}".format(best_seed))
    print("Best template match score = {}".format(best_temp_match_score))
    print("Best template distance = {}".format(best_temp_dist))
    print("*****************************")

# --- Pre-processing and data statistics --- #

def load_data(use_buckets=True, load_mappings=False):
    print(FLAGS.data_dir)
    if use_buckets:
        return data_utils.load_data(FLAGS, _buckets, load_mappings=load_mappings)
    else:
        return data_utils.load_data(FLAGS, None, load_mappings=load_mappings)


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)
    data_utils.prepare_data(FLAGS)


def induce_slot_filling_alignment():
    print("Preparing slot-filling data in %s" % FLAGS.data_dir)
    data_utils.prepare_slot_filling_data(FLAGS)


def data_statistics():
    data_utils.data_stats(FLAGS)


def main(_):
    # set GPU device
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.gpu
    
    # set up data and model directories
    FLAGS.data_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", FLAGS.dataset)
    print("Reading data from {}".format(FLAGS.data_dir))

    if FLAGS.decoder_topology in ['basic_tree']:
        FLAGS.model_dir = os.path.join(
            os.path.dirname(__file__), "..", FLAGS.model_dir, "seq2tree")
    elif FLAGS.decoder_topology in ['rnn']:
        FLAGS.model_dir = os.path.join(
            os.path.dirname(__file__), "..", FLAGS.model_dir, "seq2seq")
    else:
        raise ValueError("Unrecognized decoder topology: {}."
                         .format(FLAGS.decoder_topology))
    print("Saving models to {}".format(FLAGS.model_dir))

    if FLAGS.eval:
        _, dev_set, test_set = load_data()
        if FLAGS.test:
            eval(test_set)
        else:
            eval(dev_set)
    elif FLAGS.manual_eval:
        manual_eval(100)
    elif FLAGS.decode:
        _, dev_set, _ = load_data()
        model_sig = decode(dev_set)
        if not FLAGS.explanation:
            eval(dev_set, model_sig=model_sig, verbose=False)
    elif FLAGS.test:
        _, _, test_set = load_data()
        model_sig = decode(test_set)
        eval(test_set, model_sig=model_sig, verbose=False)
    elif FLAGS.demo:
        demo()
    elif FLAGS.grid_search:
        train_set, dev_set, _ = load_data()
        grid_search(train_set, dev_set)
    elif FLAGS.cross_valid:
        train_set, _, _ = load_data()
        cross_validation(train_set)
    elif FLAGS.process_slot_filling:
        induce_slot_filling_alignment()
    elif FLAGS.train_slot_filling:
        train_set, dev_set, _ = load_data(load_mappings=True)
        train_slot_filling_classifier(train_set, dev_set)
    elif FLAGS.process_data:
        process_data()
    elif FLAGS.data_stats:
        data_statistics()
    else:
        train_set, dev_set, _ = load_data()
        train(train_set, dev_set)
        tf.reset_default_graph()
        model_sig = decode(dev_set, construct_model_dir=False)
        if not FLAGS.explanation:
            eval(dev_set, model_sig, verbose=False)

    
if __name__ == "__main__":
    tf.app.run()
