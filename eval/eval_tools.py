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
import eval.bleu as bl
from nlp_tools import constants, tokenizer
import utils.ops


def gen_evaluation_table(dataset, FLAGS, num_examples=100, interactive=True):
    """
    Generate structure and full command accuracy results on a fixed set of dev/test
        set samples, with the results of multiple models tabulated in the same table.
    :param interactive:
        - If set, prompt the user to enter judgement if a prediction does not
            match any of the groundtruths and the correctness of the prediction
            has not been pre-determined;
          Otherwise, count all predictions that does not match any of the
          groundtruths as wrong.
    """
    def add_judgement(data_dir, nl, command, correct_template='', correct_command=''):
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

    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

    if FLAGS.test:
        model_names, model_predictions = load_all_model_predictions(
            grouped_dataset, FLAGS, top_k=3,
            tellina=True,
            partial_token_copynet=True,
            token_seq2seq=False,
            token_copynet=False,
            char_seq2seq=False,
            char_copynet=False,
            partial_token_seq2seq=False)
    else:
        model_names, model_predictions = load_all_model_predictions(
            grouped_dataset, FLAGS, top_k=3)

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

    # Interactive manual evaluation interface
    num_s_correct = collections.defaultdict(int)
    num_f_correct = collections.defaultdict(int)
    num_s_top_3_correct = collections.defaultdict(int)
    num_f_top_3_correct = collections.defaultdict(int)
    for exam_id, example_id in enumerate(sample_ids):
        data_group = grouped_dataset[example_id][1]
        sc_txt = data_group[0].sc_txt.strip()
        sc_key = get_example_nl_key(sc_txt)
        command_gts = [get_example_cm_key(dp.tg_txt) for dp in data_group]
        command_gt_asts = [data_tools.bash_parser(gt) for gt in command_gts]
        for model_id, model_name in enumerate(model_names):
            predictions = model_predictions[model_id][example_id]
            top_3_s_correct_marked = False
            top_3_f_correct_marked = False
            for i in xrange(min(3, len(predictions))):
                pred_cmd = predictions[i]
                pred_cmd_key = get_example_cm_key(pred_cmd)
                pred_ast = cmd_parser(pred_cmd_key)
                pred_temp = data_tools.ast2template(pred_ast, loose_constraints=True)
                temp_match = tree_dist.one_match(
                    command_gt_asts, pred_ast, ignore_arg_value=True)
                str_match = tree_dist.one_match(
                    command_gt_asts, pred_ast, ignore_arg_value=False)
                # Match ground truths & exisitng judgements
                command_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd_key)
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
                            add_judgement(FLAGS.data_dir, sc_key, pred_cmd_key,
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
                            add_judgement(FLAGS.data_dir, sc_key, pred_cmd_key,
                                          structure_eval, command_eval)
                            print()
                    structure_eval_cache[structure_example_key] = structure_eval
                    command_eval_cache[command_example_key] = command_eval
                if structure_eval == 'y':
                    if i == 0:
                        num_s_correct[model_name] += 1
                    if not top_3_s_correct_marked:
                        num_s_top_3_correct[model_name] += 1
                        top_3_s_correct_marked = True
                if command_eval == 'y':
                    if i == 0:
                        num_f_correct[model_name] += 1
                    if not top_3_f_correct_marked:
                        num_f_top_3_correct[model_name] += 1
                        top_3_f_correct_marked = True

    # print evaluation table
    # compute model name length offset
    max_len = len(max(model_names, key=len))
    max_len_with_offset = (int(max_len / 4) + 1) * 4
    first_line = '{}Acc_F_1    Acc_F_3    Acc_T_1    Acc_T_3'.format(
        utils.ops.padding_spaces('Model', max_len_with_offset))
    print(first_line)
    print('-' * len(first_line))
    for i, model_name in enumerate(model_names):
        print('{}{:.2f}    {:.2f}    {:.2f}    {:.2f}'.format(
            utils.ops.padding_spaces(model_name, max_len_with_offset),
            num_f_correct[model_name] / len(sample_ids),
            num_f_top_3_correct[model_name] / len(sample_ids),
            num_s_correct[model_name] / len(sample_ids),
            num_s_top_3_correct[model_name] / len(sample_ids)))
    print('-' * len(first_line))


def gen_automatic_eval_table(dataset, FLAGS, num_examples=100, interactive=True):
    # Group dataset
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)
    pass


def get_automatic_evaluation_metrics(model_dir, decode_sig, dataset, top_k, FLAGS,
                                     manual_samples_only=False, verbose=False):
    """
    Generate automatic evaluation metrics on a dev/test set.
    The following metrics are computed:
        Top 1,3,5,10
            1. Structure accuracy
            2. Full command accuracy
            3. Command keyword overlap
            4. BLEU
    """
    cmd_parser = data_tools.bash_parser

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
    template_translations = None
    command_translations = None
    template_translations, command_translations = \
        load_cached_correct_translations(os.path.join(FLAGS.data_dir, 'manual_judgements'),
                                         treat_empty_as_correct=True)

    # Compute manual evaluation scores on a subset of examples
    if manual_samples_only:
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

    for data_id in xrange(len(grouped_dataset)):
        _, data_group = grouped_dataset[data_id]
        sc_str = data_group[0].sc_txt.strip()
        sc_key = get_example_nl_key(sc_str)
        sc_tokens = [rev_sc_vocab[i] for i in data_group[0].sc_ids]
        if FLAGS.channel == 'char':
            sc_features = ''.join(sc_tokens)
            sc_features = sc_features.replace(constants._SPACE, ' ')
        else:
            sc_features = ' '.join(sc_tokens)
        command_gts = [get_example_cm_key(dp.tg_txt.strip()) for dp in data_group]
        if command_translations:
            command_gts = set(command_gts) | command_translations[sc_key]
        command_gt_asts = [data_tools.bash_parser(cmd) for cmd in command_gts]
        template_gts = [data_tools.cmd2template(cmd, loose_constraints=True) for cmd in command_gts]
        if template_translations:
            template_gts = set(template_gts) | template_translations[sc_key]
        template_gt_asts = [data_tools.bash_parser(temp) for temp in template_gts]

        if verbose:
            print("Example {}".format(data_id))
            print("Original Source: {}".format(sc_str))
            print("Source: {}".format(sc_features))
            for j, command_gt in enumerate(command_gts):
                print("GT Target {}: ".format(j + 1) + command_gt.strip())
        num_eval += 1
        predictions = prediction_list[data_id]
        for i in xrange(len(predictions)):
            pred_cmd = predictions[i]
            pred_cmd_key = get_example_cm_key(pred_cmd)
            pred_ast = cmd_parser(pred_cmd_key)
            # evaluation ignoring flag orders
            temp_match = tree_dist.one_match(
                template_gt_asts, pred_ast, ignore_arg_value=True)
            str_match = tree_dist.one_match(
                command_gt_asts, pred_ast, ignore_arg_value=False)
            if temp_match:
                top_k_temp_correct[data_id, i] = 1
            if str_match:
                top_k_str_correct[data_id, i] = 1
            cms = token_based.command_match_score(template_gt_asts, pred_ast)
            bleu = nltk.translate.bleu_score.sentence_bleu(command_gts, pred_cmd)
            top_k_cms[data_id, i] = cms
            top_k_bleu[data_id, i] = bleu
            if verbose:
                print("Prediction {}: {} ({})".format(i + 1, pred_cmd, cms))

        if verbose:
            print()

    top_temp_acc = [-1 for _ in [1, 3, 5, 10]]
    top_cmd_acc = [-1 for _ in [1, 3, 5, 10]]
    top_cms = [-1 for _ in [1, 3, 5, 10]]
    top_bleu = [-1 for _ in [1, 3, 5, 10]]
    top_temp_acc[0] = top_k_temp_correct[:, 0].mean()
    top_cmd_acc[0] = top_k_str_correct[:, 0].mean()
    top_cms[0] = top_k_cms[:, 0].mean()
    top_bleu[0] = top_k_bleu[:, 0].mean()
    if verbose:
        print("%d examples evaluated" % num_eval)
        print("Top 1 Match (template-only) = %.3f" % top_temp_acc[0])
        print("Top 1 Match (whole-string) = %.3f" % top_cmd_acc[0])
        print("Average top 1 Template Match Score = %.3f" % top_cms[0])
        print("Average top 1 BLEU Score = %.3f" % top_bleu[0])
    if len(predictions) > 1:
        top_temp_acc[1] = np.max(top_k_temp_correct[:, :3], 1).mean()
        top_cmd_acc[1] = np.max(top_k_str_correct[:, :3], 1).mean()
        top_cms[1] = np.max(top_k_cms[:, :3], 1).mean()
        top_bleu[1] = np.max(top_k_bleu[:, :3], 1).mean()
        print("Top 3 Match (template-only) = %.3f" % top_temp_acc[1])
        print("Top 3 Match (whole-string) = %.3f" % top_cmd_acc[1])
        print("Average top 3 Template Match Score = %.3f" % top_cms[1])
        print("Average top 3 BLEU Score = %.3f" % top_bleu[1])
    if len(predictions) > 3:
        top_temp_acc[2] = np.max(top_k_temp_correct[:, :5], 1).mean()
        top_cmd_acc[2] = np.max(top_k_str_correct[:, :5], 1).mean()
        top_cms[2] = np.max(top_k_cms[:, :5], 1).mean()
        top_bleu[2] = np.max(top_k_bleu[:, :5], 1).mean()
        print("Top 5 Match (template-only) = %.3f" % top_temp_acc[2])
        print("Top 5 Match (whole-string) = %.3f" % top_cmd_acc[2])
        print("Average top 5 Template Match Score = %.3f" % top_cms[2])
        print("Average top 5 BLEU Score = %.3f" % top_bleu[2])
    if len(predictions) > 5:
        top_temp_acc[3] = np.max(top_k_temp_correct[:, :10], 1).mean()
        top_cmd_acc[3] = np.max(top_k_str_correct[:, :10], 1).mean()
        top_cms[3] = np.max(top_k_cms[:, :10], 1).mean()
        top_bleu[3] = np.max(top_k_bleu[:, :10], 1).mean()
        print("Top 10 Match (template-only) = %.3f" % top_temp_acc[3])
        print("Top 10 Match (whole-string) = %.3f" % top_cmd_acc[3])
        print("Average top 10 Template Match Score = %.3f" % top_cms[3])
        print("Average top 10 BLEU Score = %.3f" % top_bleu[3])
    print()

    M = {}
    M['top_temp_acc'] = top_temp_acc
    M['top_cmd_acc'] = top_cmd_acc
    M['top_cms'] = top_cms
    M['top_bleu'] = top_bleu

    return M


def load_all_model_predictions(grouped_dataset, FLAGS, top_k=1,
                               tellina=True,
                               token_seq2seq=True,
                               token_copynet=True,
                               char_seq2seq=True,
                               char_copynet=True,
                               partial_token_seq2seq=True,
                               partial_token_copynet=True,):
    """
    Load predictions of multiple models.

    :param dataset: The dataset over which the predictions are generated.
    :param FLAGS: Experiment hyperparametrs.
    :param tellina,
           token_seq2seq,
           token_copynet,
           char_seq2seq,
           char_copynet
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
        prediction_list = load_predictions(model_dir, decode_sig, top_k)
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
        FLAGS.fill_argument_slots = False
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
            FLAGS.use_copy = False
        # -- Parital token
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
            FLAGS.use_copy = False
        # -- Character
        FLAGS.channel = 'char'
        FLAGS.batch_size = 32
        FLAGS.min_vocab_frequency = 1
        # --- Seq2Seq
        if char_seq2seq:
            model_names.append('char-seq2seq')
            model_predictions.append(load_model_predictions())
        # --= CopyNet
        if char_copynet:
            FLAGS.use_copy = True
            FLAGS.copy_fun = 'copynet'
            model_names.append('char-copynet')
            model_predictions.append(load_model_predictions())
            FLAGS.use_copy = False

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
                pred_cmd_key = get_example_nl_key(pred_cmd)
                if 'template' in row:
                    pred_temp_key = get_example_cm_key(row['template'])
                else:
                    pred_temp_key = data_tools.cmd2template(pred_cmd_key, loose_constraints=True)
                structure_eval = row['correct template']
                if treat_empty_as_correct:
                    structure_eval = normalize_judgement(structure_eval)
                command_eval = row['correct command']
                if treat_empty_as_correct:
                    command_eval = normalize_judgement(command_eval)
                if structure_eval == 'y':
                    template_translations[current_nl_key].add(pred_temp_key)
                if command_eval == 'y':
                    command_translations[current_nl_key].add(pred_cmd_key)
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
    with open(input_file) as f:
        if verbose:
            print('reading cached evaluations from {}'.format(input_file))
        reader = csv.DictReader(f)
        current_nl_key = ''
        for row in reader:
            if row['description']:
                current_nl_key = get_example_nl_key(row['description'])
            pred_cmd = row['prediction']
            pred_cmd_key = get_example_cm_key(pred_cmd)
            if 'template' in row:
                pred_temp = row['template']
            else:
                pred_temp = data_tools.cmd2template(pred_cmd_key, loose_constraints=True)
            command_eval = row['correct command']
            if treat_empty_as_correct:
                command_eval = normalize_judgement(command_eval)
            command_example_key = '{}<NL_PREDICTION>{}'.format(current_nl_key, pred_cmd_key)
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
    Get the command in an example with nuances removed.
    """
    return tree_dist.ignore_differences(cm)


def normalize_judgement(x):
    if not x or x.lower() == 'y':
        return 'y'
    else:
        return 'n'
