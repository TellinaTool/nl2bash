"""
Compute translation accuracy of a system.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import functools
import numpy as np
import os, sys
import random
import shutil

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import bash, data_tools, nast
from encoder_decoder import data_utils, graph_utils
from eval import token_based, tree_dist, zss
from eval.dfa_equal import regexDFAEquals
from nlp_tools import constants, tokenizer

DEBUG = False


error_types = {
    0 : "unmarked error",
    2 : "extra utility",
    3 : "missing utility",
    4 : "confused utility",
    5 : "extra flag",
    6 : "missing flag",
    7 : "confused flag",
    8 : "logic error",
    9 : "count error"
}


def eval_set(model_dir, decode_sig, dataset, top_k, FLAGS, manual=True,
             verbose=False):
    eval_bash = FLAGS.dataset.startswith("bash") and not FLAGS.explain
    eval_regex = FLAGS.dataset.startswith("regex") and not FLAGS.explain

    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    use_bucket = False if "knn" in model_dir else True

    tokenizer_selector = 'cm' if FLAGS.explain else 'nl'
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=use_bucket,
        tokenizer_selector=tokenizer_selector)
    vocabs = data_utils.load_vocabulary(FLAGS)
    rev_sc_vocab = vocabs.rev_sc_vocab

    # Load predictions
    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: "
            "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))

    # Load additional ground truths
    if eval_bash:
        template_translations, command_translations = \
            load_ground_truths_from_manual_evaluation(FLAGS.data_dir)

    # Compute manual evaluation scores on a subset of examples
    if manual:
        # Get FIXED dev set samples
        random.seed(100)
        example_ids = list(range(len(grouped_dataset)))
        random.shuffle(example_ids)
        sample_ids = example_ids[:100]
        grouped_dataset = [grouped_dataset[i] for i in sample_ids]
        prediction_list = [prediction_list[i] for i in sample_ids]
   
    num_eval = 0
    top_k_temp_correct = np.zeros([len(grouped_dataset), top_k])
    top_k_str_correct = np.zeros([len(grouped_dataset), top_k])
    if eval_bash:
        top_k_cms = np.zeros([len(grouped_dataset), top_k])

    o_f = open('debug.partial', 'w')
    for data_id in xrange(len(grouped_dataset)):
        _, data_group = grouped_dataset[data_id]
        sc_str = data_group[0].sc_txt.strip()
        sc_temp = normalize_nl_ground_truth(sc_str)
        sc_tokens = [rev_sc_vocab[i] for i in data_group[0].sc_ids]
        if FLAGS.channel == 'char':
            sc_features = ''.join(sc_tokens)
            sc_features = sc_features.replace(constants._SPACE, ' ')
        else:
            sc_features = ' '.join(sc_tokens)
        command_gts = [dp.tg_txt.strip() for dp in data_group]
        if eval_bash:
            command_gt_asts, template_gt_asts = extend_ground_truths(
                sc_temp, command_gts, command_translations,
                template_translations)

        num_gts = len(command_gts)

        if verbose:
            print("Example {}".format(data_id))
            print("Original Source: {}".format(sc_str))
            print("Source: {}".format(sc_features))
            for j, command_gt in enumerate(command_gts):
                print("GT Target {}: ".format(j+1) + command_gt.strip())
        num_eval += (1 if eval_bash else num_gts)
        predictions = prediction_list[data_id]
        for i in xrange(len(predictions)):
            pred_cmd = predictions[i]
            tree = cmd_parser(pred_cmd)
            # evaluation ignoring flag orders
            if eval_bash:
                temp_match = tree_dist.one_match(
                    template_gt_asts, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, tree, ignore_arg_value=False)
            else:
                if eval_regex:
                    eval_regex_with_semantic_equivalence(
                        pred_cmd, command_gts, verbose=verbose)
                else:
                    str_match = pred_cmd in command_gts
                temp_match = str_match

            if temp_match:
                top_k_temp_correct[data_id, i] = 1 if eval_bash else num_gts
            if str_match:
                if i == 0:
                    o_f.write('{}\n'.format(sc_str))
                top_k_str_correct[data_id, i] = 1 if eval_bash else num_gts
            if eval_bash:
                cms = token_based.command_match_score(template_gt_asts, tree)
                top_k_cms[data_id, i] = cms
                if verbose:
                    print("Prediction {}: {} ({})".format(
                        i+1, pred_cmd, cms))
            else:
                if verbose:
                    print("Prediction {}: {}".format(i+1, pred_cmd))

        if verbose:
            print()

    M = {}
    M["top1_temp_ms"] = np.sum(top_k_temp_correct[:, 0]) / num_eval
    M["top3_temp_ms"] = -1
    M["top5_temp_ms"] = -1
    M["top10_temp_ms"] = -1
    M["top1_str_ms"] = np.sum(top_k_str_correct[:, 0]) / num_eval
    M["top3_str_ms"] = -1
    M["top5_str_ms"] = -1
    M["top10_str_ms"] = -1
    if eval_bash:
        M["top1_cms"] = np.sum(top_k_cms[:, 0] / num_eval)
        M["top3_cms"] = -1
        M["top5_cms"] = -1
        M["top10_cms"] = -1

    print("%d examples evaluated" % num_eval)
    print("Top 1 Match (template-only) = %.3f" % M["top1_temp_ms"])
    print("Top 1 Match (whole-string) = %.3f" % M["top1_str_ms"])
    if eval_bash:
        print("Average top 1 Template Match Score = %.3f" % M["top1_cms"])

    if len(predictions) > 1:
        M["top3_temp_ms"] = \
            np.sum(np.max(top_k_temp_correct[:, :3], 1)) / num_eval
        M["top3_str_ms"] = \
            np.sum(np.max(top_k_str_correct[:, :3], 1)) /num_eval
        print("Top 3 Match (template-only) = %.3f" % M["top3_temp_ms"])
        print("Top 3 Match (whole-string) = %.3f" % M["top3_str_ms"])
        if eval_bash:
            M["top3_cms"] = np.sum(np.max(top_k_cms[:, :3], 1)) / num_eval
            print("Average top 3 Template Match Score = %.3f" % M["top3_cms"])
    if len(predictions) > 3:
        M["top5_temp_ms"] = \
            np.sum(np.max(top_k_temp_correct[:, :5], 1)) / num_eval
        M["top5_str_ms"] = \
            np.sum(np.max(top_k_str_correct[:, :5], 1)) /num_eval
        print("Top 5 Match (template-only) = %.3f" % M["top5_temp_ms"])
        print("Top 5 Match (whole-string) = %.3f" % M["top5_str_ms"])
        if eval_bash:
            M["top5_cms"] = np.sum(np.max(top_k_cms[:, :5], 1)) / num_eval
            print("Average top 5 Template Match Score = %.3f" % M["top5_cms"])
    if len(predictions) > 5:
        M["top10_temp_ms"] = \
            np.sum(np.max(top_k_temp_correct[:, :10], 1)) / num_eval
        M["top10_str_ms"] = \
            np.sum(np.max(top_k_str_correct[:, :10], 1)) / num_eval
        print("Top 10 Match (template-only) = %.3f" % M["top10_temp_ms"])
        print("Top 10 Match (whole-string) = %.3f" % M["top10_str_ms"])
        if eval_bash:
            M["top10_cms"] = np.sum(np.max(top_k_cms[:, :10], 1)) / num_eval
            print("Average top 10 Template Match Score = %.3f" % M["top10_cms"])
    print()

    return M


def eval_regex_with_semantic_equivalence(pred_cmd, ground_truths, verbose=False):
    unprocessed_pred_cmd = regexDFAEquals.unprocess_regex(pred_cmd)
    str_match = False
    for gt_str in ground_truths:
        unprocessed_gt_str = regexDFAEquals.unprocess_regex(gt_str)
        if regexDFAEquals.regex_equiv_from_raw(gt_str, pred_cmd):
            str_match = True
            # Debugging
            if verbose:
                if gt_str != pred_cmd:
                    print("1) {} ({})".format(gt_str, unprocessed_gt_str))
                    print("2) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                    print()
                else:
                    print("i) {} ({})".format(gt_str, unprocessed_gt_str))
                    print("ii) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                    print()
            break
        else:
            if verbose:
                print("A) {} ({})".format(gt_str, unprocessed_gt_str))
                print("B) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                print()
    return str_match, str_match


def gen_manual_evaluation_csv_single_model(dataset, FLAGS):
    """
    Generate .csv spreadsheet for manual evaluation on dev/test set
    examples for a specific model.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
    model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    prediction_list = load_predictions(model_dir, decode_sig, top_k=3)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth list and prediction list length must "
            "be equal: {} vs. {}".format(len(grouped_dataset),
            len(prediction_list)))

    # Load additional ground truths
    template_translations, command_translations = \
        load_ground_truths_from_manual_evaluation(FLAGS.data_dir)

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluation_results(
            os.path.join(FLAGS.data_dir, 'manual_judgements'))

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    output_path = os.path.join(model_dir, 'manual.evaluations.single.model')
    with open(output_path, 'w') as o_f:
        # write spreadsheet header
        o_f.write('id,description,command,correct template,correct command\n')
        for example_id in range(len(grouped_dataset)):
            data_group = grouped_dataset[example_id][1]
            sc_txt = data_group[0].sc_txt.strip()
            sc_temp = normalize_nl_ground_truth(sc_txt)
            command_gts = [dp.tg_txt for dp in data_group]
            command_gt_asts, template_gt_asts = extend_ground_truths(
                sc_temp, command_gts, command_translations,
                template_translations)
            predictions = prediction_list[example_id]
            for i in xrange(3):
                if i >= len(predictions):
                    o_f.write(',,,n,n\n')
                    continue
                pred_cmd = predictions[i]
                cmd = normalize_cm_ground_truth(pred_cmd)
                tree = cmd_parser(cmd)
                temp_match = tree_dist.one_match(
                    template_gt_asts, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, tree, ignore_arg_value=False)
                # Match ground truths & exisitng judgements
                command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_temp, cmd)
                structure_example_sig = '{}<NL_PREDICTION>{}'.format(
                    sc_temp, data_tools.ast2template(tree, loose_constraints=True))
                command_eval, structure_eval = '', ''
                if str_match:
                    command_eval = 'y'
                    structure_eval = 'y'
                elif temp_match:
                    structure_eval = 'y'
                if command_eval_cache and \
                        command_example_sig in command_eval_cache:
                    command_eval = command_eval_cache[command_example_sig]
                if structure_eval_cache and \
                        structure_example_sig in structure_eval_cache:
                    structure_eval = structure_eval_cache[structure_example_sig]
                if i == 0:
                    o_f.write('{},"{}","{}",{},{}\n'.format(
                        example_id, sc_txt.replace('"', '""'), pred_cmd.replace('"', '""'), 
                        structure_eval, command_eval))
                else:
                    o_f.write(',,"{}",{},{}\n'.format(
                        pred_cmd.replace('"', '""'), structure_eval, command_eval))
    print('manual evaluation spreadsheet saved to {}'.format(output_path))
    

def gen_manual_evaluation_table(dataset, FLAGS, interactive=True):
    """
    Generate a table of manual evaluation results on 100 FIXED dev set examples.
    Prompt the user to enter judgement interactively.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    model_names, model_predictions = load_multiple_model_predictions(
        grouped_dataset, FLAGS)

    # Get FIXED dev set samples
    random.seed(100)
    example_ids = list(range(len(grouped_dataset)))
    random.shuffle(example_ids)
    sample_ids = example_ids[:100]

    # Load additional ground truths
    template_translations, command_translations = \
        load_ground_truths_from_manual_evaluation(FLAGS.data_dir)

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluation_results(
            os.path.join(FLAGS.data_dir, 'manual_judgements'))

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    # Interactive manual evaluation interface
    num_s_correct = collections.defaultdict(int)
    num_f_correct = collections.defaultdict(int)
    for exam_id, example_id in enumerate(sample_ids):
        data_group = grouped_dataset[example_id][1]
        sc_txt = data_group[0].sc_txt.strip()
        sc_temp = normalize_nl_ground_truth(sc_txt)
        command_gts = [dp.tg_txt for dp in data_group]
        command_gt_asts, template_gt_asts = extend_ground_truths(
            sc_temp, command_gts, command_translations,
            template_translations)
        for model_id, model_name in enumerate(model_names):
            predictions = model_predictions[model_id][example_id]
            for i in xrange(min(3, len(predictions))):
                pred_cmd = predictions[i]
                cmd = normalize_cm_ground_truth(pred_cmd)
                tree = cmd_parser(cmd)
                temp_match = tree_dist.one_match(
                    template_gt_asts, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, tree, ignore_arg_value=False)
                # Match ground truths & exisitng judgements
                command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_temp, cmd)
                structure_example_sig = '{}<NL_PREDICTION>{}'.format(
                    sc_temp, data_tools.ast2template(tree, loose_constraints=True))
                command_eval, structure_eval = '', ''
                if str_match:
                    command_eval = 'y'
                    structure_eval = 'y'
                elif temp_match:
                    structure_eval = 'y'
                if command_eval_cache and \
                        command_example_sig in command_eval_cache:
                    command_eval = command_eval_cache[command_example_sig]
                if structure_eval_cache and \
                        structure_example_sig in structure_eval_cache:
                    structure_eval = structure_eval_cache[structure_example_sig]
                # Prompt for new judgements
                if command_eval != 'y':
                    if structure_eval == 'y':
                        if not command_eval and interactive:
                            print('#{}. {}'.format(exam_id, sc_txt))
                            for j, gt in enumerate(command_gts):
                                print('- GT{}: {}'.format(j, gt)) 
                            print('> {}'.format(pred_cmd))
                            command_eval = input(
                                'CORRECT COMMAND? [y/reason] ')
                            add_new_judgements(FLAGS.data_dir, sc_txt, pred_cmd,
                                               structure_eval, command_eval)
                            print()
                    else:
                        if not structure_eval and interactive:
                            print('#{}. {}'.format(exam_id, sc_txt))
                            for j, gt in enumerate(command_gts):
                                print('- GT{}: {}'.format(j, gt))
                            print('> {}'.format(pred_cmd))
                            structure_eval = input(
                                'CORRECT STRUCTURE? [y/reason] ')
                            if structure_eval == 'y':
                                command_eval = input(
                                    'CORRECT COMMAND? [y/reason] ')
                            add_new_judgements(FLAGS.data_dir, sc_txt, pred_cmd,
                                               structure_eval, command_eval)
                            print()
                    structure_eval_cache[structure_example_sig] = structure_eval
                    command_eval_cache[command_example_sig] = command_eval
                if structure_eval == 'y':
                    # if i == 0 and model_name == 'tellina':
                    #     o_f.write('{}\n'.format(sc_txt))
                    num_s_correct[model_name] += 1
                if command_eval == 'y':
                    num_f_correct[model_name] += 1

    # print evaluation table
    # compute model name length offset
    max_len = len(max(model_names, key=len))
    max_len_with_offset = (int(max_len / 4) + 1) * 4
    first_line = '{}Acc_F    Acc_T'.format(
        padding_spaces('Model', max_len_with_offset))
    print(first_line)
    print('-' * len(first_line))
    for i, model_name in enumerate(model_names):    
        print('{}{:.2f}    {:.2f}'.format(
            padding_spaces(model_name, max_len_with_offset),
            num_f_correct[model_name] / len(sample_ids),
            num_s_correct[model_name] / len(sample_ids)))
    print('-' * len(first_line))


def padding_spaces(s, max_len):
    return s + ' ' * (max_len - len(s))


def gen_manual_evaluation_csv(dataset, FLAGS):
    """
    Generate .csv spreadsheet for manual evaluation on 100 FIXED dev set
    examples, predictions of different models are listed side-by-side.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    model_names, model_predictions = load_multiple_model_predictions(
        grouped_dataset, FLAGS)

    # Get FIXED dev set samples
    random.seed(100)
    example_ids = list(range(len(grouped_dataset)))
    random.shuffle(example_ids)
    sample_ids = example_ids[:100]

    # Load additional ground truths
    template_translations, command_translations = \
        load_ground_truths_from_manual_evaluation(FLAGS.data_dir)

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluation_results(
            os.path.join(FLAGS.data_dir, 'manual_judgements'))

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    output_path = os.path.join(FLAGS.data_dir, 'manual.evaluations.csv')
    with open(output_path, 'w') as o_f:
        o_f.write('example_id, description, ground_truth, model, prediction, '
                  'correct template, correct command\n')
        for example_id in sample_ids:
            data_group = grouped_dataset[example_id][1]
            sc_txt = data_group[0].sc_txt.strip()
            sc_temp = normalize_nl_ground_truth(sc_txt)
            command_gts = [dp.tg_txt for dp in data_group]
            command_gt_asts, template_gt_asts = extend_ground_truths(
                sc_temp, command_gts, command_translations,
                template_translations)
            for model_id, model_name in enumerate(model_names):
                predictions = model_predictions[model_id][example_id]
                for i in xrange(min(3, len(predictions))):
                    if model_id == 0 and i == 0:
                        output_str = '{},"{}",'.format(example_id,
                            sc_txt.replace('"', '""'))
                    else:
                        output_str = ',,'
                    pred_cmd = predictions[i]
                    cmd = normalize_cm_ground_truth(pred_cmd)
                    tree = cmd_parser(pred_cmd)
                    temp_match = tree_dist.one_match(
                        template_gt_asts, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(
                        command_gt_asts, tree, ignore_arg_value=False)
                    if (model_id*min(3, len(predictions))+i) < len(command_gts):
                        output_str += '"{}",'.format(
                            command_gts[model_id*min(
                                3, len(predictions))+i].strip().replace('"', '""'))
                    else:
                        output_str += ','
                    output_str += '{},"{}",'.format(model_name, 
                        pred_cmd.replace('"', '""'))

                    command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_temp, cmd)
                    structure_example_sig = '{}<NL_PREDICTION>{}'.format(
                        sc_temp, data_tools.cmd2template(cmd, loose_constraints=True))
                    command_eval, structure_eval = '', ''
                    if str_match:
                        command_eval = 'y'
                        structure_eval = 'y'
                    elif temp_match:
                        structure_eval = 'y'
                    if command_eval_cache and \
                            command_example_sig in command_eval_cache:
                        command_eval = command_eval_cache[command_example_sig]
                    if structure_eval_cache and \
                            structure_example_sig in structure_eval_cache:
                        structure_eval = structure_eval_cache[structure_example_sig]
                    output_str += '{},{}'.format(structure_eval, command_eval)
                    o_f.write('{}\n'.format(output_str))

    print('Manual evaluation results saved to {}'.format(output_path))


def load_multiple_model_predictions(grouped_dataset, FLAGS,
                                    tellina=True,
                                    token_seq2seq=True,
                                    token_copynet=True,
                                    char_seq2seq=False,
                                    char_copynet=False,
                                    partial_token_seq2seq=True,
                                    partial_token_copynet=True):
    """
    Load predictions of multiple models.

    :param dataset: The dataset over which the predictions are generated.
    :param FLAGS: Experiment hyperparametrs.
    :param token_seq2seq,
           tellina,
           token_copynet,
           partial_token_seq2seq,
           partial_token_copynet:
           Binary variables indicating whether a model is to be included in the
           test results or not.
    :return model_names: List of model names.
    :return model_predictions: List of model predictions.
    """
    def load_model_predictions():
        model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
        model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
        prediction_list = load_predictions(model_dir, decode_sig, 1)
        if len(grouped_dataset) != len(prediction_list):
            raise ValueError("ground truth list and prediction list length must "
                "be equal: {} vs. {}".format(len(grouped_dataset), 
                len(prediction_list)))
        return prediction_list

    # Load model predictions
    model_names = []
    model_predictions = []

    include_gru = True
    include_lstm = False

    # GRUs
    if include_gru:
        # -- Token
        FLAGS.channel = 'token'
        FLAGS.normalized = False
        FLAGS.use_copy = False
        # --- Seq2Seq
        if token_seq2seq:
            model_names.append('token-seq2seq')
            model_predictions.append(load_model_predictions())
        # --- Tellina
        if tellina:
            FLAGS.normalized = True
            FLAGS.fill_argument_slots = True
            model_names.append('tellina')
            model_predictions.append(load_model_predictions())
            FLAGS.normalized = False
            FLAGS.fill_argument_slots = False
        # --- CopyNet
        if token_copynet:
            FLAGS.use_copy = True
            FLAGS.copy_fun = 'copynet'
            model_names.append('token-copynet')
            model_predictions.append(load_model_predictions())
        # -- Parital token
        FLAGS.normalized = False
        FLAGS.use_copy = False
        FLAGS.channel = 'partial.token'
        # --- Seq2Seq
        if partial_token_seq2seq:
            model_names.append('partial.token-seq2seq')
            model_predictions.append(load_model_predictions())
        # --- CopyNet
        if partial_token_copynet:
            FLAGS.use_copy = True
            FLAGS.copy_fun = 'copynet'
            model_names.append('partial.token-copynet')
            model_predictions.append(load_model_predictions())

    # LSTMs
    if include_lstm:
        FLAGS.rnn_cell = 'lstm'
        # -- Token
        FLAGS.channel = 'token'
        # --- Seq2Seq
        FLAGS.normalized = False
        FLAGS.use_copy = False
        model_names.append('token-seq2seq-lstm')
        model_predictions.append(load_model_predictions())
        # --- Tellina
        FLAGS.normalized = True
        FLAGS.fill_argument_slots = True
        model_names.append('tellina-lstm')
        model_predictions.append(load_model_predictions())
        # -- Partial token
        FLAGS.channel = 'partial.token'
        # --- Seq2Seq
        FLAGS.normalized = False
        FLAGS.fill_argument_slots = False
        model_names.append('partial.token-seq2seq-lstm')
        model_predictions.append(load_model_predictions())

    return model_names, model_predictions


def extend_ground_truths(sc_temp, tg_strs, command_translations,
                         template_translations):
    command_gts = set(tg_strs) | command_translations[sc_temp]
    command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
    template_gt_asts = []
    for gt in (command_gts | template_translations[sc_temp]):
        gt_ast = data_tools.bash_parser(gt)
        if gt_ast is None:
            # Check error in ground truth command
            print('Warning: ground truth command parsing error: {}'.format(gt))
        else:
            template_gt_asts.append(gt_ast)
    return command_gt_asts, template_gt_asts


def load_predictions(model_dir, decode_sig, top_k, verbose=True):
    """
    Load model predictions (top_k per example) from disk.

    :param model_dir: Directory where the model prediction file is stored.
    :param decode_sig: The decoding signature of the model which generated the
        prediction results.
    :param top_k: Maximum number of predictions to read per example.
    :return: List of top k predictions.
    """
    prediction_path = os.path.join(model_dir, 'predictions.{}.latest'.format(decode_sig))
    with open(prediction_path) as f:
        prediction_list = []
        for line in f:
            predictions = line.split('|||')
            prediction_list.append(predictions[:top_k])
    if verbose:
        print('{} predictions loaded from {}'.format(
            len(prediction_list), prediction_path))
    return prediction_list


def load_cached_evaluation_results(model_dir, verbose=True):
    """
    Load cached evaluation results from disk.

    :param model_dir: Directory where the evaluation result file is stored.
    :param decode_sig: The decoding signature of the model being evaluated.
    :return: dictionaries storing the evaluation results.
    """
    structure_eval_results = {}
    command_eval_results = {}
    eval_files = []
    for file_name in os.listdir(model_dir):
        if 'evaluations' in file_name and not file_name.endswith('base'):
            eval_files.append(file_name)
    for file_name in sorted(eval_files):
        manual_judgement_path = os.path.join(model_dir, file_name)
        with open(manual_judgement_path) as f:
            if verbose:
                print('reading cached evaluations from {}'.format(
                    manual_judgement_path))
            reader = csv.DictReader(f)
            current_nl = ''
            for row in reader:
                if row['description']:
                    current_nl = row['description']
                pred_cmd = row['prediction']
                pred_temp = row['template']
                command_eval = row['correct command']
                command_row_sig = '{}<NL_PREDICTION>{}'.format(
                    current_nl, pred_cmd)
                if command_eval:
                    command_eval_results[command_row_sig] = command_eval
                structure_eval = row['correct template']
                structure_row_sig = '{}<NL_PREDICTION>{}'.format(
                    current_nl, pred_temp)
                if structure_eval:
                    structure_eval_results[structure_row_sig] = structure_eval
    print('{} structure evaluation results loaded'.format(len(structure_eval_results)))
    print('{} command evaluation results loaded'.format(len(command_eval_results)))
    return structure_eval_results, command_eval_results


def load_ground_truths_from_manual_evaluation(data_dir, verbose=False):
    """
    Load cached evaluation results from disk.

    :return: nl -> template translation map, nl -> command translation map
    """
    command_translations = collections.defaultdict(set)
    template_translations = collections.defaultdict(set)
    data_dir = os.path.join(data_dir, 'manual_judgements')
    eval_files = []
    for file_name in os.listdir(data_dir):
        if 'evaluations' in file_name and not file_name.endswith('base'):
            eval_files.append(file_name)
    for file_name in sorted(eval_files):
        manual_judgement_path = os.path.join(data_dir, file_name)
        with open(manual_judgement_path) as f:
            if verbose:
                print('reading cached evaluations from {}'.format(
                    manual_judgement_path))
            reader = csv.DictReader(f)
            current_nl = ''
            for row in reader:
                if row['description']:
                    current_nl = row['description']
                pred_cmd = row['prediction']
                pred_temp = row['template']
                structure_eval = row['correct template']
                command_eval = row['correct command']
                if structure_eval == 'y':
                    template_translations[current_nl].add(pred_temp)
                if command_eval == 'y':
                    command_translations[current_nl].add(pred_cmd)
    print('{} template translations loaded'.format(len(template_translations)))
    print('{} command translations loaded'.format(len(command_translations)))

    return template_translations, command_translations


def add_new_judgements(data_dir, nl, command, correct_template='',
                       correct_command=''):
    """
    Append a new judgement
    """
    data_dir = os.path.join(data_dir, 'manual_judgements')
    manual_judgement_path = os.path.join(
        data_dir, 'manual.evaluations.additional')
    if not os.path.exists(manual_judgement_path):
        with open(manual_judgement_path, 'w') as o_f:
            o_f.write(
                'description,prediction,template,correct template,correct command\n')
    with open(manual_judgement_path, 'a') as o_f:
        nl = normalize_nl_ground_truth(nl)
        command = normalize_cm_ground_truth(command)
        temp = data_tools.cmd2template(command, loose_constraints=True)
        if not correct_template:
            correct_template = 'n'
        if not correct_command:
            correct_command = 'n'
        o_f.write('"{}","{}","{}","{}","{}"\n'.format(
            nl.replace('"', '""'), command.replace('"', '""'), 
            temp.replace('"', '""'), correct_template.replace('"', '""'), 
            correct_command.replace('"', '""')))
    print('new judgement added to {}'.format(manual_judgement_path))


def normalize_nl_ground_truth(nl):
    tokens, _ = tokenizer.basic_tokenizer(nl)
    return ' '.join(tokens)


def normalize_cm_ground_truth(cm):
    return tree_dist.ignore_differences(cm)


# -- Generate error analysis spreadsheet -- #

def print_error_analysis_csv(grouped_dataset, prediction_list, FLAGS,
        cached_evaluation_results=None, group_by_utility=False,
        error_predictions_only=True):
    """
    Convert dev/test set examples to csv format so as to make it easier for
    human annotators to enter their judgements.

    :param grouped_dataset: dev/test set grouped by natural language.
    :param prediction_list: model predictions.
    :param FLAGS: experiment hyperparameters.
    :param cached_evaluation_results: cached evaluation results from previous
        rounds.
    :param group_by_utility: if set, group the error examples by the utilities
        used in the ground truth.
    """
    def mark_example(error_list, example, gt_utility=None):
        if gt_utility:
            error_list[gt_utility].append(example)
        else:
            error_list.append(example)

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser
    if group_by_utility:
        utility_index = {}
        for line in bash.utility_stats.split('\n'):
            ind, utility, _, _, _ = line.split(',')
            utility_index[utility] = ind

    grammar_errors = collections.defaultdict(list) if group_by_utility else []
    argument_errors = collections.defaultdict(list) if group_by_utility else []
    example_id = 0
    for nl_temp, data_group in grouped_dataset:
        sc_txt = data_group[0].sc_txt.strip()
        sc_temp = normalize_nl_ground_truth(sc_txt)
        tg_strs = [dp.tg_txt for dp in data_group]
        gt_trees = [cmd_parser(cm_str) for cm_str in tg_strs]
        if group_by_utility:
            gt_utilities = functools.reduce(lambda x,y:x|y,
                [data_tools.get_utilities(gt) for gt in gt_trees])
            gt_utility = sorted(
                list(gt_utilities), key=lambda x:int(utility_index[x]))[-1]
        else:
            gt_utility = None
        predictions = prediction_list[example_id]
        example_id += 1
        example = []
        grammar_error, argument_error = False, False
        for i in xrange(min(3, len(predictions))):
            if i == 0:
                output_str = '{},"{}",'.format(
                    example_id, sc_txt.replace('"', '""'))
            else:
                output_str = ',,'
            pred_cmd = predictions[i]
            tree = cmd_parser(pred_cmd)

            # evaluation ignoring flag orders
            temp_match = tree_dist.one_match(
                gt_trees, tree, ignore_arg_value=True)
            str_match = tree_dist.one_match(
                gt_trees, tree, ignore_arg_value=False)
            if i < len(tg_strs):
                output_str += '"{}",'.format(
                    tg_strs[i].strip().replace('"', '""'))
            else:
                output_str += ','
            output_str += '"{}",'.format(pred_cmd.replace('"', '""'))
            if not str_match:
                if temp_match:
                    if i == 0:
                        argument_error = True
                        grammar_error = True
                else:
                    if i == 0:
                        grammar_error = True

            example_sig = '{}<NL_PREDICTION>{}'.format(
                sc_temp, normalize_cm_ground_truth(pred_cmd))
            if cached_evaluation_results and \
                    example_sig in cached_evaluation_results:
                output_str += cached_evaluation_results[example_sig]
            else:
                if str_match:
                    output_str += 'y,y'
                elif temp_match:
                    output_str += 'y,'
            example.append(output_str)
        if error_predictions_only:
            if grammar_error:
                mark_example(grammar_errors, example, gt_utility)
            elif argument_error:
                mark_example(argument_errors, example, gt_utility)
        else:
            mark_example(grammar_errors, example, gt_utility)

    return grammar_errors, argument_errors


def gen_error_analysis_csv(model_dir, decode_sig, dataset, FLAGS, top_k=3):
    """
    Generate error analysis evaluation spreadsheet.
        - grammar error analysis
        - argument error analysis
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: "
            "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))

    # Convert the predictions to csv format
    grammar_errors, argument_errors = print_error_analysis_csv(
        grouped_dataset, prediction_list, FLAGS)

    grammar_error_path = os.path.join(model_dir, 'grammar.error.analysis.csv')
    random.shuffle(grammar_errors)
    with open(grammar_error_path, 'w') as grammar_error_file:
        print("Saving grammar errors to {}".format(grammar_error_path))
        # print csv file header
        grammar_error_file.write(
            'example_id, description, ground_truth, prediction, ' +
            'correct template, correct command\n')
        for example in grammar_errors[:100]:
            for line in example:
                grammar_error_file.write('{}\n'.format(line))

    arg_error_path = os.path.join(model_dir, 'argument.error.analysis.csv')
    random.shuffle(argument_errors)
    with open(arg_error_path, 'w') as arg_error_file:
        print("Saving argument errors to {}".format(arg_error_path))
        # print csv file header
        arg_error_file.write(
            'example_id, description, ground_truth, prediction, ' +
            'correct template, correct command\n')
        for example in argument_errors[:100]:
            for line in example:
                arg_error_file.write('{}\n'.format(line))


def gen_error_analysis_csv_by_utility(model_dir, decode_sig, dataset, 
        FLAGS, top_k=10):
    """
    Generate error analysis evaluation sheet grouped by utility.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError(
            "ground truth and predictions length must be equal: {} vs. {}"
            .format(len(grouped_dataset), len(prediction_list)))

    # Load cached evaluation results
    cached_evaluation_results = load_cached_evaluation_results(model_dir)

    # Convert the predictions into csv format
    grammar_errors, argument_errors = print_error_analysis_csv(
        grouped_dataset, prediction_list, FLAGS, cached_evaluation_results,
        group_by_utility=True, error_predictions_only=False)

    error_by_utility_path = \
        os.path.join(model_dir, 'error.analysis.by.utility.csv')
    print("Saving grammar errors to {}".format(error_by_utility_path))
    with open(error_by_utility_path, 'w') as error_by_utility_file:
        # print csv file header
        error_by_utility_file.write(
            'utility, example_id, description, groundtruth, prediction, '
            'correct template, correct command\n')
        for line in bash.utility_stats.split('\n'):
            utility = line.split(',')[1]
            error_examples = grammar_errors[utility]
            if len(error_examples) <= 5:
                for example in error_examples:
                    for l in example:
                        error_by_utility_file.write('{},{}\n'.format(utility, l))
            else:
                random.shuffle(error_examples)
                for example in error_examples[:5]:
                    for l in example:
                        error_by_utility_file.write('{},{}\n'.format(utility, l))


def gen_accuracy_by_utility_csv(eval_by_utility_path):
    """
    Generate accuracy by utility spreadsheet table based on the evaluation by
    utility spreadsheet.
    """
    num_template_correct = collections.defaultdict(int)
    num_command_correct = collections.defaultdict(int)
    num_annotation_errors = collections.defaultdict(int)
    num_complex_tasks = collections.defaultdict(int)
    num_examples = collections.defaultdict(int)
    with open(eval_by_utility_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            utility = row['utility']
            num_examples[utility] += 1
            if row['correct template'] == 'y':
                num_template_correct[utility] += 1
            if row['correct command'] == 'y':
                num_command_correct[utility] += 1
            if row['correct template'] == 'poor description':
                num_annotation_errors[utility] += 1
            if row['correct template'] == 'complex task':
                num_complex_tasks[utility] += 1
    output_path = os.path.join(os.path.dirname(eval_by_utility_path),
                               'accuracy.by.utility.csv')
    print('Save accuracy by utility metrics to {}'.format(output_path))
    with open(output_path, 'w') as o_f: 
        # print csv file header
        o_f.write('ID,utility,# flags,# train,# test,template accuracy,'
                  'command accuracy,% annotation errors,% complex tasks,'
                  '% annotation problems\n')
        for line in bash.utility_stats.split('\n'):
            utility = line.split(',')[1]
            if utility in num_examples:
                num_exps = num_examples[utility]
                template_acc = round(
                    float(num_template_correct[utility]) / num_exps, 2)
                command_acc = round(
                    float(num_command_correct[utility]) / num_exps, 2)
                annotation_error_rate = round(
                    float(num_annotation_errors[utility]) / num_exps, 2)
                complex_task_rate = round(
                    float(num_complex_tasks[utility]) / num_exps, 2)
                o_f.write('{},{},{},{},{},{}\n'.format(line, template_acc,
                    command_acc, annotation_error_rate, complex_task_rate,
                    (annotation_error_rate+complex_task_rate)))


# -- Unit Tests -- #

def test_ted():
    while True:
        cmd1 = input(">cmd1: ")
        cmd2 = input(">cmd2: ")
        ast1 = data_tools.bash_parser(cmd1)
        ast2 = data_tools.bash_parser(cmd2)
        dist = zss.simple_distance(
            ast1, ast2, nast.Node.get_children, nast.Node.get_label,
            tree_dist.temp_local_dist
        )
        print("ted = {}".format(dist))
        print()


def normalize_judgement_file(judgement_file):
    data_dir = os.path.dirname(judgement_file)
    file_name = os.path.basename(judgement_file)
    if not os.path.exists(os.path.join(data_dir, file_name + '.base')):
        shutil.move(judgement_file, os.path.join(data_dir, file_name + '.base'))
    with open(judgement_file, 'w') as o_f:
        o_f.write('description,prediction,template,correct template,correct command\n')
        with open(os.path.join(data_dir, file_name + '.base')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                description = row['description']
                prediction = row['prediction']
                correct_template = row['correct template']
                correct_command = row['correct command']
                o_f.write('"{}","{}","{}",{},{}\n'.format(
                    normalize_nl_ground_truth(description).replace('"', '""'),
                    normalize_cm_ground_truth(prediction).replace('"', '""'),
                    data_tools.cmd2template(
                        normalize_cm_ground_truth(prediction),
                        loose_constraints=True).replace('"', '""'),
                    correct_template, correct_command))


def normalize_judgement_files(data_dir):
    for file_name in os.listdir(data_dir):
        if 'evaluations.' in file_name:
            normalize_judgement_file(os.path.join(data_dir, file_name))
    

if __name__ == "__main__":
    # eval_file = sys.argv[1]
    # gen_accuracy_by_utility_csv(eval_file)
    judgement_file = sys.argv[1]
    normalize_judgement_files(judgement_file)
