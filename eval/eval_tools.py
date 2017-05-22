"""
Compute translation accuracy of a system.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import os, sys

if sys.version_info > (3, 0):
    from six.moves import xrange

from encoder_decoder import data_utils
from bashlex import data_tools, nast
from eval import token_based, tree_dist, zss
from eval.eval_archive import DBConnection
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


def eval_set(model, dataset, top_k, FLAGS, verbose=True):
    eval_bash = FLAGS.dataset.startswith("bash") and not FLAGS.explain
    eval_regex = FLAGS.dataset.startswith("regex") and not FLAGS.explain

    num_eval = 0
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    use_bucket = False if model == "knn" else True

    tokenizer_selector = 'cm' if FLAGS.explain else 'nl'
    grouped_dataset = data_utils.group_data(
        dataset, use_bucket=use_bucket, use_temp=eval_bash,
        tokenizer_selector=tokenizer_selector)

    top_k_temp_correct = np.zeros([len(grouped_dataset), top_k])
    top_k_str_correct = np.zeros([len(grouped_dataset), top_k])
    if eval_bash:
        top_k_cms = np.zeros([len(grouped_dataset), top_k])

    with DBConnection() as db:
        data_id = 0
        for sc_temp in grouped_dataset:
            data_group = grouped_dataset[sc_temp]
            sc_str = bytes(data_group[0].sc_txt, 'utf-8')
            cm_strs = [dp.tg_txt.strip() for dp in data_group]
            num_gts = len(cm_strs)
            if eval_bash:
                gt_trees = [cmd_parser(cm_str) for cm_str in cm_strs]
                gts = gt_trees + \
                      [cmd_parser(cmd) for cmd in db.get_correct_temps(sc_str)]
            else:
                gts = cm_strs

            predictions = db.get_top_k_predictions(model, sc_str, k=top_k)

            if verbose:
                print("Example %d (%d)" % (num_eval, len(cm_strs)))
                print("Original Source: {}".format(sc_str.strip()))
                print("Source: " + sc_temp)
                for j in xrange(len(cm_strs)):
                    print("GT Target {}: ".format(j+1) + cm_strs[j].strip())
            num_eval += (1 if eval_bash else num_gts)

            for i in xrange(min(3, len(predictions))):
                pred_cmd, score = predictions[i]
                tree = cmd_parser(pred_cmd)

                if verbose:
                    if eval_bash:
                        print("Prediction {}: {} ({}) ({})".format(
                            i+1, pred_cmd, score, cms))
                    else:
                        print("Prediction {}: {} ({})".format(i+1, pred_cmd, score))

                # evaluation ignoring flag orders
                if eval_bash:
                    temp_match = tree_dist.one_match(
                        gts, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(
                        gts, tree, ignore_arg_value=False)
                else:
                    if eval_regex:
                        str_match = False
                        for cmd_str in gts:
                            if regexDFAEquals.regex_equiv_from_raw(cmd_str, pred_cmd):
                                str_match = True
                                # Debugging
                                if verbose:
                                    if cmd_str != pred_cmd:
                                        print("----------------------------------")
                                        print("1) {}".format(cmd_str))
                                        print("2) {}".format(pred_cmd))
                                        print("----------------------------------")
                                    else:
                                        print("----------------------------------")
                                        print("i) {}".format(cmd_str))
                                        print("ii) {}".format(pred_cmd))
                                        print("----------------------------------")
                                break
                            else:
                                if verbose:
                                    print("----------------------------------")
                                    print("A) {}".format(cmd_str))
                                    print("B) {}".format(pred_cmd))
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
    grouped_dataset = data_utils.group_data(
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
            nl_strs, cm_strs, nls, search_historys = grouped_dataset[num_evaled]
            nl_str = nl_strs[0].decode('utf-8')

            if num_evaled == num_eval:
                break

            gt_trees = [cmd_parser(cmd) for cmd in cm_strs]

            predictions = db.get_top_k_predictions(model, nl_str, k=10)

            top1_correct_temp, top3_correct_temp, top5_correct_temp, \
                top10_correct_temp = False, False, False, False
            top1_correct, top3_correct, top5_correct, top10_correct = \
                False, False, False, False

            # evaluation ignoring ordering of flags
            print("Example %d (%d)" % (num_evaled+1, len(cm_strs)))
            o_f.write("Example %d (%d)" % (num_evaled+1, len(cm_strs)) + "\n")
            print("English: " + nl_str.strip())
            o_f.write("English: " + nl_str.encode('utf-8'))
            for j in xrange(len(cm_strs)):
                print("GT Command %d: " % (j+1) + cm_strs[j].strip())
                o_f.write("GT Command %d: " % (j+1) + cm_strs[j].strip() + "\n")

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
                        str_judge = tree_dist.one_match(gt_trees, tree, rewrite=False,
                                                        ignore_arg_value=False)
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


def gen_eval_sheet(model, dataset, FLAGS, output_path):
    """
    :param model:
    :param dataset:
    :param FLAGS:
    :param output_path:

    :return:
    """
    with open(output_path, 'w') as o_f:
        # print evaluation form header
        o_f.write('example_id, description, ground_truth, prediction, ' +
                  'correct command, correct template\n')

        example_id = 0
        eval_bash = FLAGS.dataset.startswith("bash")
        cmd_parser = data_tools.bash_parser if eval_bash \
            else data_tools.paren_parser
        tokenizer_selector = "cm" if FLAGS.explain else "nl"
        grouped_dataset = data_utils.group_data(
            dataset, use_bucket=True, tokenizer_selector=tokenizer_selector)

        with DBConnection() as db:
            for nl_temp in grouped_dataset:
                data_group = grouped_dataset[nl_temp]
                nl_str = data_group[0].sc_txt

                cm_strs = [dp.tg_txt for dp in data_group]
                gt_trees = [cmd_parser(cm_str) for cm_str in cm_strs]
                if any(data_tools.is_low_frequency(t) for t in gt_trees):
                    continue
                gt_trees = gt_trees + [cmd_parser(cmd)
                                       for cmd in db.get_correct_temps(nl_str)]

                predictions = db.get_top_k_predictions(model, nl_str, k=10)

                example_id += 1

                for i in xrange(min(3, len(predictions))):
                    if i == 0:
                        output_str = '{},{},'.format(example_id, nl_temp.strip())
                    else:
                        output_str = ',,'
                    pred_cmd, score = predictions[i]
                    tree = cmd_parser(pred_cmd)

                    # evaluation ignoring flag orders
                    temp_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=False)
                    if i < len(cm_strs):
                        output_str += '{},'.format(cm_strs[i].strip())
                    else:
                        output_str += ','
                    output_str += '{},'.format(pred_cmd)
                    if temp_match:
                        output_str += 'y,'
                    if str_match:
                        output_str += 'y'

                    o_f.write(output_str + '\n')


def test_ted():
    while True:
        cmd1 = raw_input(">cmd1: ")
        cmd2 = raw_input(">cmd2: ")
        ast1 = data_tools.bash_parser(cmd1)
        ast2 = data_tools.bash_parser(cmd2)
        dist = zss.simple_distance(
            ast1, ast2, nast.Node.get_children, nast.Node.get_label,
            tree_dist.temp_local_dist
        )
        print("ted = {}".format(dist))
        print()


if __name__ == "__main__":
    test_ted()

