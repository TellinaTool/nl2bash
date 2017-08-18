"""
Compute translation accuracy of a system.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import csv
import numpy as np
import os, sys
import random

if sys.version_info > (3, 0):
    from six.moves import xrange

from encoder_decoder import data_utils
from bashlint import data_tools, nast
from eval import token_based, tree_dist, zss
from eval.eval_db import DBConnection
from eval.dfa_equal import regexDFAEquals


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
        use_temp=(eval_bash and FLAGS.normalized),
        tokenizer_selector=tokenizer_selector)
    top_k_temp_correct = np.zeros([len(grouped_dataset), top_k])
    top_k_str_correct = np.zeros([len(grouped_dataset), top_k])
    if eval_bash:
        top_k_cms = np.zeros([len(grouped_dataset), top_k])

    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: {} vs. {}"
            .format(len(grouped_dataset), len(prediction_list)))
    
    with DBConnection() as db:
        num_eval = 0
        for data_id in xrange(len(grouped_dataset)):
            key, data_group = grouped_dataset[data_id]
            sc_str = data_group[0].sc_txt
            tg_strs = [dp.tg_txt.strip() for dp in data_group]
            num_gts = len(tg_strs)
            if eval_bash:
                gt_trees = [cmd_parser(cm_str) for cm_str in tg_strs]
                gts = gt_trees + \
                      [cmd_parser(cmd) for cmd in db.get_correct_temps(sc_str)]
            else:
                gts = tg_strs + db.get_correct_temps(sc_str)

            if verbose:
                print("Example {} ({})".format(data_id, len(tg_strs)))
                print("Original Source: {}".format(sc_str))
                print("Source: {}".format(key))
                for j in xrange(len(tg_strs)):
                    print("GT Target {}: ".format(j+1) + tg_strs[j].strip())
            num_eval += (1 if eval_bash else num_gts)

            predictions = prediction_list[data_id]
            for i in xrange(len(predictions)):
                pred_cmd = predictions[i]
                tree = cmd_parser(pred_cmd)
                unprocessed_pred_cmd = regexDFAEquals.unprocess_regex(pred_cmd)
                # evaluation ignoring flag orders
                if eval_bash:
                    temp_match = tree_dist.one_match(gts, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(gts, tree, ignore_arg_value=False)
                else:
                    if eval_regex:
                        str_match = False
                        for cmd_str in gts:
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
                        str_match = pred_cmd in gts
                    temp_match = str_match

                cms = token_based.command_match_score(gts, tree) \
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


def manual_eval(model, dataset, FLAGS, output_dir, num_eval=None):
    num_top1_correct_temp = 0.0
    num_top3_correct_temp = 0.0
    num_top5_correct_temp = 0.0
    num_top10_correct_temp = 0.0
    num_top1_correct = 0.0
    num_top3_correct = 0.0
    num_top5_correct = 0.0
    num_top10_correct = 0.0
    num_evaled = 0

    eval_bash = FLAGS.dataset.startswith("bash")
    use_bucket = False if model == "knn" else True
    tokenizer_selector = 'cm' if FLAGS.explain else 'nl'
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_bucket=use_bucket, use_temp=eval_bash,
        tokenizer_selector=tokenizer_selector)

    if num_eval is None:
        num_eval = len(grouped_dataset)

    cmd_parser = data_tools.bash_parser if FLAGS.dataset.startswith("bash") \
        else data_tools.paren_parser

    o_f = open(os.path.join(output_dir, "manual.eval.results"), 'w')

    rejudge = False

    with DBConnection() as db:
        db.create_schema()
        while num_evaled < len(grouped_dataset):
            nl_strs, tg_strs, nls, search_historys = grouped_dataset[num_evaled]
            nl_str = nl_strs[0].decode('utf-8')

            if num_evaled == num_eval:
                break

            gt_trees = [cmd_parser(cmd) for cmd in tg_strs]

            predictions = db.get_top_k_predictions(model, nl_str, k=10)

            top1_correct_temp, top3_correct_temp, top5_correct_temp, \
                top10_correct_temp = False, False, False, False
            top1_correct, top3_correct, top5_correct, top10_correct = \
                False, False, False, False

            # evaluation ignoring ordering of flags
            print("Example %d (%d)" % (num_evaled+1, len(tg_strs)))
            o_f.write("Example %d (%d)" % (num_evaled+1, len(tg_strs)) + "\n")
            print("English: " + nl_str.strip())
            o_f.write("English: " + nl_str.encode('utf-8'))
            for j in xrange(len(tg_strs)):
                print("GT Command %d: " % (j+1) + tg_strs[j].strip())
                o_f.write("GT Command %d: " % (j+1) + tg_strs[j].strip() + "\n")

            pred_id = 0
            while pred_id < min(3, len(predictions)):
                pred_cmd, score = predictions[pred_id]
                tree = cmd_parser(pred_cmd)
                print("Prediction {}: {} ({})".format(pred_id+1, pred_cmd, score))
                o_f.write("Prediction {}: {} ({})\n".format(pred_id+1, pred_cmd, score))
                print()
                pred_temp = data_tools.ast2template(tree, loose_constraints=True)
                str_judge = db.get_str_judgement((nl_str, pred_cmd))
                temp_judge = db.get_temp_judgement((nl_str, pred_temp))
                if temp_judge is not None and not rejudge:
                    judgement_str = "y" if temp_judge == 1 \
                        else "n ({})".format(error_types[temp_judge])
                    print("Is the command template correct [y/n]? %s" % judgement_str)
                else:
                    temp_judge = tree_dist.one_match(gt_trees, tree, rewrite=False,
                                                     ignore_arg_value=True)
                    if not temp_judge:
                        inp = raw_input("Is the command template correct [y/n]? ")
                        if inp == "REVERSE":
                            rejudge = True
                        else:
                            if inp == "y":
                                temp_judge = True
                                db.add_temp_judgement((nl_str, pred_temp, 1))
                            else:
                                temp_judge = False
                                error_type = raw_input(
                                    "Error type: \n"
                                    "(2) extra utility \n"
                                    "(3) missing utility \n"
                                    "(4) confused utility \n"
                                    "(5) extra flag \n"
                                    "(6) missing flag \n"
                                    "(7) confused flag \n"
                                    "(8) logic error\n"
                                    "(9) count error\n"
                                )
                                db.add_temp_judgement((nl_str, pred_temp, int(error_type)))
                            rejudge = False
                    else:
                        print("Is the command template correct [y/n]? y")
                if temp_judge == 1:
                    if pred_id < 1:
                        top1_correct_temp = True
                        top3_correct_temp = True
                        top5_correct_temp = True
                        top10_correct_temp = True
                    elif pred_id < 3:
                        top3_correct_temp = True
                        top5_correct_temp = True
                        top10_correct_temp = True
                    elif pred_id < 5:
                        top5_correct_temp = True
                        top10_correct_temp = True
                    elif pred_id < 10:
                        top10_correct_temp = True
                    o_f.write("C")
                    if str_judge is not None and not rejudge:
                        judgement_str = "y" if str_judge == 1 \
                            else "n ({})".format(error_types[str_judge])
                        print("Is the complete command correct [y/n]? %s" % judgement_str)
                    else:
                        str_judge = tree_dist.one_match(
                            gt_trees, tree, rewrite=False, ignore_arg_value=False)
                        if not str_judge:
                            inp = raw_input("Is the complete command correct [y/n]? ")
                            if inp == "REVERSE":
                                rejudge = True
                                continue
                            elif inp == "y":
                                str_judge = True
                                o_f.write("C")
                                db.add_str_judgement((nl_str, pred_cmd, 1))
                            else:
                                str_judge = False
                                o_f.write("W")
                                db.add_str_judgement((nl_str, pred_cmd, 0))
                        else:
                            print("Is the complete command correct [y/n]? y")
                    if str_judge == 1:
                        if pred_id < 1:
                            top1_correct = True
                            top3_correct = True
                            top5_correct = True
                            top10_correct = True
                        elif pred_id < 3:
                            top3_correct = True
                            top5_correct = True
                            top10_correct = True
                        elif pred_id < 5:
                            top5_correct = True
                            top10_correct = True
                        elif pred_id < 10:
                            top10_correct = True
                        o_f.write("C")
                    else:
                        o_f.write("W")
                else:
                    o_f.write("WW")

                o_f.write("\n")
                o_f.write("\n")

                pred_id += 1

            if rejudge:
                num_evaled -= 1
            else:
                num_evaled += 1
                if top1_correct_temp:
                    num_top1_correct_temp += 1
                if top3_correct_temp:
                    num_top3_correct_temp += 1
                if top5_correct_temp:
                    num_top5_correct_temp += 1
                if top10_correct_temp:
                    num_top10_correct_temp += 1
                if top1_correct:
                    num_top1_correct += 1
                if top3_correct:
                    num_top3_correct += 1
                if top5_correct:
                    num_top5_correct += 1
                if top10_correct:
                    num_top10_correct += 1
            
            rejudge = False
            
            print()

    print("%d examples evaluated" % num_eval)
    print("Top 1 Template Match Score = %.2f" % (num_top1_correct_temp/num_eval))
    print("Top 1 String Match Score = %.2f" % (num_top1_correct/num_eval))
    if len(predictions) > 3:
        print("Top 5 Template Match Score = %.2f" % (num_top5_correct_temp/num_eval))
        print("Top 5 String Match Score = %.2f" % (num_top5_correct/num_eval))
        print("Top 10 Template Match Score = %.2f" % (num_top10_correct_temp/num_eval))
        print("Top 10 String Match Score = %.2f" % (num_top10_correct/num_eval))
    print()

    o_f.write("%d examples evaluated" % num_eval + "\n")
    o_f.write("Top 1 Template MatchScore = %.2f" % (num_top1_correct_temp/num_eval) + "\n")
    o_f.write("Top 1 String Match Score = %.2f" % (num_top1_correct/num_eval) + "\n")
    if len(predictions) > 1:
        o_f.write("Top 5 Template Match Score = %.2f" % (num_top5_correct_temp/num_eval) + "\n")
        o_f.write("Top 5 String Match Score = %.2f" % (num_top5_correct/num_eval) + "\n")
        o_f.write("Top 10 Template Match Score = %.2f" % (num_top10_correct_temp/num_eval) + "\n")
        o_f.write("Top 10 String Match Score = %.2f" % (num_top10_correct/num_eval) + "\n")
    o_f.write("\n")


def gen_eval_sheet(model_dir, decode_sig, dataset, FLAGS, output_path, top_k=3):
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
            dataset, use_temp=False, use_bucket=True, 
            tokenizer_selector=tokenizer_selector)
        prediction_list = load_predictions(model_dir, decode_sig, top_k)
        if len(grouped_dataset) != len(prediction_list):
            raise ValueError("ground truth and predictions length must be equal: {} vs. {}"
                .format(len(grouped_dataset), len(prediction_list)))

        example_id = 0
        with DBConnection() as db:
            for nl_temp, data_group in grouped_dataset:
                tg_strs = [dp.tg_txt for dp in data_group]
                gt_trees = [cmd_parser(cm_str) for cm_str in tg_strs]
                gt_trees = gt_trees + [cmd_parser(cmd)
                                       for cmd in db.get_correct_temps(nl_temp)]
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
                    temp_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=False)
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


def gen_error_analysis_sheet(model_dir, decode_sig, dataset, FLAGS, top_k=3):
    """
    Generate error analysis evaluation sheet.
    """
    # print evaluation form header
    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser
    tokenizer_selector = "cm" if FLAGS.explain else "nl"
    grouped_dataset = data_utils.group_parallel_data(
        dataset, use_temp=False, use_bucket=True,
        tokenizer_selector=tokenizer_selector)

    prediction_list = load_predictions(model_dir, decode_sig, top_k)
    if len(grouped_dataset) != len(prediction_list):
        raise ValueError("ground truth and predictions length must be equal: {} vs. {}"
            .format(len(grouped_dataset), len(prediction_list)))

    example_id = 0
    with DBConnection() as db:
        grammar_errors, argument_errors = [], []
        for nl_temp, data_group in grouped_dataset:
            tg_strs = [dp.tg_txt for dp in data_group]
            gt_trees = [cmd_parser(cm_str) for cm_str in tg_strs]
            gt_trees = gt_trees + \
                [cmd_parser(cmd) for cmd in db.get_correct_temps(nl_temp)]
            predictions = prediction_list[example_id]
            example_id += 1
            example = []
            grammar_error, argument_error = False, False
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
                if not str_match:
                    if temp_match:
                        output_str += 'y,'
                        if i == 0:
                            argument_error = True
                    else:
                        if i == 0:
                            grammar_error = True
                    example.append(output_str)
            if grammar_error:
                grammar_errors.append(example)
            else:
                argument_errors.append(example)
            example_id += 1

    grammar_error_path = os.path.join(model_dir, 'grammar.error.analysis.csv')
    arg_error_path = os.path.join(model_dir, 'argument.error.analysis.csv')
    random.shuffle(argument_errors)
    random.shuffle(grammar_errors)
    with open(grammar_error_path, 'w') as grammar_error_file:
        with open(arg_error_path, 'w') as arg_error_file:
            arg_error_file.write(
                'example_id, description, ground_truth, prediction, ' +
                'correct command, correct template\n')
            for line in argument_errors[:100]:
                arg_error_file.write('{}\n'.format(line))
            grammar_error_file.write(
                'example_id, description, ground_truth, prediction, ' +
                'correct command, correct template\n')
            for line in grammar_errors[:100]:
                grammar_error_file.write('{}\n'.format(line))


def import_manual_annotations_from_files(input_dir):
    """
    Import manual annotations to the database to extend the set of ground truths.

    :param input_dir: Directory where the manual annotation CSV files are stored.
        - If there is only one file in the input directory, read the annotations
            as they are.
        - If there are multiple files in the input directory, read the annotations
            as the majority voting of them.
    """
    def parse_csv(file_name):
        """parse a file into a log for evaluation"""
        task_log = {}
        with open(os.path.join(input_dir, file_name)) as csvfile:
            reader = csv.DictReader(csvfile)
            current_task = {}
            for row in reader:
                if row["id"] != "":
                    assert(row["description"] != "" )
                    if current_task:
                        task_log[current_task["id"]] = current_task
                    current_task = {}
                    current_task["id"] = int(row["id"])
                    current_task["description"] = row["description"]
                    current_task["top_solutions"] = []
                solution = {}
                solution["command"] = row["command"]
                solution["template_correct"] = False \
                    if row["correct template"] == "x" else True
                solution["command_correct"] = False \
                    if row["correct command"] == "x" else True
                current_task["top_solutions"].append(solution)
        return task_log

    def merge_log(task_logs):
        """merge multiple logs by majority voting"""
        num_logs = len(task_logs)
        vote_threshold = num_logs / 2 + 1
        merged_log = copy.deepcopy(task_logs[0])
        uncertain_cnt = 0
        weak_uncertain_cnt = 0
        total_cnt = 0
        for task_id in merged_log:
            task = merged_log[task_id]
            for i in range(len(task["top_solutions"])):
                command_correct_vote = 0
                template_correct_vote = 0
                for log in task_logs:
                    solution = log[task_id]["top_solutions"][i]
                    if solution["command_correct"]:
                        command_correct_vote += 1
                    if solution["template_correct"]:
                        template_correct_vote += 1

                # the following code section calculates command properties
                total_cnt += 1
                if command_correct_vote != 0 and command_correct_vote != num_logs \
                        and template_correct_vote != 0 and template_correct_vote != num_logs:
                    uncertain_cnt += 1
                if (command_correct_vote != 0 and command_correct_vote != num_logs) \
                        or (template_correct_vote != 0 and template_correct_vote != num_logs):
                    weak_uncertain_cnt += 1
                task["top_solutions"][i]["command_correct"] = True \
                    if command_correct_vote >= vote_threshold else False
                task["top_solutions"][i]["template_correct"] = True \
                    if template_correct_vote >= vote_threshold else False
        print("Total: ", total_cnt, "Uncertain ones: ", uncertain_cnt,
              "Weak uncertain ones: ", weak_uncertain_cnt)
        return merged_log

    task_logs = []
    for f_name in os.listdir(input_dir):
        if f_name.endswith('.csv'):
            task_log = parse_csv(f_name)
            task_logs.append(task_log)
    if len(task_logs) > 1:
        annotation_log = merge_log(task_logs)
    else:
        annotation_log = task_logs[0]

    with DBConnection() as db:
        for task_id in annotation_log:
            task = annotation_log[task_id]
            for i in range(len(task["top_solutions"])):
                solution = task["top_solutions"][i]
                if solution["command_correct"]:
                    db.add_str_judgement(
                        (task["description"], solution["command"], 1))
                if solution["template_correct"]:
                    print((task["description"], solution["command"], 1))
                    db.add_temp_judgement(
                        (task["description"], solution["command"], 1))


def load_predictions(model_dir, decode_sig, top_k):
    """
    Load model predictions (top_k per example) from disk.

    :param pred_dir: Directory where the model prediction file is stored.
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


def import_manual_annotation():
    input_dir = sys.argv[1]
    import_manual_annotations_from_files(input_dir)


if __name__ == "__main__":
    import_manual_annotation()
