"""
Evaluate system performance.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import nltk
import numpy as np
import os, sys
import random

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import data_tools
from encoder_decoder import data_utils, graph_utils
from eval import token_based, tree_dist
from nlp_tools import constants, tokenizer


def manual_eval(prediction_path, dataset, FLAGS, top_k, num_examples=-1, interactive=True, verbose=True):
    """
    Conduct dev/test set evaluation.

    Evaluation metrics:
        1) full command accuracy;
        2) command template accuracy. 

    :param interactive:
        - If set, prompt the user to enter judgement if a prediction does not
            match any of the groundtruths and the correctness of the prediction
            has not been pre-determined;
          Otherwise, all predictions that does not match any of the groundtruths are counted as wrong.
    """
    # Group dataset
    grouped_dataset = data_utils.group_parallel_data(dataset)

    # Load model prediction
    prediction_list = load_predictions(prediction_path, top_k)

    metrics = get_manual_evaluation_metrics(
        grouped_dataset, prediction_list, FLAGS, num_examples=num_examples, interactive=interactive, verbose=verbose)

    return metrics


def gen_manual_evaluation_table(dataset, FLAGS, num_examples=-1, interactive=True):
    """
    Conduct dev/test set evaluation. The results of multiple pre-specified models are tabulated in the same table.

    Evaluation metrics:
        1) full command accuracy;
        2) command template accuracy.
        
    :param interactive:
        - If set, prompt the user to enter judgement if a prediction does not
            match any of the groundtruths and the correctness of the prediction
            has not been pre-determined;
          Otherwise, all predictions that does not match any of the groundtruths are counted as wrong.
    """
    # Group dataset
    grouped_dataset = data_utils.group_parallel_data(dataset)

    # Load all model predictions
    model_names, model_predictions = load_all_model_predictions(grouped_dataset, FLAGS, top_k=3)

    manual_eval_metrics = {}
    for model_id, model_name in enumerate(model_names):
        prediction_list = model_predictions[model_names]
        M = get_manual_evaluation_metrics(
            grouped_dataset, prediction_list, FLAGS, num_examples=num_examples, interactive=interactive, verbose=False)
        manual_eval_metrics[model_name] = [M['acc_f'][0], M['acc_f'[1]], M['acc_t'][0], M['acc_t'][1]]

    metrics_names = ['Acc_F_1', 'Acc_F_3', 'Acc_T_1', 'Acc_T_3']
    print_eval_table(model_names, metrics_names, manual_eval_metrics)


def get_manual_evaluation_metrics(grouped_dataset, prediction_list, FLAGS, num_examples=-1, interactive=True,
                                  verbose=True):

    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: "
                         "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))

    # Get dev set samples (fixed)
    random.seed(100)
    example_ids = list(range(len(grouped_dataset)))
    random.shuffle(example_ids)
    if num_examples > 0:
        sample_ids = example_ids[:num_examples]
    else:
        sample_ids = example_ids

    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluations(
            os.path.join(FLAGS.data_dir, 'manual_judgements'), verbose=True)

    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    # Interactive manual evaluation
    num_t_top_1_correct = 0.0
    num_f_top_1_correct = 0.0
    num_t_top_3_correct = 0.0
    num_f_top_3_correct = 0.0

    for exam_id, example_id in enumerate(sample_ids):
        data_group = grouped_dataset[example_id][1]
        sc_txt = data_group[0].sc_txt.strip()
        sc_key = get_example_nl_key(sc_txt)
        command_gts = [dp.tg_txt for dp in data_group]
        command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
        predictions = prediction_list[example_id]
        top_3_s_correct_marked = False
        top_3_f_correct_marked = False
        for i in xrange(min(3, len(predictions))):
            pred_cmd = predictions[i]
            pred_ast = cmd_parser(pred_cmd)
            pred_temp = data_tools.ast2template(pred_ast, loose_constraints=True)
            temp_match = tree_dist.one_match(
                command_gt_asts, pred_ast, ignore_arg_value=True)
            str_match = tree_dist.one_match(
                command_gt_asts, pred_ast, ignore_arg_value=False)
            # Match ground truths & exisitng judgements
            command_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
            structure_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
            command_eval, structure_eval = '', ''
            if str_match:
                command_eval = 'y'
                structure_eval = 'y'
            elif temp_match:
                structure_eval = 'y'
            if command_eval_cache and command_example_key in command_eval_cache:
                command_eval = command_eval_cache[command_example_key]
            if structure_eval_cache and structure_example_key in structure_eval_cache:
                structure_eval = structure_eval_cache[structure_example_key]
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
                        add_judgement(FLAGS.data_dir, sc_txt, pred_cmd,
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
                        add_judgement(FLAGS.data_dir, sc_txt, pred_cmd,
                                      structure_eval, command_eval)
                        print()
                structure_eval_cache[structure_example_key] = structure_eval
                command_eval_cache[command_example_key] = command_eval
            if structure_eval == 'y':
                if i == 0:
                    num_t_top_1_correct += 1
                if not top_3_s_correct_marked:
                    num_t_top_3_correct += 1
                    top_3_s_correct_marked = True
            if command_eval == 'y':
                if i == 0:
                    num_f_top_1_correct += 1
                if not top_3_f_correct_marked:
                    num_f_top_3_correct += 1
                    top_3_f_correct_marked = True

    metrics = {}
    acc_f_1 = num_f_top_1_correct / len(sample_ids)
    acc_f_3 = num_f_top_3_correct / len(sample_ids)
    acc_t_1 = num_t_top_1_correct / len(sample_ids)
    acc_t_3 = num_t_top_3_correct / len(sample_ids)
    metrics['acc_f'] = [acc_f_1, acc_f_3]
    metrics['acc_t'] = [acc_t_1, acc_t_3]

    if verbose:
        print('{} examples evaluated'.format(len(sample_ids)))
        print('Top 1 Command Acc = {:.3f}'.format(acc_f_1))
        print('Top 3 Command Acc = {:.3f}'.format(acc_f_3))
        print('Top 1 Template Acc = {:.3f}'.format(acc_t_1))
        print('Top 3 Template Acc = {:.3f}'.format(acc_t_3))
    return metrics


def add_judgement(data_dir, nl, command, correct_template='', correct_command=''):
    """
    Append a new judgement
    """
    data_dir = os.path.join(data_dir, 'manual_judgements')
    manual_judgement_path = os.path.join(
        data_dir, 'manual.evaluations.author')
    if not os.path.exists(manual_judgement_path):
        with open(manual_judgement_path, 'w') as o_f:
            o_f.write(
                'description,prediction,template,correct template,correct command\n')
    with open(manual_judgement_path, 'a') as o_f:
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


def automatic_eval(prediction_path, dataset, FLAGS, top_k, num_samples=-1, verbose=False):
    """
    Generate automatic evaluation metrics on dev/test set.
    The following metrics are computed:
        Top 1,3,5,10
            1. Structure accuracy
            2. Full command accuracy
            3. Command keyword overlap
            4. BLEU
    """
    grouped_dataset = data_utils.group_parallel_data(dataset)
    try:
        vocabs = data_utils.load_vocabulary(FLAGS)
    except ValueError:
        vocabs = None

    # Load predictions
    prediction_list = load_predictions(prediction_path, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: "
                         "{} vs. {}".format(len(grouped_dataset), len(prediction_list)))

    metrics = get_automatic_evaluation_metrics(grouped_dataset, prediction_list, vocabs, FLAGS,
                                               top_k, num_samples, verbose)
    return metrics


def gen_automatic_evaluation_table(dataset, FLAGS):
    # Group dataset
    grouped_dataset = data_utils.group_parallel_data(dataset)
    vocabs = data_utils.load_vocabulary(FLAGS)

    model_names, model_predictions = load_all_model_predictions(grouped_dataset, FLAGS, top_k=3)
    auto_eval_metrics = {}
    for model_id, model_name in enumerate(model_names):
        prediction_list = model_predictions[model_id]
        if prediction_list is not None:
            M = get_automatic_evaluation_metrics(
                grouped_dataset, prediction_list, vocabs, FLAGS, top_k=3)
            auto_eval_metrics[model_name] = [M['bleu'][0], M['bleu'][1], M['cms'][0], M['cms'][1]]
        else:
            print('Model {} skipped in evaluation'.format(model_name))
    metrics_names = ['BLEU1', 'BLEU3', 'TM1', 'TM3']
    print_eval_table(model_names, metrics_names, auto_eval_metrics)


def get_automatic_evaluation_metrics(grouped_dataset, prediction_list, vocabs, FLAGS, top_k,
                                     num_samples=-1, verbose=False):
    cmd_parser = data_tools.bash_parser
    rev_sc_vocab = vocabs.rev_sc_vocab if vocabs is not None else None


    # Load cached evaluation results
    structure_eval_cache, command_eval_cache = \
        load_cached_evaluations(
            os.path.join(FLAGS.data_dir, 'manual_judgements'))

    # Compute manual evaluation scores on a subset of examples
    if num_samples > 0:
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
    top_k_cms = np.zeros([len(grouped_dataset), top_k])
    top_k_bleu = np.zeros([len(grouped_dataset), top_k])

    command_gt_asts_list, pred_ast_list = [], []
    
    for data_id in xrange(len(grouped_dataset)):
        _, data_group = grouped_dataset[data_id]
        sc_str = data_group[0].sc_txt.strip()
        sc_key = get_example_nl_key(sc_str)
        if vocabs is not None:
            sc_tokens = [rev_sc_vocab[i] for i in data_group[0].sc_ids]
            if FLAGS.channel == 'char':
                sc_features = ''.join(sc_tokens)
                sc_features = sc_features.replace(constants._SPACE, ' ')
            else:
                sc_features = ' '.join(sc_tokens)
        command_gts = [dp.tg_txt.strip() for dp in data_group]
        command_gt_asts = [cmd_parser(cmd) for cmd in command_gts]
        command_gt_asts_list.append(command_gt_asts)
        template_gts = [data_tools.cmd2template(cmd, loose_constraints=True) for cmd in command_gts]
        template_gt_asts = [cmd_parser(temp) for temp in template_gts]
        if verbose:
            print("Example {}".format(data_id))
            print("Original Source: {}".format(sc_str.encode('utf-8')))
            if vocabs is not None:
                print("Source: {}".format([x.encode('utf-8') for x in sc_features]))
            for j, command_gt in enumerate(command_gts):
                print("GT Target {}: {}".format(j + 1, command_gt.strip().encode('utf-8')))
        num_eval += 1
        predictions = prediction_list[data_id]
        for i in xrange(len(predictions)):
            pred_cmd = predictions[i]
            pred_ast = cmd_parser(pred_cmd)
            if i == 0:
                pred_ast_list.append(pred_ast)
            pred_temp = data_tools.cmd2template(pred_cmd, loose_constraints=True)
            # A) Exact match with ground truths & exisitng judgements
            command_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
            structure_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
            # B) Match ignoring flag orders
            temp_match = tree_dist.one_match(
                template_gt_asts, pred_ast, ignore_arg_value=True)
            str_match = tree_dist.one_match(
                command_gt_asts, pred_ast, ignore_arg_value=False)
            if command_eval_cache and command_example_key in command_eval_cache:
                str_match = normalize_judgement(command_eval_cache[command_example_key]) == 'y'
            if structure_eval_cache and structure_example_key in structure_eval_cache:
                temp_match = normalize_judgement(structure_eval_cache[structure_example_key]) == 'y'
            if temp_match:
                top_k_temp_correct[data_id, i] = 1
            if str_match:
                top_k_str_correct[data_id, i] = 1
            cms = token_based.command_match_score(command_gt_asts, pred_ast)
            # if pred_cmd.strip():
            #     bleu = token_based.sentence_bleu_score(command_gt_asts, pred_ast)   
            # else:
            #     bleu = 0
            bleu = nltk.translate.bleu_score.sentence_bleu(command_gts, pred_cmd)
            top_k_cms[data_id, i] = cms
            top_k_bleu[data_id, i] = bleu
            if verbose:
                print("Prediction {}: {} ({}, {})".format(i + 1, pred_cmd, cms, bleu))
        if verbose:
            print()
    
    bleu = token_based.corpus_bleu_score(command_gt_asts_list, pred_ast_list)

    top_temp_acc = [-1 for _ in [1, 3, 5, 10]]
    top_cmd_acc = [-1 for _ in [1, 3, 5, 10]]
    top_cms = [-1 for _ in [1, 3, 5, 10]]
    top_bleu = [-1 for _ in [1, 3, 5, 10]]
    top_temp_acc[0] = top_k_temp_correct[:, 0].mean()
    top_cmd_acc[0] = top_k_str_correct[:, 0].mean()
    top_cms[0] = top_k_cms[:, 0].mean()
    top_bleu[0] = top_k_bleu[:, 0].mean()
    print("{} examples evaluated".format(num_eval))
    print("Top 1 Template Acc = %.3f" % top_temp_acc[0])
    print("Top 1 Command Acc = %.3f" % top_cmd_acc[0])
    print("Average top 1 Template Match Score = %.3f" % top_cms[0])
    print("Average top 1 BLEU Score = %.3f" % top_bleu[0])
    if len(predictions) > 1:
        top_temp_acc[1] = np.max(top_k_temp_correct[:, :3], 1).mean()
        top_cmd_acc[1] = np.max(top_k_str_correct[:, :3], 1).mean()
        top_cms[1] = np.max(top_k_cms[:, :3], 1).mean()
        top_bleu[1] = np.max(top_k_bleu[:, :3], 1).mean()
        print("Top 3 Template Acc = %.3f" % top_temp_acc[1])
        print("Top 3 Command Acc = %.3f" % top_cmd_acc[1])
        print("Average top 3 Template Match Score = %.3f" % top_cms[1])
        print("Average top 3 BLEU Score = %.3f" % top_bleu[1])
    if len(predictions) > 3:
        top_temp_acc[2] = np.max(top_k_temp_correct[:, :5], 1).mean()
        top_cmd_acc[2] = np.max(top_k_str_correct[:, :5], 1).mean()
        top_cms[2] = np.max(top_k_cms[:, :5], 1).mean()
        top_bleu[2] = np.max(top_k_bleu[:, :5], 1).mean()
        print("Top 5 Template Acc = %.3f" % top_temp_acc[2])
        print("Top 5 Command Acc = %.3f" % top_cmd_acc[2])
        print("Average top 5 Template Match Score = %.3f" % top_cms[2])
        print("Average top 5 BLEU Score = %.3f" % top_bleu[2])
    if len(predictions) > 5:
        top_temp_acc[3] = np.max(top_k_temp_correct[:, :10], 1).mean()
        top_cmd_acc[3] = np.max(top_k_str_correct[:, :10], 1).mean()
        top_cms[3] = np.max(top_k_cms[:, :10], 1).mean()
        top_bleu[3] = np.max(top_k_bleu[:, :10], 1).mean()
        print("Top 10 Template Acc = %.3f" % top_temp_acc[3])
        print("Top 10 Command Acc = %.3f" % top_cmd_acc[3])
        print("Average top 10 Template Match Score = %.3f" % top_cms[3])
        print("Average top 10 BLEU Score = %.3f" % top_bleu[3])
    print('Corpus BLEU = %.3f' % bleu)
    print()

    metrics = {}
    metrics['acc_f'] = top_cmd_acc
    metrics['acc_t'] = top_temp_acc
    metrics['cms'] = top_cms
    metrics['bleu'] = top_bleu

    return metrics


def print_eval_table(model_names, metrics_names, model_metrics):

    def pad_spaces(s, max_len):
        return s + ' ' * (max_len - len(s))

    # print evaluation table
    # pad model names with spaces to create alignment
    max_len = len(max(model_names, key=len))
    max_len_with_offset = (int(max_len / 4) + 1) * 4
    first_row = pad_spaces('Model', max_len_with_offset)
    for metrics_name in metrics_names:
        first_row += '{}    '.format(metrics_name)
    print(first_row.strip())
    print('-' * len(first_row))
    for i, model_name in enumerate(model_names):
        row = pad_spaces(model_name, max_len_with_offset)
        for metrics in model_metrics[model_name]:
            row += '{:.2f}    '.format(metrics)
        print(row.strip())
    print('-' * len(first_row))


def load_all_model_predictions(grouped_dataset, FLAGS, top_k=1, model_names=('token_seq2seq',
                                                                             'token_copynet',
                                                                             'char_seq2seq',
                                                                             'char_copynet',
                                                                             'partial_token_seq2seq',
                                                                             'partial_token_copynet',
                                                                             'tellina')):
    """
    Load predictions of multiple models (specified with "model_names").

    :return model_predictions: List of model predictions.
    """

    def load_model_predictions():
        model_subdir, decode_sig = graph_utils.get_decode_signature(FLAGS)
        model_dir = os.path.join(FLAGS.model_root_dir, model_subdir)
        prediction_path = os.path.join(model_dir, 'predictions.{}.latest'.format(decode_sig))
        prediction_list = load_predictions(prediction_path, top_k)
        if prediction_list is not None and len(grouped_dataset) != len(prediction_list):
            raise ValueError("ground truth list and prediction list length must "
                             "be equal: {} vs. {}".format(len(grouped_dataset),
                                                          len(prediction_list)))
        return prediction_list

    # Load model predictions
    model_predictions = []

    # -- Token
    FLAGS.channel = 'token'
    FLAGS.normalized = False
    FLAGS.fill_argument_slots = False
    FLAGS.use_copy = False
    # --- Seq2Seq
    if 'token_seq2seq' in model_names:
        model_predictions.append(load_model_predictions())
    # --- Tellina
    if 'tellina' in model_names:
        FLAGS.normalized = True
        FLAGS.fill_argument_slots = True
        model_predictions.append(load_model_predictions())
        FLAGS.normalized = False
        FLAGS.fill_argument_slots = False
    # --- CopyNet
    if 'token_copynet' in model_names:
        FLAGS.use_copy = True
        FLAGS.copy_fun = 'copynet'
        model_predictions.append(load_model_predictions())
        FLAGS.use_copy = False
    # -- Parital token
    FLAGS.channel = 'partial.token'
    # --- Seq2Seq
    if 'partial_token_seq2seq' in model_names:
        model_predictions.append(load_model_predictions())
    # --- CopyNet
    if 'partial_token_copynet' in model_names:
        FLAGS.use_copy = True
        FLAGS.copy_fun = 'copynet'
        model_predictions.append(load_model_predictions())
        FLAGS.use_copy = False
    # -- Character
    FLAGS.channel = 'char'
    FLAGS.batch_size = 32
    FLAGS.min_vocab_frequency = 1
    # --- Seq2Seq
    if 'char_seq2seq' in model_names:
        model_predictions.append(load_model_predictions())
    # --= CopyNet
    if 'char_copynet' in model_names:
        FLAGS.use_copy = True
        FLAGS.copy_fun = 'copynet'
        model_predictions.append(load_model_predictions())
        FLAGS.use_copy = False

    return model_names, model_predictions


def load_predictions(prediction_path, top_k, verbose=True):
    """
    Load model predictions (top_k per example) from disk.

    :param prediction_path: path to the decoding output

        We assume the file is of the format:

            1. The i-th line of the file contains predictions for example i in the dataset'
            2. Each line contains top-k predictions separated by "|||".

    :param top_k: Maximum number of predictions to read per example.
    :return: List of top k predictions.
    """

    if os.path.exists(prediction_path):
        with open(prediction_path) as f:
            prediction_list = []
            for line in f:
                predictions = line.split('|||')
                prediction_list.append(predictions[:top_k])
    else:
        if verbose:
            print('Warning: file not found: {}'.format(prediction_path))
        return None
    if verbose:
        print('{} predictions loaded from {}'.format(
            len(prediction_list), prediction_path))
    return prediction_list


def load_cached_correct_translations(data_dir, treat_empty_as_correct=False, verbose=False):
    """
    Load cached correct translations from disk.

    :return: nl -> template translation map, nl -> command translation map
    """
    command_translations = collections.defaultdict(set)
    template_translations = collections.defaultdict(set)
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
            current_nl_key = ''
            for row in reader:
                if row['description']:
                    current_nl_key = get_example_nl_key(row['description'])
                pred_cmd = row['prediction']
                if 'template' in row:
                    pred_temp = row['template']
                else:
                    pred_temp = data_tools.cmd2template(pred_cmd, loose_constraints=True)
                structure_eval = row['correct template']
                if treat_empty_as_correct:
                    structure_eval = normalize_judgement(structure_eval)
                command_eval = row['correct command']
                if treat_empty_as_correct:
                    command_eval = normalize_judgement(command_eval)
                if structure_eval == 'y':
                    template_translations[current_nl_key].add(pred_temp)
                if command_eval == 'y':
                    command_translations[current_nl_key].add(pred_cmd)
    print('{} template translations loaded'.format(len(template_translations)))
    print('{} command translations loaded'.format(len(command_translations)))

    return template_translations, command_translations


def load_cached_evaluations(model_dir, verbose=True):
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
        ser, cer = load_cached_evaluations_from_file(manual_judgement_path, verbose=verbose)
        for key in ser:
            structure_eval_results[key] = ser[key]
        for key in cer:
            command_eval_results[key] = cer[key]
    if verbose:
        print('{} structure evaluation results loaded'.format(len(structure_eval_results)))
        print('{} command evaluation results loaded'.format(len(command_eval_results)))
    return structure_eval_results, command_eval_results


def load_cached_evaluations_from_file(input_file, treat_empty_as_correct=False, verbose=True):
    structure_eval_results = {}
    command_eval_results = {}
    with open(input_file, encoding='utf-8') as f:
        if verbose:
            print('reading cached evaluations from {}'.format(input_file))
        reader = csv.DictReader(f)
        current_nl_key = ''
        for row in reader:
            if row['description']:
                current_nl_key = get_example_nl_key(row['description'])
            pred_cmd = row['prediction']
            if 'template' in row:
                pred_temp = row['template']
            else:
                pred_temp = data_tools.cmd2template(pred_cmd, loose_constraints=True)
            command_eval = row['correct command']
            if treat_empty_as_correct:
                command_eval = normalize_judgement(command_eval)
            command_example_key = '{}<NL_PREDICTION>{}'.format(current_nl_key, pred_cmd)
            if command_eval:
                command_eval_results[command_example_key] = command_eval
            structure_eval = row['correct template']
            if treat_empty_as_correct:
                structure_eval = normalize_judgement(structure_eval)
            structure_example_key = '{}<NL_PREDICTION>{}'.format(current_nl_key, pred_temp)
            if structure_eval:
                structure_eval_results[structure_example_key] = structure_eval
    return structure_eval_results, command_eval_results


def get_example_nl_key(nl):
    """
    Get the natural language description in an example with nuances removed.
    """
    tokens, _ = tokenizer.basic_tokenizer(nl)
    return ' '.join(tokens)


def get_example_cm_key(cm):
    """
    TODO: implement command normalization
        1. flag order normalization
        2. flag format normalization (long flag vs. short flag)
        3. remove flags whose effect does not matter
    """
    return cm


def normalize_judgement(x):
    if not x or x.lower() == 'y':
        return 'y'
    else:
        return 'n'
