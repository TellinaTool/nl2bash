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
from tqdm import tqdm
from random import sample

import tensorflow as tf

import data_utils
from parse_args import define_input_flags
from data_tools import basic_tokenizer, bash_tokenizer, to_template
from normalizer import to_list, to_ast, to_command, pretty_print, normalize_ast
from encoder_decoder import Seq2TreeModel
import ast_based 

FLAGS = tf.app.flags.FLAGS

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
_buckets = [(5, 10), (10, 20), (20, 30), (30, 40), (40, 50)]

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
    params["use_attention"] = FLAGS.use_attention
    params["use_copy"] = FLAGS.use_copy

    params["decoder_topology"] = FLAGS.decoder_topology
    params["decoding_algorithm"] = FLAGS.decoding_algorithm
    model = Seq2TreeModel(params, forward_only)

    ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
    global_epochs = int(ckpt.model_checkpoint_path.rsplit('-')[-1]) if ckpt else 0
    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print("Created model with fresh parameters.")
        session.run(tf.initialize_all_variables())
    return model, global_epochs

def train(train_set, dev_set, verbose=False):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model.
        model, global_epochs = create_model(sess, forward_only=False)

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

        # dev_set = train_set + dev_set
        for t in xrange(FLAGS.num_epochs):
            print("Epoch %d" % t)

            start_time = time.time()

            # shuffling training examples
            random.shuffle(train_set)

            for i in tqdm(xrange(len(train_set))):
                time.sleep(0.01)
                _, _, nl, tree = train_set[i]
                formatted_example = model.format_example(nl, tree)
                _, step_loss, _ = model.step(sess, formatted_example, forward_only=False)
                loss += step_loss
                current_step += 1

            epoch_time = time.time() - start_time

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if t % FLAGS.epochs_per_checkpoint == 0:

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
                model.saver.save(sess, checkpoint_path, global_step=global_epochs+t+1)

                epoch_time, loss, dev_loss = 0.0, 0.0, 0.0

                # Run evals on development set and print the metrics.
                for i in xrange(len(dev_set)):
                    nl_str, cm_str, nl, tree = dev_set[i]
                    formatted_example = model.format_example(nl, tree)
                    _, eval_loss, output_logits = model.step(sess, formatted_example, forward_only=True)
                    dev_loss += eval_loss
                dev_loss /= len(dev_set)
                dev_ppx = math.exp(dev_loss) if dev_loss < 300 else float('int')
                print("dev perplexity %.2f" % dev_ppx)
                print()

                eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose=False)

                # Early stop if no improvement of dev loss was seen over last 2 checkpoints.
                if ppx < 1.1 and len(previous_dev_losses) > 2 and dev_loss > max(previous_dev_losses[-2:]):
                    return False
                previous_dev_losses.append(dev_loss)

                sys.stdout.flush()
      
    return True


def decode(logits, rev_cm_vocab):
    outputs = [int(np.argmax(logit, axis=1)) for logit in logits]
    return to_readable(outputs, rev_cm_vocab)


def to_readable(outputs, rev_cm_vocab):
    search_history = [data_utils._ROOT] + [tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]
    tree = to_ast(search_history)
    cmd = to_command(tree, loose_constraints=True)
    return tree, cmd, search_history


def interactive_decode():
    """
    Simple command line decoding interface.
    """
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, True)

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
            formatted_example = model.format_example(token_ids, [data_utils.ROOT_ID])

            # Get output logits for the sentence.
            _, _, output_logits = model.step(sess, formatted_example, forward_only=True)
            if FLAGS.decoding_algorithm == "greedy":
                tree, cmd, search_history = decode(output_logits, rev_cm_vocab)
                print()
                print(cmd)
                print()
                pretty_print(tree, 0)
                print()
                # print("->".join(search_history[:20]))
                # print()
            elif FLAGS.decoding_algorithm == "beam_search":
                top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
                print()
                for i in xrange(FLAGS.top_k):
                    outputs = top_k_search_histories[i]
                    tree, cmd, search_history = to_readable(outputs, rev_cm_vocab)
                    print("prediction %d (%.2f): " % (i, decode_scores[i]) + cmd)
                    print()
                    pretty_print(tree, 0)
                    print()
                    # print("->".join(search_history[:20]))
                    # print()

            print("> ", end="")
            sys.stdout.flush()
            sentence = sys.stdin.readline()

def group_data_by_desp(dataset):
    grouped_dataset = {}

    for i in xrange(len(dataset)):
        nl_str, cm_str, nl, search_history = dataset[i]
        if nl_str in grouped_dataset:
            grouped_dataset[nl_str][0].append(cm_str)
            grouped_dataset[nl_str][2].append(search_history)
        else:
            grouped_dataset[nl_str] = [[cm_str], nl, [search_history]]

    grouped_dataset2 = []
    for nl_str in grouped_dataset:
        grouped_dataset2.append((nl_str, grouped_dataset[nl_str][0],
                                grouped_dataset[nl_str][1],
                                grouped_dataset[nl_str][2]))
    return grouped_dataset2

def eval_set(sess, model, dataset, rev_nl_vocab, rev_cm_vocab, verbose=True):
    num_top_k_correct_template = 0.0
    num_top_k_correct = 0.0
    num_correct_template = 0.0
    num_correct = 0.0
    num_eval = 0

    grouped_dataset = group_data_by_desp(dataset)

    for i in xrange(len(grouped_dataset)):
        nl_str, cm_strs, nl, search_historys = grouped_dataset[i]
      
        formatted_example = model.format_example(
            nl, [data_utils.ROOT_ID])
        _, _, output_logits = model.step(sess, formatted_example, forward_only=True)

        sentence = ' '.join([rev_nl_vocab[i] for i in nl])
        gt_trees = [normalize_ast(cmd) for cmd in cm_strs]
        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, search_history = decode(output_logits, rev_cm_vocab)
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            top_k_pred_trees = []
            top_k_pred_cmds = []
            for j in xrange(FLAGS.top_k-1, -1, -1):
                tree, pred_cmd, search_history = to_readable(top_k_search_histories[i], rev_cm_vocab)
                top_k_pred_trees.insert(0, tree)
                top_k_pred_cmds.insert(0, pred_cmd)
                if ast_based.one_template_match(gt_trees, tree):
                    num_top_k_correct_template += 1
                if ast_based.one_string_match(gt_trees, tree):
                    num_top_k_correct += 1
        # evaluation ignoring ordering of flags
        if ast_based.one_template_match(gt_trees, tree):
            num_correct_template += 1
        if ast_based.one_string_match(gt_trees, tree):
            num_correct += 1
        num_eval += 1

        if verbose:
            print("Example %d (%d)" % (num_eval, len(cm_strs)))
            print("Original English: " + nl_str.strip())
            print("English: " + sentence)
            print("Original Command: " + cm_strs[0].strip())
            print("Ground truth: " + to_command(gt_trees[0]))
            if FLAGS.decoding_algorithm == "greedy":
                print("Prediction: " + pred_cmd)
                # print("Search history (truncated at 25 steps): ")
                # print(" -> ".join(search_historys[0][:25]))
                print("AST: ")
                pretty_print(tree, 0)
                print()
                # print("token-overlap score: %.2f" % score)
                # print()
            elif FLAGS.decoding_algorithm == "beam_search":
                for j in xrange(FLAGS.top_k):
                    print("Prediction %d: " % (j+1) + top_k_pred_cmds[j])
                    print("AST: ")
                    pretty_print(top_k_pred_trees[j], 0)
                    print()

    print("%d examples evaluated" % num_eval)
    print("Percentage of Template Match = %.2f" % (num_correct_template/num_eval))
    print("Percentage of String Match = %.2f" % (num_correct/num_eval))
    print()


def eval(verbose=True):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        eval_set(sess, model, dev_set, rev_nl_vocab, rev_cm_vocab, verbose)


def manual_eval(num_eval = 30):
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                          log_device_placement=FLAGS.log_device_placement)) as sess:
        # Create model and load parameters.
        model, _ = create_model(sess, forward_only=True)

        # Load vocabularies.
        nl_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.nl" % FLAGS.nl_vocab_size)
        cm_vocab_path = os.path.join(FLAGS.data_dir,
                                     "vocab%d.cm" % FLAGS.cm_vocab_size)
        _, rev_nl_vocab = data_utils.initialize_vocabulary(nl_vocab_path)
        _, rev_cm_vocab = data_utils.initialize_vocabulary(cm_vocab_path)
        _, dev_set, _ = load_data()

        num_correct_template = 0.0
        num_correct_command = 0.0

        grouped_dataset = group_data_by_desp(dev_set)
        random.shuffle(grouped_dataset)

        o_f = open("manual.eval.results", 'w')

        num_evaled = 0

        for i in xrange(len(grouped_dataset)):
            if num_evaled == num_eval:
                break

            nl_str, cm_strs, nl, search_historys = grouped_dataset[i]

            formatted_example = model.format_example(
                nl, [data_utils.ROOT_ID])
            _, _, output_logits = model.step(sess, formatted_example, forward_only=True)

            gt_trees = [normalize_ast(cmd) for cmd in cm_strs]
            if FLAGS.decoding_algorithm == "greedy":
                tree, pred_cmd, search_history = decode(output_logits, rev_cm_vocab)
            else:
                top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
                top_k_pred_trees = []
                top_k_pred_cmds = []
                for j in xrange(FLAGS.top_k):
                    tree, pred_cmd, search_history = to_readable(top_k_search_histories[j], rev_cm_vocab)
                    top_k_pred_trees.append(tree)
                    top_k_pred_cmds.append(pred_cmd)
            # evaluation ignoring ordering of flags
            if ast_based.one_template_match(gt_trees, tree):
                continue
            else:
                print("Example %d (%d)" % (num_evaled+1, len(cm_strs)))
                o_f.write("Example %d (%d)" % (num_evaled+1, len(cm_strs)) + "\n")
                print("English: " + nl_str.strip())
                o_f.write("English: " + nl_str.strip() + "\n")
                for j in xrange(len(cm_strs)):
                    print("GT Command %d: " % (j+1) + cm_strs[j].strip())
                    o_f.write("GT Command %d: " % (j+1) + cm_strs[j].strip() + "\n")
                if FLAGS.decoding_algorithm == "greedy":
                    print("Prediction: " + pred_cmd)
                    o_f.write("Prediction: " + pred_cmd + "\n")
                    print("AST: ")
                    pretty_print(tree, 0)
                    print()
                elif FLAGS.decoding_algorithm == "beam_search":
                    for j in xrange(FLAGS.top_k):
                        decode_score = decode_scores[j]
                        tree = top_k_pred_trees[j]
                        pred_cmd = top_k_pred_cmds[j]
                        print("Prediction %d (%.2f): " % (j+1, decode_score) + pred_cmd)
                        print("AST: ")
                        pretty_print(tree, 0)
                        print()
                inp = raw_input("Correct template [y/n]: ")
                if inp == "y":
                    num_correct_template += 1
                    o_f.write("C")
                    inp = raw_input("Correct command [y/n]: ")
                    if inp == "y":
                        num_correct_command += 1
                        o_f.write("C")
                    else:
                        o_f.write("W")
                else:
                    o_f.write("WW")
                o_f.write("\n")
                o_f.write("\n")

            num_evaled += 1

        print()
        print("%d examples evaluated" % num_eval)
        print("Percentage of Template Match = %.2f" % (num_correct_template/num_eval))
        print("Percentage of String Match = %.2f" % (num_correct_command/num_eval))
        print()

        o_f.write("\n")
        o_f.write("%d examples evaluated" % num_eval + "\n")
        o_f.write("Percentage of Template Match = %.2f" % (num_correct_template/num_eval) + "\n")
        o_f.write("Percentage of String Match = %.2f" % (num_correct_command/num_eval) + "\n")
        o_f.write("\n")


def process_data():
    print("Preparing data in %s" % FLAGS.data_dir)

    with open(FLAGS.data_dir + "data.by.template.dat") as f:
        data = pickle.load(f)

    numFolds = len(data)
    print("%d folds" % numFolds)

    output_dir = os.path.join(FLAGS.data_dir, "seq2tree.by.%s" % FLAGS.data_split)
    data_utils.prepare_data(data, output_dir, FLAGS.nl_vocab_size, FLAGS.cm_vocab_size)


def load_data(sample_size=-1):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = os.path.join(FLAGS.data_dir, "seq2tree.by.%s" % FLAGS.data_split)
    nl_train =

    train_set = read_data(nl_train, cm_train, FLAGS.max_train_data_size)
    dev_set = read_data(nl_dev, cm_dev)
    test_set = read_data(nl_test, cm_test)

    with open(data_dir + "data.processed.dat", 'wb') as o_f:
        pickle.dump((train_set, dev_set, test_set), o_f)


def read_data(source_path, target_path, max_size=None):
    """Read data from source and target files and put into buckets.
    :param source_path: path to the file with token-ids for the source language.
    :param target_path: path to the file with token-ids for the target language.
    :param max_size: maximum number of lines to read. Read complete data files if
        this entry is 0 or None.
    """
    data_set = []

    source_txt_path = '.'.join([source_path.rsplit('.', 2)[0], source_path.rsplit('.', 2)[2]])
    target_txt_path = '.'.join([target_path.rsplit('.', 2)[0], target_path.rsplit('.', 2)[2]])
    with tf.gfile.GFile(source_txt_path, mode="r") as source_txt_file:
        with tf.gfile.GFile(target_txt_path, mode="r") as target_txt_file:
            with tf.gfile.GFile(source_path, mode="r") as source_file:
                with tf.gfile.GFile(target_path, mode="r") as target_file:
                    source_txt, target_txt = source_txt_file.readline(), target_txt_file.readline()
                    source, target = source_file.readline(), target_file.readline()
                    counter = 0
                    while source:
                        assert(target)
                        if max_size and counter < max_size:
                            break
                        counter += 1
                        if counter % 1000 == 0:
                            print("  reading data line %d" % counter)
                            sys.stdout.flush()
                        source_ids = [int(x) for x in source.split()]
                        target_ids = [int(x) for x in target.split()]
                        data_set.append([source_txt, target_txt, source_ids, target_ids])
                        source_txt, target_txt = source_txt_file.readline(), target_txt_file.readline()
                        source, target = source_file.readline(), target_file.readline()
    print("  %d data points read." % len(data_set))
    return data_set


def main(_):
    # set GPU device
    os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.gpu)

    # train_set, dev_set, test_set = load_data()
    # print(len(group_data_by_desp(train_set)))
    # print(len(group_data_by_desp(dev_set)))
    # print(len(group_data_by_desp(test_set)))

    with tf.device('/gpu:%d' % FLAGS.gpu):
        if FLAGS.eval:
            eval()
        elif FLAGS.manual_eval:
            manual_eval()
        elif FLAGS.decode:
            interactive_decode()
        elif FLAGS.process_data:
            process_data()
        elif FLAGS.sample_train:
            train_set, dev_set, _ = load_data(FLAGS.sample_size)
            train(train_set, dev_set)
        else:
            train_set, dev_set, _ = load_data()
            train(train_set, dev_set, verbose=False)


if __name__ == "__main__":
    define_input_flags()
    tf.app.run()
