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
import pickle
import time
from tqdm import tqdm

import tensorflow as tf

from encoder_decoder import data_utils
from encoder_decoder import decode_tools
from encoder_decoder import graph_utils
from encoder_decoder import meta_experiments
from encoder_decoder import parse_args
from encoder_decoder import slot_filling
from .seq2seq.seq2seq_model import Seq2SeqModel
from .seq2tree.seq2tree_model import Seq2TreeModel
from eval import eval_tools

# Refer to parse_args.py for model parameter explanations
FLAGS = tf.app.flags.FLAGS
parse_args.define_input_flags()

# --- Define models --- #

def define_model(session, forward_only, buckets=None):
    """
    Define tensor graphs.
    """
    if FLAGS.decoder_topology in ['basic_tree']:
        return graph_utils.define_model(
            FLAGS, session, Seq2TreeModel, buckets, forward_only)
    elif FLAGS.decoder_topology in ['rnn']:
        return graph_utils.define_model(
            FLAGS, session, Seq2SeqModel, buckets, forward_only)
    else:
        raise ValueError("Unrecognized decoder topology: {}.".format(
            FLAGS.decoder_topology))

# --- Run experiments --- #

def train(train_set, test_set):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        # Initialize model parameters
        model = define_model(sess, forward_only=False, buckets=train_set.buckets)

        train_bucket_sizes = [len(train_set.data_points[b])
                              for b in xrange(len(train_set.buckets))]
        for i, bucket in enumerate(train_set.buckets):
            print('bucket {}: {} ({})'.format(i, bucket, train_bucket_sizes[i]))
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
                formatted_example = model.get_batch(train_set.data_points, bucket_id)
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
                sample_size = 10
                repeated_samples = list(range(len(train_set.buckets))) * sample_size
                for bucket_id in repeated_samples:
                    if len(test_set.data_points[bucket_id]) == 0:
                        print("  eval: empty bucket %d" % (bucket_id))
                        continue
                    formatted_example = model.get_batch(test_set.data_points, bucket_id)
                    model_outputs = model.step(
                        sess, formatted_example, bucket_id, forward_only=True)
                    eval_loss = model_outputs.losses
                    dev_loss += eval_loss
                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))
                dev_loss = dev_loss / len(repeated_samples)

                dev_perplexity = math.exp(dev_loss) if dev_loss < 1000 else float('inf')
                print("step %d learning rate %.4f dev_perplexity %.2f"
                        % (t+1, model.learning_rate.eval(), dev_perplexity))

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-3:]):
                    break
           
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()

        return model


def decode(data_set, buckets=None, verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        # Initialize model parameters.
        model = define_model(sess, forward_only=True, buckets=buckets)
        decode_tools.decode_set(sess, model, data_set, 3, FLAGS, verbose)
        return model


def eval(data_set, model_dir=None, decode_sig=None, verbose=True):
    if model_dir is None:
        model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
        model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    print("evaluating " + model_dir)

    return eval_tools.eval_set(model_dir, decode_sig, data_set, 3, FLAGS, 
        verbose=verbose)


def demo(buckets=None):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
        log_device_placement=FLAGS.log_device_placement)) as sess:
        # Initialize model parameters.
        model = define_model(sess, forward_only=True, buckets=buckets)
        decode_tools.demo(sess, model, FLAGS)


def save_hyperparameters():
    model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
    with open(os.path.join(FLAGS.model_root_dir, model_subdir, 'hyperparameters.pkl'), 'wb') as o_f:
        pickle.dump(FLAGS, o_f)


def gen_slot_filling_training_data(FLAGS, datasets):
    # Set hyperparameters
    token_decoding_algorithm = FLAGS.token_decoding_algorithm
    FLAGS.token_decoding_algorithm = 'greedy'
    FLAGS.force_reading_input = True

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
            log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        train_set, dev_set, test_set = datasets
        model = define_model(sess, forward_only=True, buckets=train_set.buckets)
        # Save slot filling embeddings.
        slot_filling.gen_slot_filling_training_data(sess, FLAGS, model, train_set,
            os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz'))
        slot_filling.gen_slot_filling_training_data(sess, FLAGS, model, dev_set,
            os.path.join(FLAGS.model_dir, 'dev.mappings.X.Y.npz'))
        slot_filling.gen_slot_filling_training_data(sess, FLAGS, model, test_set,
            os.path.join(FLAGS.model_dir, 'test.mappings.X.Y.npz'))

    # Restore hyperparameters
    FLAGS.token_decoding_algorithm = token_decoding_algorithm
    FLAGS.force_reading_input = False


def gen_error_analysis_sheets(dataset, model_dir=None, decode_sig=None,
                              group_by_utility=False):
    if model_dir is None:
        model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
        model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    if group_by_utility:
        eval_tools.gen_error_analysis_csv_by_utility(
            model_dir, decode_sig, dataset, FLAGS)
    else:
        eval_tools.gen_error_analysis_csv(
            model_dir, decode_sig, dataset, FLAGS)


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

# --- Pre-processing --- #

def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)
    data_utils.prepare_data(FLAGS)


def main(_):
    # set GPU device
    os.environ["CUDA_VISIBLE_DEVICES"] = FLAGS.gpu
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
 
    # set up data and model directories
    FLAGS.data_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", FLAGS.dataset)
    print("Reading data from {}".format(FLAGS.data_dir))

    # set up encoder/decider dropout rate
    if FLAGS.universal_keep >= 0 and FLAGS.universal_keep < 1:
        FLAGS.sc_input_keep = FLAGS.universal_keep
        FLAGS.sc_output_keep = FLAGS.universal_keep
        FLAGS.tg_input_keep = FLAGS.universal_keep
        FLAGS.tg_output_keep = FLAGS.universal_keep
        FLAGS.attention_input_keep = FLAGS.universal_keep
        FLAGS.attention_output_keep = FLAGS.universal_keep

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

    if FLAGS.process_data:
        process_data()

    else:
        train_set, dev_set, test_set = \
            data_utils.load_data(FLAGS, use_buckets=True, load_mappings=False)
        vocab = data_utils.load_vocabulary(FLAGS)

        print("Set dataset parameters")
        FLAGS.max_sc_length = train_set.max_sc_length if not train_set.buckets else \
            train_set.buckets[-1][0]
        FLAGS.max_tg_length = train_set.max_tg_length if not train_set.buckets else \
            train_set.buckets[-1][1]
        FLAGS.sc_vocab_size = len(vocab.sc_vocab)
        FLAGS.tg_vocab_size = len(vocab.tg_vocab)
        FLAGS.max_sc_token_size = vocab.max_sc_token_size
        FLAGS.max_tg_token_size = vocab.max_tg_token_size

        dataset = test_set if FLAGS.test else dev_set
        if FLAGS.eval:
            eval(dataset)
            save_hyperparameters()
        elif FLAGS.gen_error_analysis_sheet:
            gen_error_analysis_sheets(dataset, group_by_utility=True)
        elif FLAGS.gen_manual_evaluation_sheet:
            eval_tools.gen_manual_evaluation_csv(dataset, FLAGS)
        elif FLAGS.gen_manual_evaluation_sheet_single_model:
            eval_tools.gen_manual_evaluation_csv_single_model(dataset, FLAGS)
        elif FLAGS.gen_manual_evaluation_table:
            eval_tools.gen_manual_evaluation_table(dataset, FLAGS)

        elif FLAGS.gen_slot_filling_training_data:
            gen_slot_filling_training_data(FLAGS, [train_set, dev_set, test_set])

        elif FLAGS.decode:
            model = decode(dataset, buckets=train_set.buckets)
            if not FLAGS.explain:
                eval(dataset, model.model_dir, model.decode_sig, verbose=False)

        elif FLAGS.demo:
            demo(buckets=train_set.buckets)

        elif FLAGS.grid_search:
            meta_experiments.grid_search(
                train, decode, eval, train_set, dataset, FLAGS)
        elif FLAGS.schedule_experiments:
            schedule_experiments(
                train, decode, eval, train_set, dataset)
        else:
            # Train the model.
            train(train_set, dataset)

            if FLAGS.normalized:
                tf.reset_default_graph()
                gen_slot_filling_training_data(FLAGS, [train_set, dev_set, test_set])
                FLAGS.fill_argument_slots = True

            # save model hyperparameters
            save_hyperparameters() 

            # Decode the new model on the development set.
            tf.reset_default_graph()
            model = decode(dataset, buckets=train_set.buckets)

            # Run automatic evaluation on the development set.
            if not FLAGS.explain:
                eval(dataset, model.model_dir, model.decode_sig, verbose=False)

    
if __name__ == "__main__":
    tf.app.run()
