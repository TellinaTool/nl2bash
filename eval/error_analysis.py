"""
Error Analysis.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import functools
import os, sys
import random

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import bash, data_tools
from encoder_decoder import data_utils, graph_utils
from eval import tree_dist
from eval.eval_tools import load_predictions
from eval.eval_tools import load_all_model_predictions
from eval.eval_tools import load_cached_evaluations
from eval.eval_tools import load_cached_correct_translations
from eval.eval_tools import get_example_nl_key


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


def gen_manual_evaluation_csv_single_model(dataset, FLAGS):
    """
    Generate .csv spreadsheet for manual evaluation on dev/test set
    examples for a specific model.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
    model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
    prediction_path = os.path.join(model_dir, 'predictions.{}.latest'.format(decode_sig))
    prediction_list = load_predictions(prediction_path, top_k=3)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth list and prediction list length must "
                         "be equal: {} vs. {}".format(len(grouped_dataset),
                                                      len(prediction_list)))

    # Load additional ground truths
    template_translations, command_translations = load_cached_correct_translations(FLAGS.data_dir)

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = load_cached_evaluations(
        os.path.join(FLAGS.data_dir, 'manual_judgements'))

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash else data_tools.paren_parser

    output_path = os.path.join(model_dir, 'manual.evaluations.single.model')
    with open(output_path, 'w') as o_f:
        # write spreadsheet header
        o_f.write('id,description,command,correct template,correct command\n')
        for example_id in range(len(grouped_dataset)):
            data_group = grouped_dataset[example_id][1]
            sc_txt = data_group[0].sc_txt.strip()
            sc_key = get_example_nl_key(sc_txt)
            command_gts = [dp.tg_txt for dp in data_group]
            command_gts = set(command_gts + command_translations[sc_key])
            command_gt_asts = [data_tools.bash_parser(cmd) for cmd in command_gts]
            template_gts = [data_tools.cmd2template(cmd, loose_constraints=True) for cmd in command_gts]
            template_gts = set(template_gts + template_translations[sc_key])
            template_gt_asts = [data_tools.bash_parser(temp) for temp in template_gts]
            predictions = prediction_list[example_id]
            for i in xrange(3):
                if i >= len(predictions):
                    o_f.write(',,,n,n\n')
                    continue
                pred_cmd = predictions[i]
                pred_tree = cmd_parser(pred_cmd)
                pred_temp = data_tools.ast2template(pred_tree, loose_constraints=True)
                temp_match = tree_dist.one_match(
                    template_gt_asts, pred_tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, pred_tree, ignore_arg_value=False)
                # Match ground truths & exisitng judgements
                command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
                structure_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
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


def gen_manual_evaluation_csv(dataset, FLAGS, num_examples=100):
    """
    Generate .csv spreadsheet for manual evaluation on a fixed set of test/dev
    examples, predictions of different models are listed side-by-side.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, tokenizer_selector=tokenizer_selector)

    model_names, model_predictions = load_all_model_predictions(
        grouped_dataset, FLAGS, top_k=3)

    # Get FIXED dev set samples
    random.seed(100)
    example_ids = list(range(len(grouped_dataset)))
    random.shuffle(example_ids)
    sample_ids = example_ids[num_examples:num_examples+100]

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluations(
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
            sc_key = get_example_nl_key(sc_txt)
            command_gts = [dp.tg_txt for dp in data_group]
            command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
            for model_id, model_name in enumerate(model_names):
                predictions = model_predictions[model_id][example_id]
                for i in xrange(min(3, len(predictions))):
                    if model_id == 0 and i == 0:
                        output_str = '{},"{}",'.format(example_id, sc_txt.replace('"', '""'))
                    else:
                        output_str = ',,'
                    pred_cmd = predictions[i]
                    pred_tree = cmd_parser(pred_cmd)
                    pred_temp = data_tools.ast2template(pred_tree, loose_constraints=True)
                    temp_match = tree_dist.one_match(
                        command_gt_asts, pred_tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(
                        command_gt_asts, pred_tree, ignore_arg_value=False)
                    if (model_id * min(3, len(predictions)) + i) < len(command_gts):
                        output_str += '"{}",'.format(
                            command_gts[model_id * min(
                                3, len(predictions)) + i].strip().replace('"', '""'))
                    else:
                        output_str += ','
                    output_str += '{},"{}",'.format(model_name, pred_cmd.replace('"', '""'))

                    command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
                    structure_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
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


def tabulate_example_predictions(dataset, FLAGS, num_examples=100):
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, tokenizer_selector=tokenizer_selector)

    model_names, model_predictions = load_all_model_predictions(
        grouped_dataset, FLAGS, top_k=1)

    # Get FIXED dev set samples
    random.seed(100)
    example_ids = list(range(len(grouped_dataset)))
    random.shuffle(example_ids)
    sample_ids = example_ids[:num_examples]

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluations(
            os.path.join(FLAGS.data_dir, 'manual_judgements'))

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    model_name_pt = {
        'token-seq2seq': 'T-Seq2Seq',
        'tellina': 'Tellina',
        'token-copynet': 'T-CopyNet',
        'partial.token-seq2seq': 'ST-Seq2Seq',
        'partial.token-copynet': 'ST-CopyNet',
        'char-seq2seq': 'C-Seq2Seq',
        'char-copynet': 'C-CopyNet'
    }

    for example_id in sample_ids:
        print('Example {}'.format(example_id))
        data_group = grouped_dataset[example_id][1]
        sc_txt = data_group[0].sc_txt.strip()
        sc_key = get_example_nl_key(sc_txt)
        command_gts = [dp.tg_txt for dp in data_group]
        command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
        output_strs = {}
        for model_id, model_name in enumerate(model_names):
            predictions = model_predictions[model_id][example_id]
            for i in xrange(min(3, len(predictions))):
                pred_cmd = predictions[i]
                pred_tree = cmd_parser(pred_cmd)
                pred_temp = data_tools.ast2template(pred_tree, loose_constraints=True)
                temp_match = tree_dist.one_match(
                    command_gt_asts, pred_tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, pred_tree, ignore_arg_value=False)
                
                output_str = '& \\<{}> & {}'.format(pred_cmd.replace('__SP__', '')
                                                           .replace('_', '\\_')
                                                           .replace('$', '\\$')
                                                           .replace('%', '\\%')
                                                           .replace('{{}}', '\\ttcbs'), 
                                                   model_name_pt[model_name])

                command_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
                structure_example_sig = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
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
                output_str += ', {},{} \\\\'.format(structure_eval, command_eval)
            output_strs[model_name] = output_str
        for model_name in ['char-seq2seq', 
                           'char-copynet', 
                           'token-seq2seq', 
                           'token-copynet',
                           'partial.token-seq2seq',
                           'partial.token-copynet',
                           'tellina']:
            if model_name == 'char-seq2seq':
                print('\\multirow{{7}}{{*}}{{\\specialcell{{{}}}}} '.format(sc_txt) + output_strs[model_name])
            else:
                print(output_strs[model_name])
        output_str = '& \<{}> & Human \\\\'.format(command_gts[0].replace('__SP__', '')
                                                           .replace('_', '\\_')
                                                           .replace('$', '\\$')
                                                           .replace('%', '\\%')
                                                           .replace('{{}}', '\\ttcbs'))
        print(output_str)
        print()


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
            ind, utility, _, _ = line.split(',')
            utility_index[utility] = ind

    grammar_errors = collections.defaultdict(list) if group_by_utility else []
    argument_errors = collections.defaultdict(list) if group_by_utility else []
    example_id = 0
    for nl_temp, data_group in grouped_dataset:
        sc_txt = data_group[0].sc_txt.strip()
        sc_temp = get_example_nl_key(sc_txt)
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

            example_sig = '{}<NL_PREDICTION>{}'.format(sc_temp, pred_cmd)
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
        dataset, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    prediction_path = os.path.join(model_dir, 'predictions.{}.latest'.format(decode_sig))
    prediction_list = load_predictions(prediction_path, top_k)
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


def gen_error_analysis_csv_by_utility(model_dir, decode_sig, dataset, FLAGS, top_k=10):
    """
    Generate error analysis evaluation sheet grouped by utility.
    """
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, tokenizer_selector=tokenizer_selector)

    # Load model predictions
    prediction_path = os.path.join(model_dir, 'predictions.{}.latest'.format(decode_sig))
    prediction_list = load_predictions(prediction_path, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError(
            "ground truth and predictions length must be equal: {} vs. {}"
            .format(len(grouped_dataset), len(prediction_list)))

    # Load cached evaluation results
    cached_evaluation_results = load_cached_evaluations(model_dir)

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
