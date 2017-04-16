#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Translation model that generates bash commands given natural language
descriptions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

if sys.version_info > (3, 0):
    from six.moves import xrange
    
import itertools
import math
import numpy as np
import random
import time
from tqdm import tqdm

import tensorflow as tf
from tensorflow.python.util import nest

from encoder_decoder import classifiers, data_utils, data_stats, graph_utils, \
    decode_tools, hyperparam_range, parse_args
from nlp_tools import tokenizer, slot_filling, constants
from eval import eval_tools
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

# --- Run/train encoder-decoder models --- #

def train(train_set, dev_set, construct_model_dir=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model, global_epochs = create_model(sess, forward_only=False,
                                            construct_model_dir=construct_model_dir)

        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(_buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll
        # use to select a bucket. Length of [scale[i], scale[i+1]] is
        # proportional to the size if i-th training bucket, as used later.
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
                model_outputs = model.step(sess, formatted_example,
                                           bucket_id, forward_only=False)
                loss += model_outputs.losses
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
                model.saver.save(sess, checkpoint_path,
                                 global_step=global_epochs+t+1,
                                 write_meta_graph=False)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0
                # Run evals on development set and print the metrics.
                dev_size = 10
                repeated_samples = list(range(len(_buckets))) * dev_size
                for bucket_id in repeated_samples:
                    if len(dev_set[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    formatted_example = model.get_batch(dev_set, bucket_id)
                    model_outputs = model.step(sess, formatted_example,
                                               bucket_id, forward_only=True)
                    eval_loss = model_outputs.losses
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))
                dev_loss = dev_loss / dev_size

                dev_perplexity = math.exp(dev_loss) if dev_loss < 1000 else float('inf')
                print("global step %d learning rate %.4f dev_perplexity %.2f" 
                        % (global_epochs+t+1, model.learning_rate.eval(), dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    return False
           
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()


        # Save slot filling embeddings.
        tf.reset_default_graph()
        mapping_path = os.path.join(FLAGS.model_dir,
            'train.{}.mappings.X.Y.npz'.format(FLAGS.sc_vocab_size))
        gen_slot_filling_training_data_fun(sess, model, train_set,
                                           mapping_path)
    return True


def decode(data_set, construct_model_dir=True, verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True,
                                construct_model_dir=construct_model_dir)

        decode_tools.decode_set(sess, model, data_set, FLAGS, verbose)

        return model.model_sig


def eval(data_set, model_sig=None, verbose=True):
    if model_sig is None:
        _, model_sig = graph_utils.get_model_signature(FLAGS)
    print("evaluating " + model_sig)

    return eval_tools.eval_set(model_sig, data_set, FLAGS, verbose=verbose)


def manual_eval(dataset, num_eval):
    # Create model and load parameters.
    _, model_sig = graph_utils.get_model_signature(FLAGS)
    eval_tools.manual_eval(
        model_sig, dataset, FLAGS, FLAGS.model_dir, num_eval)


def gen_eval_sheet(dataset):
    model_dir, model_sig = graph_utils.get_model_signature(FLAGS)
    print("evaluating " + model_sig)

    output_path = os.path.join(FLAGS.model_dir, model_dir, "predictions.csv")
    eval_tools.gen_eval_sheet(model_sig, dataset, FLAGS, output_path)
    print("prediction results saved to {}".format(output_path))


def demo():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)
        decode_tools.demo(sess, model, FLAGS)


def train_and_eval(train_set, dev_set):
    train(train_set, dev_set, construct_model_dir=True)
    tf.reset_default_graph()
    decode(dev_set, construct_model_dir=False, verbose=False)
    tms, cms = eval(dev_set, verbose=False)
    tf.reset_default_graph()
    return tms, cms


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
    best_tms = 0.0
    best_cms = 0.0

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
            tms, cms = train_and_eval(train_set, dev_set)
            print("Parameter set: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], row[i]))
            print("random seed: {}".format(seed))
            print("Template match score = {}".format(tms))
            print("Template match score (token-based) = {}".format(cms))
            print("Best parameter set so far: ")
            for i in xrange(num_hps):
                print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
            print("Best random seed so far: {}".format(best_seed))
            print("Best template match score so far = {}".format(best_tms))
            print("Best template match score (token-based) so far = {}".format(best_cms))
            if cms > best_cms:
                best_hp_set = row
                best_seed = seed
                best_tms = tms
                best_cms = cms
                print("☺ New best parameter setting found")

    print()
    print("*****************************")
    print("Best parameter set: ")
    for i in xrange(num_hps):
        print("* {}: {}".format(hyperparameters[i], best_hp_set[i]))
    print("Best seed = {}".format(best_seed))
    print("Best template match score = {}".format(best_tms))
    print("Best template match score (token-based) = {}".format(best_cms))
    print("*****************************")


# --- Run/train slot-filling classifier --- #

def eval_local_slot_filling(train_path, test_path):
    """
    Evaluate accuracy of the local slot filling classifier.
    :param train_path: path to the training data points stored on disk.
    :param test_path: path to the test data points stored on disk.
    :return:
    """
    train_X, train_Y = data_utils.load_slot_filling_data(train_path)
    test_X, test_Y = data_utils.load_slot_filling_data(test_path)

    # Create model.
    model = classifiers.KNearestNeighborModel(FLAGS.num_nn_slot_filling,
                                              train_X, train_Y)
    model.eval(train_X, train_Y, verbose=True)
    model.eval(test_X, test_Y, verbose=False)


def eval_slot_filling(dataset):
    """
    Evaluate accuracy of the global slot filling algorithm.
    """
    model_param_dir = os.path.join(FLAGS.model_dir,
        'train.{}.mappings.X.Y.npz'.format(FLAGS.sc_vocab_size))
    train_X, train_Y = data_utils.load_slot_filling_data(model_param_dir)
    slot_filling_classifier = classifiers.KNearestNeighborModel(
        FLAGS.num_nn_slot_filling, train_X, train_Y)
    print('Slot filling classifier parameters loaded.')

    _, _, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model, global_epochs = graph_utils.create_model(sess, FLAGS,
            Seq2SeqModel, buckets=_buckets, forward_only=True)

        num_correct = 0.0
        num_predict = 0.0
        num_gt = 0.0
        for bucket_id in xrange(len(_buckets)):
            for i in xrange(len(dataset[bucket_id])):
                sc, tg, sc_ids, tg_ids, gt_mappings = dataset[bucket_id][i]
                gt_mappings = [tuple(m) for m in gt_mappings]
                if gt_mappings:
                    _, entities = tokenizer.ner_tokenizer(sc)
                    nl_fillers = entities[0]
                    encoder_inputs = [dataset[bucket_id][i][2]]
                    encoder_full_inputs = [dataset[bucket_id][i][4]]
                    decoder_inputs = [dataset[bucket_id][i][3]]
                    decoder_full_inputs = [dataset[bucket_id][i][5]]
                    formatted_example = model.format_example(
                        [encoder_inputs, encoder_full_inputs],
                        [decoder_inputs, decoder_full_inputs],
                        bucket_id=bucket_id)
                    model_outputs = model.step(sess, formatted_example,
                                               bucket_id, forward_only=True,
                                               return_rnn_hidden_states=True)
                    encoder_outputs = model_outputs.encoder_hidden_states
                    decoder_outputs = model_outputs.decoder_hidden_states
                    cm_slots = {}
                    output_tokens = []
                    outputs = tg_ids[1:-1]
                    for ii in xrange(len(outputs)):
                        output = outputs[ii]
                        if output < len(rev_tg_vocab):
                            pred_token = rev_tg_vocab[output]
                            if "@@" in pred_token:
                                pred_token = pred_token.split("@@")[-1]
                            output_tokens.append(pred_token)
                            if nl_fillers is not None and \
                                    pred_token in constants._ENTITIES:
                                if ii > 0 and slot_filling.is_min_flag(
                                        rev_tg_vocab[outputs[ii-1]]):
                                    pred_token_type = 'Timespan'
                                else:
                                    pred_token_type = pred_token
                                cm_slots[ii] = (pred_token, pred_token_type)
                        else:
                            output_tokens.append(data_utils._UNK)
                    tree2, temp, mappings = slot_filling.stable_slot_filling(
                                output_tokens, nl_fillers, cm_slots,
                                encoder_outputs[0], decoder_outputs[0],
                                slot_filling_classifier)
                    # print(mappings)
                    # print(gt_mappings)
                    for mapping in mappings:
                        if mapping in gt_mappings:
                            num_correct += 1
                    num_predict += len(mappings)
                    num_gt += len(gt_mappings)

        precision = num_correct / num_predict
        recall = num_correct / num_gt
        print("Precision: {}".format(precision))
        print("Recall: {}".format(recall))
        print("F1: {}".format(2 * precision * recall / (precision + recall)))


def gen_slot_filling_training_data_fun(sess, model, dataset, output_file):
    X, Y = [], []
    for bucket_id in xrange(len(_buckets)):
        for i in xrange(len(dataset[bucket_id])):
            sc, tg, sc_ids, tg_ids, _, _, gt_mappings = dataset[bucket_id][i]
            mappings = [tuple(m) for m in gt_mappings]
            if gt_mappings:
                encoder_inputs = [dataset[bucket_id][i][2]]
                encoder_full_inputs = [dataset[bucket_id][i][4]]
                decoder_inputs = [dataset[bucket_id][i][3]]
                decoder_full_inputs = [dataset[bucket_id][i][5]]
                formatted_example = model.format_example(
                    [encoder_inputs, encoder_full_inputs],
                    [decoder_inputs, decoder_full_inputs],
                    bucket_id=bucket_id)
                model_outputs = model.step(sess, formatted_example, bucket_id,
                    forward_only=True, return_rnn_hidden_states=True)
                encoder_outputs = model_outputs.encoder_hidden_states
                decoder_outputs = model_outputs.decoder_hidden_states

                # add positive examples
                for f, s in mappings:
                    # use reversed index for the encoder embedding matrix
                    ff = _buckets[bucket_id][0] - f - 1
                    assert(f <= encoder_outputs.shape[1])
                    assert(s <= decoder_outputs.shape[1])
                    X.append(np.concatenate([encoder_outputs[:, ff, :],
                                             decoder_outputs[:, s, :]], axis=1))
                    Y.append(np.array([1, 0]))
                    # add negative examples
                    # sample unmatched filler-slot pairs as negative examples
                    if len(mappings) > 1:
                        for n_s in [ss for _, ss in mappings if ss != s]:
                            X.append(np.concatenate(
                                [encoder_outputs[:, ff, :],
                                 decoder_outputs[:, n_s, :]], axis=1))
                            Y.append(np.array([0, 1]))
                    # Debugging
                    # if i == 0:
                    #     print(ff)
                    #     print(encoder_outputs[:, ff, :].shape)
                    #     print(X[0].shape)
                    #     print(encoder_outputs[:, ff, :][0, :40])
                    #     print(X[0][0, :40])
            if i > 0 and i % 1000 == 0:
                print('{} examples gathered for generating slot filling features...'
                      .format(len(X)))

    np.savez(output_file, [X, Y])


def gen_slot_filling_training_data():
    _, _, _, rev_tg_vocab = data_utils.load_vocab(FLAGS)

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        datasets = load_data(load_mappings=True)

        seq2seq_model, global_epochs = graph_utils.create_model(sess, FLAGS,
            Seq2SeqModel, buckets=_buckets, forward_only=True)

        data_splits = ['train', 'dev', 'test']
        for i in xrange(len(data_splits)):
            split = data_splits[i]
            mapping_path = os.path.join(FLAGS.model_dir,
                '{}.{}.mappings.X.Y.npz'.format(split, FLAGS.sc_vocab_size))
            gen_slot_filling_training_data_fun(
                sess, seq2seq_model, datasets[i], mapping_path)


# --- Pre-processing --- #

def load_data(use_buckets=True, load_mappings=True):
    if use_buckets:
        return data_utils.load_data(FLAGS, _buckets, load_mappings=load_mappings)
    else:
        return data_utils.load_data(FLAGS, None, load_mappings=load_mappings)


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)
    data_utils.prepare_data(FLAGS)

# --- Data Statistics --- #

def data_statistics():
    data_stats.data_stats(FLAGS)


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

    if FLAGS.data_stats:
        data_statistics()
    elif FLAGS.process_data:
        process_data()

    elif FLAGS.gen_slot_filling_training_data:
        gen_slot_filling_training_data()
    elif FLAGS.eval_slot_filling:
        _, dev_set, test_set = load_data(load_mappings=True)
        dataset = test_set if FLAGS.test else dev_set
        eval_slot_filling(dataset)
    elif FLAGS.eval_local_slot_filling:
        train_path = os.path.join(
            FLAGS.model_dir, 'train.{}.mappings.X.Y.npz'.format(FLAGS.sc_vocab_size))
        dev_path = os.path.join(
            FLAGS.model_dir, 'dev.{}.mappings.X.Y.npz'.format(FLAGS.sc_vocab_size))
        eval_local_slot_filling(train_path, dev_path)

    elif FLAGS.demo:
        demo()

    else:
        train_set, dev_set, test_set = load_data()
        if FLAGS.gen_eval_sheet:
            dataset = test_set if FLAGS.test else dev_set
            gen_eval_sheet(dataset)
        elif FLAGS.eval:
            dataset = test_set if FLAGS.test else dev_set
            eval(dataset, verbose=False)
        elif FLAGS.manual_eval:
            dataset = test_set if FLAGS.test else dev_set
            manual_eval(dataset, 100)
        elif FLAGS.decode:
            dataset = test_set if FLAGS.test else dev_set
            model_sig = decode(dataset)
            if not FLAGS.explain:
                eval(dataset, model_sig=model_sig, verbose=False)
        elif FLAGS.grid_search:
            grid_search(train_set, dev_set)
        elif FLAGS.cross_valid:
            cross_validation(train_set)
        else:
            # Train the model.
            train(train_set, dev_set)

            # Decode the new model on the development set.
            tf.reset_default_graph()
            model_sig = decode(dev_set, construct_model_dir=False)

            # Run automatic evaluation on the development set.
            if not FLAGS.explain:
                eval(dev_set, model_sig, verbose=False)

    
if __name__ == "__main__":
    tf.app.run()
