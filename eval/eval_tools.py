"""
Compute translation accuracy of a system.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import copy
import csv
import functools
import numpy as np
import os, sys
import random

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import bash, data_tools, nast
from encoder_decoder import data_utils
from eval import token_based, tree_dist, zss
from eval.dfa_equal import regexDFAEquals
from nlp_tools import constants, tokenizer


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


def eval_set(model_dir, decode_sig, dataset, top_k, FLAGS, verbose=True):
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

    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: "
            "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))
    
    num_eval = 0
    top_k_temp_correct = np.zeros([len(grouped_dataset), top_k])
    top_k_str_correct = np.zeros([len(grouped_dataset), top_k])
    if eval_bash:
        top_k_cms = np.zeros([len(grouped_dataset), top_k])

    # Load manual judgements
    if eval_bash:
        template_translations, command_translations = \
            load_judgments(model_dir, decode_sig)

    for data_id in xrange(len(grouped_dataset)):
        _, data_group = grouped_dataset[data_id]
        sc_str = data_group[0].sc_txt.strip()
        sc_temp = normalize_nl(sc_str)
        sc_tokens = [rev_sc_vocab[i] for i in data_group[0].sc_ids]
        if FLAGS.channel == 'char':
            sc_features = ''.join(sc_tokens)
            sc_features = sc_features.replace(constants._SPACE, ' ')
        else:
            sc_features = ' '.join(sc_tokens)
        if eval_bash:
            command_gts = set([dp.tg_txt.strip() for dp in data_group] + \
                          command_translations[sc_temp])
            command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
            template_gt_asts = [data_tools.bash_parser(gt)
                for gt in set(command_gts + template_translations[sc_temp])]
        else:
            command_gts = [dp.tg_txt.strip() for dp in data_group]
        num_gts = len(command_gts)


        if verbose:
            print("Example {}".format(data_id))
            print("Original Source: {}".format(sc_str))
            print("Source: {}".format(sc_features))
            for j in xrange(len(command_gts)):
                print("GT Target {}: ".format(j+1) + command_gts[j].strip())
        num_eval += (1 if eval_bash else num_gts)

        predictions = prediction_list[data_id]
        for i in xrange(len(predictions)):
            pred_cmd = predictions[i]
            tree = cmd_parser(pred_cmd)
            unprocessed_pred_cmd = regexDFAEquals.unprocess_regex(pred_cmd)
            # evaluation ignoring flag orders
            if eval_bash:
                temp_match = tree_dist.one_match(template_gt_asts, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(command_gt_asts, tree, ignore_arg_value=False)
            else:
                if eval_regex:
                    str_match = False
                    for cmd_str in command_gts:
                        unprocessed_cmd_str = regexDFAEquals.unprocess_regex(cmd_str)
                        if regexDFAEquals.regex_equiv_from_raw(cmd_str, pred_cmd):
                            str_match = True
                            # Debugging
                            if verbose:
                                if cmd_str != pred_cmd:
                                    print("----------------------------------")
                                    print("1) {} ({})".format(cmd_str, unprocessed_cmd_str))
                                    print("2) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                                    print("----------------------------------")
                                else:
                                    print("----------------------------------")
                                    print("i) {} ({})".format(cmd_str, unprocessed_cmd_str))
                                    print("ii) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                                    print("----------------------------------")
                            break
                        else:
                            if verbose:
                                print("----------------------------------")
                                print("A) {} ({})".format(cmd_str, unprocessed_cmd_str))
                                print("B) {} ({})".format(pred_cmd, unprocessed_pred_cmd))
                                print("----------------------------------")
                else:
                    str_match = pred_cmd in command_gts
                temp_match = str_match

            cms = token_based.command_match_score(template_gt_asts, tree) \
                if eval_bash else -1

            if temp_match:
                top_k_temp_correct[data_id, i] = 1 if eval_bash else num_gts
            if str_match:
                top_k_str_correct[data_id, i] = 1 if eval_bash else num_gts
            if eval_bash:
                top_k_cms[data_id, i] = cms
                if verbose:
                    print("Prediction {}: {} ({})".format(
                        i+1, pred_cmd, cms))
            else:
                if verbose:
                    print("Prediction {}: {}".format(i+1, pred_cmd))

        if verbose:
            print()

        data_id += 1
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


def gen_eval_csv(model_dir, decode_sig, dataset, FLAGS, output_path, top_k=3):
    """
    Generate evaluation spreadsheet.
    """
    with open(output_path, 'w') as o_f:
        # print evaluation form header
        o_f.write('example_id, description, ground_truth, prediction, ' +
                  'correct command, correct template\n')

        eval_bash = FLAGS.dataset.startswith("bash")
        cmd_parser = data_tools.bash_parser if eval_bash \
            else data_tools.paren_parser
        tokenizer_selector = "cm" if FLAGS.explain else "nl"
        grouped_dataset = data_utils.group_parallel_data(
            dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)
        prediction_list = load_predictions(model_dir, decode_sig, top_k)
        if len(grouped_dataset) != len(prediction_list):
            raise ValueError("ground truth and predictions length must be equal: "
                "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))

        example_id = 0
        for nl_temp, data_group in grouped_dataset:
            tg_strs = [dp.tg_txt for dp in data_group]
            gt_trees = [cmd_parser(cm_str) for cm_str in tg_strs]
            predictions = prediction_list[example_id]
            example_id += 1
            for i in xrange(min(3, len(predictions))):
                if i == 0:
                    output_str = '{},{},'.format(
                        example_id, data_group[0].sc_txt.strip())
                else:
                    output_str = ',,'
                pred_cmd, score = predictions[i]
                tree = cmd_parser(pred_cmd)
                # evaluation ignoring flag orders
                temp_match = tree_dist.one_match(
                    gt_trees, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    gt_trees, tree, ignore_arg_value=False)
                if i < len(tg_strs):
                    output_str += '{},'.format(tg_strs[i].strip())
                else:
                    output_str += ','
                output_str += '{},'.format(pred_cmd)
                if temp_match:
                    output_str += 'y,'
                if str_match:
                    output_str += 'y'
                o_f.write(output_str + '\n')


def gen_error_analysis_csv(grouped_dataset, prediction_list, FLAGS,
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

    grammar_errors = collections.defaultdict(list) if group_by_utility else []
    argument_errors = collections.defaultdict(list) if group_by_utility else []
    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser
    if group_by_utility:
        utility_index = {}
        for line in bash.utility_stats.split('\n'):
            ind, utility, _, _, _ = line.split(',')
            utility_index[utility] = ind

    example_id = 0
    for nl_temp, data_group in grouped_dataset:
        sc_txt = data_group[0].sc_txt.strip()
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

            example_sig = '{}<NL_PREDICTION>{}'.format(sc_txt, pred_cmd)
            if cached_evaluation_results and \
                    example_sig in cached_evaluation_results:
                # print('example_sig: {}'.format(example_sig))
                # print(cached_evaluation_results[example_sig])
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

    # Convert the predictions to csv format
    grammar_errors, argument_errors = gen_error_analysis_csv(
        grouped_dataset, prediction_list, FLAGS)

    grammar_error_path = os.path.join(model_dir, 'grammar.error.analysis.csv')
    arg_error_path = os.path.join(model_dir, 'argument.error.analysis.csv')
    print("Saving grammar errors to {}".format(grammar_error_path))
    print("Saving argument errors to {}".format(arg_error_path))
    random.shuffle(argument_errors)
    random.shuffle(grammar_errors)
    with open(grammar_error_path, 'w') as grammar_error_file:
        with open(arg_error_path, 'w') as arg_error_file:
            # print csv file header
            arg_error_file.write(
                'example_id, description, ground_truth, prediction, ' +
                'correct template, correct command\n')
            for example in argument_errors[:100]:
                for line in example:
                    arg_error_file.write('{}\n'.format(line))
            # print csv file header
            grammar_error_file.write(
                'example_id, description, ground_truth, prediction, ' +
                'correct template, correct command\n')
            for example in grammar_errors[:100]:
                for line in example:
                    grammar_error_file.write('{}\n'.format(line))


def gen_error_analysis_csv_by_utility(model_dir, decode_sig, dataset, FLAGS,
                                        top_k=10):
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
    cached_evaluation_results = \
        load_cached_evaluation_results(model_dir, decode_sig)

    # Convert the predictions into csv format
    grammar_errors, argument_errors = gen_error_analysis_csv(
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


def load_predictions(model_dir, decode_sig, top_k):
    """
    Load model predictions (top_k per example) from disk.

    :param model_dir: Directory where the model prediction file is stored.
    :param decode_sig: The decoding signature of the model which generated the
        prediction results.
    :param top_k: Maximum number of predictions to read per example.
    :return: List of top k predictions.
    """
    with open(os.path.join(model_dir,
            'predictions.{}.latest'.format(decode_sig))) as f:
        prediction_list = []
        for line in f:
            predictions = line.split('|||')
            prediction_list.append(predictions[:top_k])
    return prediction_list


def load_cached_evaluation_results(model_dir):
    """
    Load cached evaluation results from disk.

    :param model_dir: Directory where the evaluation result file is stored.
    :param decode_sig: The decoding signature of the model being evaluated.
    :return: dictionary storing the evaluation results.
    """
    evaluation_results = {}
    for file_name in os.listdir(model_dir):
        if 'evaluations' in file_name:
            with open(os.path.join(model_dir, file_name)) as f:
                reader = csv.DictReader(f)
                current_nl = ''
                for row in reader:
                    if row['description']:
                        current_nl = row['description']
                    pred_cmd = row['prediction']
                    structure_eval = row['correct template']
                    command_eval = row['correct command']
                    row_sig = '{}<NL_PREDICTION>{}'.format(current_nl, pred_cmd)
                    evaluation_results[row_sig] = \
                        '{},{}'.format(structure_eval, command_eval)
    print('{} evaluation results loaded'.format(len(evaluation_results)))
    return evaluation_results


def load_judgments(model_dir):
    """
    Load cached evaluation results from disk.

    :return: nl -> template translation map, nl -> command translation map
    """
    command_translations = collections.defaultdict(list)
    template_translations = collections.defaultdict(list)
    for file_name in os.listdir(model_dir):
        if 'evaluations' in file_name:
            with open(os.path.join(model_dir, file_name)) as f:
                reader = csv.DictReader(f)
                current_nl = ''
                for row in reader:
                    if row['description']:
                        current_nl = row['description']
                    pred_cmd = row['prediction']
                    structure_eval = row['correct template']
                    command_eval = row['correct command']
                    if structure_eval == 'y':
                        template_translations[normalize_nl(current_nl)].append(pred_cmd)
                    if command_eval == 'y':
                        command_translations[normalize_nl(current_nl)].append(pred_cmd)
    return template_translations, command_translations


def normalize_nl(nl):
    tokens = tokenizer.basic_tokenizer(nl)
    return ' '.join(tokens)


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

# Unit Tests

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


if __name__ == "__main__":
    eval_file = sys.argv[1]
    gen_accuracy_by_utility_csv(eval_file)
