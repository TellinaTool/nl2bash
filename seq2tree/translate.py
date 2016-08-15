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
sys.path.append("../seq2seq")

import time
import cPickle as pickle

import numpy as np
from random import shuffle

import tensorflow as tf

import data_utils
from argparse import define_input_flags
from bash import basic_tokenizer, bash_tokenizer
from normalizer import to_list, list_to_tree, to_command, pretty_print, normalize_ast
from seq2tree_model import Seq2TreeModel
from token_overlap import TokenOverlap

FLAGS = tf.app.flags.FLAGS

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
    params = collections.defaultdict()
    params["source_vocab_size"] = FLAGS.nl_vocab_size
    params["target_vocab_size"] = FLAGS.cm_vocab_size
    params["max_source_length"] = FLAGS.max_nl_length
    params["max_target_length"] = FLAGS.max_cm_length
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

def train(train_set, dev_set, num_epochs):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model = create_model(sess, False)

        loss, dev_loss, epoch_time = 0.0, 0.0, 0.0
        current_step = 0
        previous_losses = []
        previous_dev_losses = []

        # Load Vocabularies for evaluation on dev set at each checkpoint
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        for t in xrange(num_epochs):

            start_time = time.time()

            # shuffling training examples
            shuffle(train_set)

            for i in xrange(len(train_set)):
                nl, tree = train_set[i]
                encoder_inputs, decoder_inputs, target_weights = model.format_example(
                    nl, tree)
                _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                             target_weights, forward_only=False)
                loss += step_loss
                current_step += 1

            epoch_time = time.time() - start_time

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.iters_per_checkpoint == 0:
                print("Epoch %d" % t)

                # Print statistics for the previous epoch.
                loss /= len(train_set)
                ppx = math.exp(loss) if loss < 300 else float('inf')
                print("learning rate %.4f epoch-time %.2f perplexity %.2f" % (
                    model.learning_rate.eval(), epoch_time, ppx))

                # Decrease learning rate if no improvement of loss was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)
                previous_losses.append(loss)

                # Save checkpoint and zero timer and loss.
                checkpoint_path = os.path.join(FLAGS.train_dir, "translate.ckpt")
                model.saver.save(sess, checkpoint_path, num_epochs=t)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0

                # Run evals on development set and print the metrics.
                for i in xrange(len(dev_set)):
                    nl, tree = dev_set[i]
                    encoder_inputs, decoder_inputs, target_weights = model.format_example(
                        nl, tree)
                    _, eval_loss, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                                             target_weights, forward_only=True)
                    dev_loss += eval_loss
                dev_loss /= len(dev_set)
                dev_ppx = math.exp(dev_loss) if dev_loss < 300 else float('int')
                print("dev perplexity %.2f" % dev_ppx)

                # Early stop if no improvement of dev loss was seen over last 3 checkpoints.
                if len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[:-3]):
                    return False
                previous_dev_losses.append(dev_loss)

                eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, False)

                sys.stdout.flush()
    return True


def decode(logits, rev_cm_vocab):
    if FLAGS.decoding_algorithm == "greedy":
        outputs = [int(np.argmax(logit, axis=1)) for logit in logits]
    tree = list_to_tree([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs])
    cmd = to_command(tree)
    return tree, cmd


def decode():
    """
    Simple command line decoding interface.
    """
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        nl_vocab, _ = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)

        # Decode from standard input.
        sys.stdout.write("> ")
        sys.stdout.flush()
        sentence = sys.stdin.readline()

        while sentence:
            # Get token-ids for the input sentence.
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                         basic_tokenizer)

            # Get a 1-element batch to feed the sentence to the model.
            encoder_inputs, decoder_inputs, target_weights = model.format_example(
                token_ids, [data_utils._ROOT])

            # Get output logits for the sentence.
            _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                             target_weights, forward_only=True)
            tree, cmd = decode(output_logits, rev_cm_vocab)
            pretty_print(cmd)

            print("> ", end="")
            sys.stdout.flush()
            sentence = sys.stdin.readline()


def eval_set(sess, model, dataset, rev_nl_vocab, rev_cm_vocab, verbose=True):
    total_score = 0.0
    num_correct = 0.0
    num_eval = 0

    for i in xrange(len(dataset)):
        nl, tree = dataset[i]

        encoder_inputs, decoder_inputs, target_weights = model.format_example(
            nl, [data_utils._ROOT])
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, forward_only=True)

        rev_encoder_inputs = []
        for i in xrange(len(encoder_inputs)-1, -1, -1):
            rev_encoder_inputs.append(encoder_inputs[i])
        sentence = data_utils.token_ids_to_sentences(rev_encoder_inputs, rev_nl_vocab)[0]
        ground_truth = data_utils.token_ids_to_sentences(decoder_inputs, rev_cm_vocab,
                                               headAppended=False)[0]
        prediction = decode(output_logits, rev_cm_vocab)
        score = TokenOverlap.compute(ground_truth, prediction, verbose)
        total_score += score
        if score == 1:
            num_correct += 1
        num_eval += 1
        if verbose:
            print("Example %d" % num_eval)
            print("English: " + sentence)
            print("Ground truth: " + ground_truth)
            print("Prediction: " + prediction)
            print("token-overlap score: %.2f" % score)
            print()

    print("%d examples evaluated" % num_eval)
    print("Accuracy = %.2f" % (num_correct/num_eval))
    print("Average token-overlap score = %.2f" % (total_score/num_eval))
    print()


def eval(verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = process_data()

        eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose)


"""def train_and_eval(train_set, dev_set):
    num_iter = FLAGS.steps_per_milestone
    for i in xrange(FLAGS.num_milestones):
        is_learning = train(train_set, dev_set, num_iter)
        tf.reset_default_graph()
        eval(False)
        tf.reset_default_graph()
        if not is_learning:
            print("Training stopped early for no improvement observed on dev set.")
            break
"""


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)

    with open(FLAGS.data_dir + "data.dat") as f:
        data = pickle.load(f)

    numFolds = len(data)
    print("%d folds" % numFolds)

    train_cm_list = []
    train_nl_list = []
    dev_cm_list = []
    dev_nl_list = []
    test_cm_list = []
    test_nl_list = []
    for i in xrange(numFolds):
        if i < numFolds - 2:
            for nl, cmd in data[i]:
                ast = normalize_ast(cmd)
                train_cm_list.append(to_list(ast))
                train_nl_list.append(nl)
        elif i == numFolds - 2:
            for nl, cmd in data[i]:
                ast = normalize_ast(cmd)
                dev_cm_list.append(to_list(ast))
                dev_nl_list.append(nl)
        elif i == numFolds - 1:
            for nl, cmd in data[i]:
                ast = normalize_ast(cmd)
                test_cm_list.append(to_list(ast))
                test_nl_list.append(nl)

    train_dev_test = {}
    train_dev_test["train"] = [train_cm_list, train_nl_list]
    train_dev_test["dev"] = [dev_cm_list, dev_nl_list]
    train_dev_test["test"] = [test_cm_list, test_nl_list]

    nl_train, cm_train, nl_dev, cm_dev, nl_test, cm_test, _, _ = data_utils.prepare_data(
        train_dev_test, FLAGS.data_dir, FLAGS.nl_vocab_size, FLAGS.cm_vocab_size)

    train_set = read_data(nl_train, cm_train, FLAGS.max_train_data_size)
    dev_set = read_data(nl_dev, cm_dev)
    test_set = read_data(nl_test, nl_test)

    with open(FLAGS.data_dir + "seq2tree/" + "data.processed.dat", 'wb') as o_f:
        pickle.dump((train_set, dev_set, test_set), o_f)
    return train_set, dev_set, test_set


def load_data():
    print("Loading data from %s" % FLAGS.data_dir)

    with open(FLAGS.data_dir + "data.processed.dat", 'rb') as f:
        return pickle.load(f)


def read_data(source_path, target_path, max_size=None):
    """Read data from source and target files and put into buckets.
    :param source_path: path to the file with token-ids for the source language.
    :param target_path: path to the file with token-ids for the target language.
    :param max_size: maximum number of lines to read. Read complete data files if
        this entry is 0 or None.
    """
    data_set = []

    with tf.gfile.GFile(source_path, mode="r") as source_file:
        with tf.gfile.GFile(target_path, mode="r") as target_file:
            source, target = source_file.readline(), target_file.readline()
            counter = 0
            while source and target and (not max_size or counter < max_size):
                counter += 1
                if counter % 1000 == 0:
                    print("  reading data line %d" % counter)
                    sys.stdout.flush()
                source_ids = [int(x) for x in source.split()]
                target_ids = [int(x) for x in target.split()]
                data_set.append([source_ids, target_ids])
                source, target = source_file.readline(), target_file.readline()
    print("  %d data points read." % len(data_set))
    return data_set


def main(_):
    # set GPU device
    with tf.device('/gpu:%d' % FLAGS.gpu):
        if FLAGS.eval:
            eval()
        elif FLAGS.decode:
            decode()
        elif FLAGS.process_data:
            process_data()
        else:
            train_set, dev_set, _ = load_data()
            train(train_set, dev_set)


if __name__ == "__main__":
    define_input_flags()
    tf.app.run()