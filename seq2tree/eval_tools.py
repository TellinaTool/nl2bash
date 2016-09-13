"""
The set of functions used at test time.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import random

import tensorflow as tf

import os, sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "eval"))

import data_utils, data_tools
import ast_based


def to_readable(outputs, rev_cm_vocab):
    search_history = [data_utils._ROOT]
    for output in outputs:
        if output < len(rev_cm_vocab):
            search_history.append(rev_cm_vocab[output])
        else:
            search_history.append(data_utils._UNK)
    tree = data_tools.list2ast(search_history)
    cmd = data_tools.ast2command(tree, loose_constraints=True)
    return tree, cmd, search_history


def decode(output_logits, rev_cm_vocab, FLAGS):
    if FLAGS.decoding_algorithm == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
    elif FLAGS.decoding_algorithm == "beam_search":
        outputs = [np.argmax(logit, axis=1) for logit in output_logits]
    else:
        raise ValueError("Unrecognized decoding algorithm name.")

    # If there is an EOS symbol in outputs, cut them at that point.
    if data_utils.EOS_ID in outputs:
        outputs = outputs[:outputs.index(data_utils.EOS_ID)]

    # Print out command corresponding to outputs.
    if FLAGS.decoder_topology == "rnn":
        if FLAGS.char:
            cmd = "".join([tf.compat.as_str(rev_cm_vocab[output]).strip() for output in outputs]) \
                .replace(data_utils._UNK, ' ')
        else:
            tokens = []
            for output in outputs:
                if output < len(rev_cm_vocab):
                    tokens.append(rev_cm_vocab[output])
                else:
                    tokens.append(data_utils._UNK)
            cmd = " ".join(tokens)
        cmd = re.sub('( ;\s+)|( ;$)', ' \\; ', cmd)
        cmd = re.sub('( \)\s+)|( \)$)', ' \\) ', cmd)
        cmd = re.sub('(^\( )|( \( )', '\\(', cmd)
        tree = data_tools.bash_parser(cmd)
        return tree, cmd, None
    else:
        return to_readable(outputs, rev_cm_vocab)


def batch_decode(output_logits, rev_cm_vocab, FLAGS):
    batch_size = len(output_logits[0])
    batch_outputs = []
    if FLAGS.decoding_algorithm == "greedy":
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        predictions = [np.argmax(logit, axis=1) for logit in output_logits]
    elif FLAGS.decoding_algorithm == "beam_search":
        predictions = [np.argmax(logit, axis=1) for logit in output_logits] 
    else:
        raise ValueError("Unrecognized decoding algorithm name.")

    for i in xrange(batch_size):
        outputs = [int(pred[i]) for pred in predictions]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            # Print out command corresponding to outputs.
        if FLAGS.decoder_topology == "seq":
            if FLAGS.char:
                cmd = "".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs]) \
                                    .replace(data_utils._UNK, ' ')
            else:
                cmd = " ".join([tf.compat.as_str(rev_cm_vocab[output]) for output in outputs])
            cmd = cmd.replace(' ; ', ' \\; ')
            tree = data_tools.bash_parser(cmd)
            search_history = None
        else:
            tree, cmd, search_history = to_readable(outputs, rev_cm_vocab)
        batch_outputs.append((tree, cmd, search_history))
    return batch_outputs


def eval_set(sess, model, dataset, rev_nl_vocab, rev_cm_vocab, FLAGS,
             verbose=True):
    num_top_k_correct_template = 0.0
    num_top_k_correct = 0.0
    num_correct_template = 0.0
    num_correct = 0.0
    num_eval = 0

    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True)

    for nl_template in grouped_dataset:
        nl_strs, cm_strs, nls, search_historys = grouped_dataset[nl_template]
        nl_str = nl_strs[0]
        nl = nls[0]

        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(model.buckets))
                        if model.buckets[b][0] > len(nl)])

        formatted_example = model.format_example(nl, [data_utils.ROOT_ID], bucket_id)
        _, _, output_logits, attn_masks = model.step(sess, formatted_example, bucket_id,
                                         forward_only=True)

        sentence = ' '.join([rev_nl_vocab[i] for i in nl])
        gt_trees = [data_tools.bash_parser(cmd) for cmd in cm_strs]
        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, _ = decode(output_logits, rev_cm_vocab, FLAGS)
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_search_histories, decode_scores = \
                model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            top_k_pred_trees = []
            top_k_pred_cmds = []
            for j in xrange(FLAGS.top_k-1, -1, -1):
                tree, pred_cmd, _ = to_readable(
                    top_k_search_histories[j], rev_cm_vocab)
                top_k_pred_trees.insert(0, tree)
                top_k_pred_cmds.insert(0, pred_cmd)
                if ast_based.one_template_match(gt_trees, tree):
                    num_top_k_correct_template += 1
                if ast_based.one_string_match(gt_trees, tree):
                    num_top_k_correct += 1

        # evaluation ignoring flag orders
        if ast_based.one_template_match(gt_trees, tree):
            num_correct_template += 1
        if ast_based.one_string_match(gt_trees, tree):
            num_correct += 1
        num_eval += 1

        if verbose:
            print("Example %d (%d)" % (num_eval, len(cm_strs)))
            print("Original English: " + nl_str.strip())
            print("English: " + sentence)
            for j in xrange(len(cm_strs)):
                print("GT Command {}: ".format(j+1) + cm_strs[j].strip())
            if FLAGS.decoding_algorithm == "greedy":
                print("Prediction: " + pred_cmd)
                print("AST: ")
                data_tools.pretty_print(tree, 0)
                print()
            elif FLAGS.decoding_algorithm == "beam_search":
                for j in xrange(FLAGS.top_k):
                    print("Prediction %d: " % (j+1) + top_k_pred_cmds[j])
                    print("AST: ")
                    data_tools.pretty_print(top_k_pred_trees[j], 0)
                    print()

    temp_match_score = num_correct_template/num_eval
    string_match_score = num_correct/num_eval
    print("%d examples evaluated" % num_eval)
    print("Percentage of Template Match = %.2f" % temp_match_score)
    print("Percentage of String Match = %.2f" % string_match_score)
    print()

    return temp_match_score, string_match_score


def manual_eval(sess, model, dataset, rev_nl_vocab, rev_cm_vocab,
                FLAGS, num_eval = 30):
    num_correct_template = 0.0
    num_correct_command = 0.0

    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=True).values()
    random.shuffle(grouped_dataset)

    o_f = open("manual.eval.results", 'w')

    num_evaled = 0

    for i in xrange(len(grouped_dataset)):
        nl_strs, cm_strs, nls, search_historys = grouped_dataset[i]
        nl_str = nl_strs[0]
        nl = nls[0]

        if num_evaled == num_eval:
            break

        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(model.buckets))
                        if model.buckets[b][0] > len(nl)])

        formatted_example = model.format_example(nl, [data_utils.ROOT_ID], bucket_id)
        _, _, output_logits, _ = model.step(sess, formatted_example, bucket_id,
                                         forward_only=True)

        gt_trees = [data_tools.bash_parser(cmd) for cmd in cm_strs]
        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, _ = decode(output_logits, rev_cm_vocab, FLAGS)
        else:
            top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            top_k_pred_trees = []
            top_k_pred_cmds = []
            for j in xrange(FLAGS.top_k):
                tree, pred_cmd, _ = \
                    to_readable(top_k_search_histories[j], rev_cm_vocab)
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
                data_tools.pretty_print(tree, 0)
                print()
            elif FLAGS.decoding_algorithm == "beam_search":
                for j in xrange(FLAGS.top_k):
                    decode_score = decode_scores[j]
                    tree = top_k_pred_trees[j]
                    pred_cmd = top_k_pred_cmds[j]
                    print("Prediction %d (%.2f): " % (j+1, decode_score) + pred_cmd)
                    print("AST: ")
                    data_tools.pretty_print(tree, 0)
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


def interactive_decode(sess, model, nl_vocab, rev_cm_vocab, FLAGS):
    """
    Simple command line decoding interface.
    """

    # Decode from standard input.
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while sentence:
        # Get token-ids for the input sentence.
        if FLAGS.char:
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                     data_tools.char_tokenizer, data_tools.basic_tokenizer)
        else:
            token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), nl_vocab,
                                                     data_tools.basic_tokenizer, None)

        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(model.buckets))
                        if model.buckets[b][0] > len(token_ids)])

        # Get a 1-element batch to feed the sentence to the model.
        formatted_example = model.format_example(token_ids, [data_utils.ROOT_ID], bucket_id)

        # Get output logits for the sentence.
        _, _, output_logits, _ = model.step(sess, formatted_example, bucket_id,
                                         forward_only=True)
        if FLAGS.decoding_algorithm == "greedy":
            tree, cmd, _ = decode(output_logits, rev_cm_vocab, FLAGS)
            print()
            print(cmd)
            print()
            data_tools.pretty_print(tree, 0)
            print()
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_search_histories, decode_scores = model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            print()
            for i in xrange(FLAGS.top_k):
                outputs = top_k_search_histories[i]
                tree, cmd, _ = to_readable(outputs, rev_cm_vocab)
                print("prediction %d (%.2f): " % (i, decode_scores[i]) + cmd)
                print()
                data_tools.pretty_print(tree, 0)
                print()

        print("> ", end="")
        sys.stdout.flush()
        sentence = sys.stdin.readline()
