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
    
import math
import numpy as np
import time
from tqdm import tqdm

import tensorflow as tf

from bashlex import data_tools
from encoder_decoder import classifiers
from encoder_decoder import data_stats
from encoder_decoder import data_utils
from encoder_decoder import decode_tools
from encoder_decoder import graph_utils
from encoder_decoder import meta_experiments
from encoder_decoder import parse_args
from .seq2seq.seq2seq_model import Seq2SeqModel
from .seq2tree.seq2tree_model import Seq2TreeModel
from eval import eval_tools
from nlp_tools import tokenizer, slot_filling, constants


FLAGS = tf.app.flags.FLAGS
parse_args.define_input_flags()

_buckets = graph_utils.get_buckets(FLAGS)


def create_model(session, forward_only, buckets=None):
    """
    Refer parse_args.py for model parameter explanations.
    """
    if buckets is None:
        buckets = _buckets

    if FLAGS.decoder_topology in ['basic_tree']:
        return graph_utils.create_model(
            session, FLAGS, Seq2TreeModel, buckets, forward_only)
    elif FLAGS.decoder_topology in ['rnn']:
        return graph_utils.create_model(
            session, FLAGS, Seq2SeqModel, buckets, forward_only)
    else:
        raise ValueError("Unrecognized decoder topology: {}."
                         .format(FLAGS.decoder_topology))

# --- Run/train encoder-decoder models --- #

def train(train_set, dev_set):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:

        # Create model.
        model = create_model(sess, forward_only=False)

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

            # progress bar
            start_time = time.time()
            for _ in tqdm(xrange(FLAGS.steps_per_epoch)):
                time.sleep(0.01)
                random_number_01 = np.random.random_sample()
                bucket_id = min([i for i in xrange(len(train_buckets_scale))
                                 if train_buckets_scale[i] > random_number_01])
                formatted_example = model.get_batch(train_set, bucket_id)
                model_outputs = model.step(
                    sess, formatted_example, bucket_id, forward_only=False)
                loss += model_outputs.losses
                current_step += 1
            epoch_time = time.time() - start_time

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.epochs_per_checkpoint == 0:
                # Print statistics for the previous epoch.
                loss /= FLAGS.steps_per_epoch
                if loss < 300:
                    ppx = math.exp(loss)
                else:
                    print("Training loss = {} is too large.".format(loss))
                    if t > 1:
                        break
                    else:
                        raise graph_utils.InfPerplexityError
                print("learning rate %.4f epoch-time %.4f perplexity %.2f" % (
                    model.learning_rate.eval(), epoch_time, ppx))

                # Decrease learning rate if no improvement of loss was seen
                # over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)

                checkpoint_path = os.path.join(FLAGS.model_dir, "translate.ckpt")
                # Save checkpoint and reset timer and loss.
                model.saver.save(
                    sess, checkpoint_path, global_step=t, write_meta_graph=False)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0
                # Run evals on development set and print the metrics.
                dev_size = 10
                repeated_samples = list(range(len(_buckets))) * dev_size
                for bucket_id in repeated_samples:
                    if len(dev_set[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    formatted_example = model.get_batch(dev_set, bucket_id)
                    model_outputs = model.step(
                        sess, formatted_example, bucket_id, forward_only=True)
                    eval_loss = model_outputs.losses
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))
                dev_loss = dev_loss / dev_size

                dev_perplexity = math.exp(dev_loss) if dev_loss < 1000 else float('inf')
                print("step %d learning rate %.4f dev_perplexity %.2f"
                        % (t+1, model.learning_rate.eval(), dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    break
           
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()

    if not FLAGS.explain and (FLAGS.normalized or FLAGS.canonical):
        tf.reset_default_graph()
        gen_slot_filling_training_data(train_set, dev_set)

    return True


def decode(data_set, verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)
        decode_tools.decode_set(sess, model, data_set, 3, FLAGS, verbose)

        return model.model_dir, model.decode_sig


def eval(data_set, model_dir=None, decode_sig=None, verbose=True):
    if model_dir is None:
        model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
        model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    print("evaluating " + model_dir)

    return eval_tools.eval_set(model_dir, decode_sig, data_set, 3, FLAGS, 
        verbose=verbose)


def manual_eval(dataset, num_eval):
    _, decode_sig = graph_utils.get_decode_signature(FLAGS)
    eval_tools.manual_eval(
        decode_sig, dataset, FLAGS, FLAGS.model_root_dir, num_eval)


def gen_eval_sheet(dataset):
    model_dir, decode_sig = graph_utils.get_decode_signature(FLAGS)
    print("evaluating " + decode_sig)

    output_path = os.path.join(FLAGS.model_root_dir, model_dir, "predictions.csv")
    eval_tools.gen_eval_sheet(decode_sig, dataset, FLAGS, output_path)
    print("prediction results saved to {}".format(output_path))


def demo():
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)
        decode_tools.demo(sess, model, FLAGS)

def write_predictions_to_file(test_file, output_file):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)
        decode_tools.write_predictions_to_file(
            test_file, output_file, sess, model, FLAGS)


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
        model_dir, decode_sig = decode(cv_dev_set)
        tf.reset_default_graph()
        match_score, _, dist, _ = \
            eval(cv_dev_set, model_dir, decode_sig, verbose=False)
        match_scores.append(match_score)
        dists.append(dist)

    print("cross validation template match score = {}"
          .format(sum(match_scores) / num_folds))
    print("cross validation template distance = {}"
          .format(sum(dists) / num_folds))


# --- Schedule experiments --- #

def schedule_experiments(train_fun, decode_fun, eval_fun, train_set, dev_set):
    # hp_set1 = {'universal_keep': 0.5}
    # hp_set2 = {'universal_keep': 0.6}
    # hp_set3 = {'universal_keep': 0.7}
    # hyperparam_sets = [hp_set1, hp_set2, hp_set3]
    
    hp_set1 = {'universal_keep': 0.6, 'rnn_cell': 'gru', 'num_layers': 2}
    hp_set2 = {'universal_keep': 0.75, 'rnn_cell': 'gru', 'num_layers': 2}
    hyperparam_sets = [hp_set1, hp_set2]
    meta_experiments.schedule_experiments(train_fun, decode_fun, eval_fun,
        train_set, dev_set, hyperparam_sets, FLAGS)


# --- Train/Test slot-filling classifier --- #

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
    Evaluate global slot filling algorithm F1 using ground truth templates.
    """
    vocabs = data_utils.load_vocab(FLAGS)
    rev_tg_vocab = vocabs.rev_tg_vocab
    rev_tg_full_vocab = vocabs.rev_tg_full_vocab

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model = graph_utils.create_model(
            sess, FLAGS, Seq2SeqModel, buckets=_buckets, forward_only=True)

        model_param_dir = os.path.join(
            FLAGS.model_dir, 'train.mappings.X.Y.npz')
        train_X, train_Y = data_utils.load_slot_filling_data(model_param_dir)
        slot_filling_classifier = classifiers.KNearestNeighborModel(
            FLAGS.num_nn_slot_filling, train_X, train_Y)
        print('Slot filling classifier parameters loaded.')

        num_correct_argument = 0.0
        num_argument = 0.0
        num_correct_align = 0.0
        num_predict_align = 0.0
        num_gt_align = 0.0
        for bucket_id in xrange(len(_buckets)):
            for data_id in xrange(len(dataset[bucket_id])):
                dp = dataset[bucket_id][data_id]
                gt_mappings = [tuple(m) for m in dp.mappings]
                outputs = dp.tg_ids[1:-1]
                full_outputs = dp.tg_full_ids[1:-1]
                if gt_mappings:
                    _, entities = tokenizer.ner_tokenizer(dp.sc_txt)
                    nl_fillers = entities[0]
                    encoder_inputs = [dp.sc_ids]
                    encoder_full_inputs = [dp.sc_copy_full_ids]
                    decoder_inputs = [dp.tg_ids]
                    decoder_full_inputs = [dp.tg_full_ids]
                    if FLAGS.use_copy:
                        pointer_targets = [dp.pointer_targets]
                    else:
                        pointer_targets = None
                    formatted_example = model.format_example(
                        [encoder_inputs, encoder_full_inputs],
                        [decoder_inputs, decoder_full_inputs],
                        pointer_targets=pointer_targets,
                        bucket_id=bucket_id)
                    model_outputs = model.step(sess, formatted_example,
                        bucket_id, forward_only=True, return_rnn_hidden_states=True)
                    encoder_outputs = model_outputs.encoder_hidden_states
                    decoder_outputs = model_outputs.decoder_hidden_states
                    cm_slots = {}
                    output_tokens = []
                    for ii in xrange(len(outputs)):
                        output = outputs[ii]
                        if output < len(rev_tg_vocab):
                            token = rev_tg_vocab[output]
                            if "@@" in token:
                                token = token.split("@@")[-1]
                            output_tokens.append(token)
                            if nl_fillers is not None and \
                                    token in constants._ENTITIES:
                                if ii > 0 and slot_filling.is_min_flag(
                                        rev_tg_vocab[outputs[ii-1]]):
                                    token_type = 'Timespan'
                                else:
                                    token_type = token
                                cm_slots[ii] = (token, token_type)
                        else:
                            output_tokens.append(data_utils._UNK)
                    if FLAGS.use_copy:
                        P = pointer_targets[0][0] > 0
                        pointers = model_outputs.pointers[0]
                        pointers = np.multiply(
                            np.sum(P.astype(float)[:pointers.shape[0],
                                -pointers.shape[1]:], 1, keepdims=True), pointers)
                        M = {}
                        for j in xrange(pointers.shape[0]):
                            for i in xrange(pointers.shape[1]):
                                ci = pointers.shape[1] - i - 1
                                if not ci in M:
                                    M[ci] = {}
                                if pointers[j, i] == 0:
                                    M[ci][j] = -np.inf
                                else:
                                    M[ci][j] = pointers[j, i]
                        mappings, _ = \
                            slot_filling.stable_marriage_alignment(M)
                    else:
                        tree, _, mappings = slot_filling.stable_slot_filling(
                                    output_tokens, nl_fillers, cm_slots,
                                    encoder_outputs[0], decoder_outputs[0],
                                    slot_filling_classifier)
                    for mapping in mappings:
                        if mapping in gt_mappings:
                            num_correct_align += 1
                    num_predict_align += len(mappings)
                    num_gt_align += len(gt_mappings)

                    tokens = data_tools.ast2tokens(tree)
                    if not tokens:
                        continue
                    for ii in xrange(len(outputs)):
                        output = outputs[ii]
                        token = rev_tg_vocab[output]
                        if token in constants._ENTITIES:
                            argument = rev_tg_full_vocab[full_outputs[ii]]
                            if argument.startswith('__LF__'):
                                argument = argument[len('__LF__'):]
                            pred = tokens[ii]
                            if constants.remove_quotation(argument) == \
                                    constants.remove_quotation(pred):
                                num_correct_argument += 1
                            print(constants.remove_quotation(argument),
                                  constants.remove_quotation(pred))
                            num_argument += 1

        precision = num_correct_align / num_predict_align
        recall = num_correct_align / num_gt_align
        print("Argument Alignment Precision: {}".format(precision))
        print("Argument Alignment Recall: {}".format(recall))
        print("Argument Alignment F1: {}".format(
            2 * precision * recall / (precision + recall)))

        print("Argument filling accuracy: {}".format(
            num_correct_argument / num_argument))


def gen_slot_filling_training_data(train_set, dev_set):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        decoding_algorithm = FLAGS.decoding_algorithm
        FLAGS.decoding_algorithm = 'greedy'
        FLAGS.force_reading_input = True

        # Create model and load parameters.
        model = create_model(sess, forward_only=True)

        # Save slot filling embeddings.
        mapping_path = os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz')
        gen_slot_filling_training_data_fun(sess, model, train_set, mapping_path)
        mapping_path = os.path.join(FLAGS.model_dir, 'dev.mappings.X.Y.npz')
        gen_slot_filling_training_data_fun(sess, model, dev_set, mapping_path)

        FLAGS.decoding_algorithm = decoding_algorithm
        FLAGS.force_reading_input = False

def gen_slot_filling_training_data_fun(sess, model, dataset, output_file):
    print("saving slot filling mappings to {}".format(output_file))

    X, Y = [], []
    for bucket_id in xrange(len(_buckets)):
        for i in xrange(len(dataset[bucket_id])):
            dp = dataset[bucket_id][i]
            if dp.mappings:
                mappings = [tuple(m) for m in dp.mappings]
                encoder_channel_inputs = [[dp.sc_ids], [dp.sc_full_ids]]
                decoder_channel_inputs = [[dp.tg_ids], [dp.tg_full_ids]]
                if FLAGS.use_copy:
                    encoder_channel_inputs.append([dp.sc_copy_full_ids])
                    pointer_targets = [dp.pointer_targets]
                else:
                    pointer_targets = None
                formatted_example = model.format_example(
                    encoder_channel_inputs, decoder_channel_inputs,
                    pointer_targets=pointer_targets,
                    bucket_id=bucket_id)
                model_outputs = model.step(
                    sess, formatted_example, bucket_id, forward_only=True)
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

            if len(X) > 0 and len(X) % 1000 == 0:
                print('{} examples gathered for generating slot filling features...'
                      .format(len(X)))

    np.savez(output_file, [X, Y])

# --- Pre-processing --- #

def load_data(use_buckets=True, load_mappings=True, load_pointers=True):
    if use_buckets:
        return data_utils.load_data(FLAGS, _buckets,
                                    load_mappings=load_mappings,
                                    load_pointers=load_pointers)
    else:
        return data_utils.load_data(FLAGS, None,
                                    load_mappings=load_mappings,
                                    load_pointers=load_pointers)


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

    # set up source and target length
    FLAGS.max_sc_length = FLAGS.max_sc_length \
        if not _buckets else _buckets[-1][0]
    FLAGS.max_tg_length = FLAGS.max_tg_length \
        if not _buckets else _buckets[-1][1]

    # set up encoder/decider dropout rate
    if FLAGS.universal_keep >= 0 and FLAGS.universal_keep < 1:
        FLAGS.sc_input_keep = FLAGS.universal_keep
        FLAGS.sc_output_keep = FLAGS.universal_keep
        FLAGS.tg_input_keep = FLAGS.universal_keep
        FLAGS.tg_output_keep = FLAGS.universal_keep
        FLAGS.attention_input_keep = FLAGS.universal_keep
        FLAGS.attention_output_keep = FLAGS.universal_keep

    # set up source and target vocabulary size
    FLAGS.sc_token_embedding_size = FLAGS.cm_known_vocab_size \
        if FLAGS.explain else FLAGS.nl_known_vocab_size
    FLAGS.sc_vocab_size = FLAGS.cm_vocab_size \
        if FLAGS.explain else FLAGS.nl_vocab_size
    FLAGS.tg_token_embedding_size = FLAGS.nl_known_vocab_size \
        if FLAGS.explain else FLAGS.cm_known_vocab_size
    FLAGS.tg_vocab_size = FLAGS.nl_vocab_size \
        if FLAGS.explain else FLAGS.cm_vocab_size

    # adjust hyperparameters for batch normalization
    if FLAGS.recurrent_batch_normalization:
        # larger batch size
        FLAGS.batch_size *= 4
        # larger initial learning rate
        FLAGS.learning_rate *= 10

    if FLAGS.decoder_topology in ['basic_tree']:
        FLAGS.model_root_dir = os.path.join(
            os.path.dirname(__file__), "..", FLAGS.model_root_dir, "seq2tree")
    elif FLAGS.decoder_topology in ['rnn']:
        FLAGS.model_root_dir = os.path.join(
            os.path.dirname(__file__), "..", FLAGS.model_root_dir, "seq2seq")
    else:
        raise ValueError("Unrecognized decoder topology: {}."
                         .format(FLAGS.decoder_topology))
    print("Saving models to {}".format(FLAGS.model_root_dir))

    if FLAGS.data_stats:
        data_statistics()
    elif FLAGS.process_data:
        process_data()

    elif FLAGS.write_predictions_to_file:
        write_predictions_to_file(os.path.join(FLAGS.data_dir, '..', 'reader',
            'data.final0502', 'test.3112.cm'), 'test.3112.explain')

    elif FLAGS.eval_local_slot_filling:
        train_path = os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz')
        dev_path = os.path.join(FLAGS.model_dir, 'dev.mappings.X.Y.npz')
        eval_local_slot_filling(train_path, dev_path)

    elif FLAGS.demo:
        demo()

    else:
        train_set, dev_set, test_set = load_data(
            load_mappings=FLAGS.dataset.startswith("bash"),
            load_pointers=FLAGS.dataset.startswith("bash"))
        dataset = test_set if FLAGS.test else dev_set
        if FLAGS.gen_eval_sheet:
            gen_eval_sheet(dataset)
        elif FLAGS.eval:
            eval(dataset, verbose=True)
        elif FLAGS.manual_eval:
            manual_eval(dataset, 100)
        elif FLAGS.eval_slot_filling:
            eval_slot_filling(dataset)
        elif FLAGS.decode:
            tf.reset_default_graph()
            gen_slot_filling_training_data(train_set, dev_set)

            model_dir, decode_sig = decode(dataset)
            if not FLAGS.explain:
                eval(dataset, model_dir, decode_sig, verbose=False)
        elif FLAGS.grid_search:
            meta_experiments.grid_search(
                train, decode, eval, train_set, dataset, FLAGS)
        elif FLAGS.schedule_experiments:
            schedule_experiments(
                train, decode, eval, train_set, dataset)
        elif FLAGS.cross_valid:
            cross_validation(train_set)
        else:
            # Train the model.
            train(train_set, dataset)

            # Decode the new model on the development set.
            tf.reset_default_graph()
            model_dir, decode_sig = decode(dataset)

            # Run automatic evaluation on the development set.
            if not FLAGS.explain:
                eval(dataset, model_dir, decode_sig, verbose=False)

    
if __name__ == "__main__":
    tf.app.run()
