"""
The set of functions used at test time.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import random

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "eval"))

import data_utils, data_tools
import ast_based
from eval_archive import DBConnection


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

        gt_trees = [data_tools.bash_parser(cmd) for cmd in cm_strs]
        if FLAGS.decoding_algorithm == "greedy":
            tree, pred_cmd, outputs = decode(output_logits, rev_cm_vocab, FLAGS)
        elif FLAGS.decoding_algorithm == "beam_search":
            top_k_search_histories, decode_scores = \
                model.beam_decode(FLAGS.beam_size, FLAGS.top_k)
            top_k_pred_trees = []
            top_k_pred_cmds = []
            for j in xrange(FLAGS.top_k-1, -1, -1):
                tree, pred_cmd, outputs = to_readable(
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
        if attn_masks != None:
            visualize_attn_masks(attn_masks[0, :, :], nl, outputs, rev_nl_vocab, rev_cm_vocab,
                             os.path.join(FLAGS.train_dir, "{}.jpg".format(num_eval)))

        if verbose:
            print("Example %d (%d)" % (num_eval, len(cm_strs)))
            print("Original English: " + nl_str.strip())
            print("English: " + ' '.join([rev_nl_vocab[i] for i in nl]))
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
    random.shuffle(grouped_dataset, lambda: 0.5208484091114275)

    o_f = open("manual.eval.results", 'w')

    num_evaled = 0

    with DBConnection() as db:
        db.create_schema()
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
            if True:
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
                pred_temp = data_tools.ast2template(tree, loose_constraints=True)
                str_judge = db.get_str_judgement((nl_str, pred_cmd))
                temp_judge = db.get_temp_judgement((nl_str, pred_temp))
                if temp_judge != None:
                    judgement_str = "y" if temp_judge else "n"
                    print("Correct template [y/n]: %s" % judgement_str)
                else:
                    temp_judge = ast_based.one_template_match(gt_trees, tree)
                    if not temp_judge:
                        inp = raw_input("Correct template [y/n]: ")
                        if inp == "y":
                            temp_judge = True
                            db.add_temp_judgement((nl_str, pred_temp, 1))
                        else:
                            temp_judge = False
                            db.add_temp_judgement((nl_str, pred_temp, 0))
                    else:
                        print("Correct template [y/n]: y")
                if temp_judge:
                    num_correct_template += 1
                    o_f.write("C")
                    if str_judge != None:
                        judgement_str = "y" if str_judge else "n"
                        print("Correct command [y/n]: %s" % judgement_str)
                    else:
                        str_judge = ast_based.one_string_match(gt_trees, tree)
                        if not str_judge:
                            inp = raw_input("Correct command [y/n]: ")
                            if inp == "y":
                                str_judge = True
                                o_f.write("C")
                                db.add_str_judgement((nl_str, pred_cmd, 1))
                            else:
                                str_judge = False
                                o_f.write("W")
                                db.add_str_judgement((nl_str, pred_cmd, 0))
                        else:
                            print("Correct command [y/n]: y")
                    if str_judge:
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


def compare_models(sessions, models, dataset, rev_nl_vocab, rev_cm_vocab,
                FLAGS, num_eval = 30):
    num_correct_template = [0.0] * len(models)
    num_correct_command = [0.0] * len(models)

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

        print("Example %d (%d)" % (num_evaled+1, len(cm_strs)))
        o_f.write("Example %d (%d)" % (num_evaled+1, len(cm_strs)) + "\n")
        print("English: " + nl_str.strip())
        o_f.write("English: " + nl_str.strip() + "\n")
        for j in xrange(len(cm_strs)):
            print("GT Command %d: " % (j+1) + cm_strs[j].strip())
            o_f.write("GT Command %d: " % (j+1) + cm_strs[j].strip() + "\n")

        for i, model in enumerate(models):
            print("Model %d" % i)
            o_f.write("Model %d\n" % i)
            # Which bucket does it belong to?
            bucket_id = min([b for b in xrange(len(model.buckets))
                            if model.buckets[b][0] > len(nl)])

            formatted_example = model.format_example(nl, [data_utils.ROOT_ID], bucket_id)
            _, _, output_logits, _ = model.step(sessions[i], formatted_example, bucket_id,
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
                num_correct_template[i] += 1
                o_f.write("C")
                inp = raw_input("Correct command [y/n]: ")
                if inp == "y":
                    num_correct_command[i] += 1
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
    for i in xrange(len(models)):
        print("Percentage of Template Match = %.2f" % (num_correct_template[i]/num_eval))
        print("Percentage of String Match = %.2f" % (num_correct_command[i]/num_eval))
    print()

    o_f.write("\n")
    o_f.write("%d eamples evaluated" % num_eval + "\n")
    for i in xrange(len(models)):
        o_f.write("Percentage of Template Match = %.2f" % (num_correct_template[i]/num_eval) + "\n")
        o_f.write("Percentage of String Match = %.2f" % (num_correct_command[i]/num_eval) + "\n")
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


def visualize_attn_masks(M, source, target, rev_nl_vocab, rev_cm_vocab, output_path):
    target_length, source_length = M.shape
    
    plt.clf()
    fig = plt.imshow(M, interpolation='nearest', cmap=plt.cm.Blues)

    nl = [rev_nl_vocab[x] for x in source]
    cm = [rev_cm_vocab[x] for x in target]
    plt.xticks(xrange(source_length), 
               [x.replace("$$", "") for x in reversed(nl + [data_utils._PAD] * (source_length - len(nl)))],
               rotation='vertical')
    plt.yticks(xrange(len(cm)), 
               [x.replace("$$", "") for x in cm],
               rotation='horizontal')

    plt.colorbar()
    
    plt.savefig(output_path, bbox_inches='tight')
