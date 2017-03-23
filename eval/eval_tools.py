"""
The set of functions used at test time.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

import os, sys

from encoder_decoder import data_utils
from bashlex import data_tools, nast
from eval import tree_dist, zss
from eval.eval_archive import DBConnection

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

def eval_set(model, dataset, FLAGS, verbose=True):
    num_top1_correct_temp = 0.0
    num_top3_correct_temp = 0.0
    num_top5_correct_temp = 0.0
    num_top10_correct_temp = 0.0
    total_top1_temp_dist = 0.0
    total_top3_temp_dist = 0.0
    total_top5_temp_dist = 0.0
    total_top10_temp_dist = 0.0
    num_top1_correct = 0.0
    num_top3_correct = 0.0
    num_top5_correct = 0.0
    num_top10_correct = 0.0
    total_top1_dist = 0.0
    total_top3_dist = 0.0
    total_top5_dist = 0.0
    total_top10_dist = 0.0

    num_eval = 0
    eval_bash = FLAGS.dataset.startswith("bash")
    cmd_parser = data_tools.bash_parser if eval_bash \
        else data_tools.paren_parser

    use_bucket = False if model == "knn" else True

    grouped_dataset = data_utils.group_data_by_nl(
        dataset, use_bucket=use_bucket, use_temp = eval_bash)

    with DBConnection() as db:
        for nl_temp in grouped_dataset:
            nl_strs, cm_strs, nls, search_historys = grouped_dataset[nl_temp]
            nl_str = nl_strs[0].decode('utf-8')

            gt_trees = [cmd_parser(cmd) for cmd in cm_strs]
            num_gts = len(gt_trees)
            gt_trees = gt_trees + [cmd_parser(cmd) for cmd in db.get_correct_temps(nl_str)]

            predictions = db.get_top_k_predictions(model, nl_str, k=10)

            if verbose:
                print("Example %d (%d)" % (num_eval, len(cm_strs)))
                print("Original English: " + nl_str.strip())
                print("English: " + nl_temp)
                for j in xrange(len(cm_strs)):
                    print("GT Command {}: ".format(j+1) + cm_strs[j].strip())
            num_eval += (1 if eval_bash else num_gts)

            top1_correct_temp, top3_correct_temp, top5_correct_temp, top10_correct_temp = \
                False, False, False, False
            top1_correct, top3_correct, top5_correct, top10_correct = \
                False, False, False, False

            top1_temp_dist = sys.maxint
            top3_temp_dist = sys.maxint
            top5_temp_dist = sys.maxint
            top10_temp_dist = sys.maxint
            top1_dist = sys.maxint
            top3_dist = sys.maxint
            top5_dist = sys.maxint
            top10_dist = sys.maxint

            for i in xrange(min(1, len(predictions))):
                pred_cmd, score = predictions[i]
                tree = cmd_parser(pred_cmd)
                # evaluation ignoring flag orders
                temp_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=True)
                str_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=False)
                min_temp_dist = tree_dist.min_dist(gt_trees, tree, ignore_arg_value=True)
                min_dist = tree_dist.min_dist(gt_trees, tree, ignore_arg_value=False)

                if temp_match:
                    if i < 1:
                        top1_correct_temp = True
                    if i < 3:
                        top3_correct_temp = True
                    if i < 5:
                        top5_correct_temp = True
                    if i < 10:
                        top10_correct_temp = True
                if str_match:
                    if i < 1:
                        top1_correct = True
                    if i < 3:
                        top3_correct = True
                    if i < 5:
                        top5_correct = True
                    if i < 10:
                        top10_correct = True
                if i < 1:
                    if min_temp_dist < top1_temp_dist:
                        top1_temp_dist = min_temp_dist
                    if min_dist < top1_dist:
                        top1_dist = min_dist
                if i < 3:
                    if min_temp_dist < top3_temp_dist:
                        top3_temp_dist = min_temp_dist
                    if min_dist < top3_dist:
                        top3_dist = min_dist
                if i < 5:
                    if min_temp_dist < top5_temp_dist:
                        top5_temp_dist = min_temp_dist
                    if min_dist < top5_dist:
                        top5_dist = min_dist
                if i < 10:
                    if min_temp_dist < top10_temp_dist:
                        top10_temp_dist = min_temp_dist
                    if min_dist < top10_dist:
                        top10_dist = min_dist
                if verbose:
                    print("Prediction {}: {} ({}) ({})".format(i+1, pred_cmd, score, temp_match))
            if verbose:
                print()
            if top1_correct_temp:
                num_top1_correct_temp += (1 if eval_bash else num_gts)
            if top3_correct_temp:
                num_top3_correct_temp += (1 if eval_bash else num_gts)
            if top5_correct_temp:
                num_top5_correct_temp += (1 if eval_bash else num_gts)
            if top10_correct_temp:
                num_top10_correct_temp += (1 if eval_bash else num_gts)
            if top1_correct:
                num_top1_correct += (1 if eval_bash else num_gts)
            if top3_correct:
                num_top3_correct += (1 if eval_bash else num_gts)
            if top5_correct:
                num_top5_correct += (1 if eval_bash else num_gts)
            if top10_correct:
                num_top10_correct += (1 if eval_bash else num_gts)

            total_top1_temp_dist += top1_temp_dist
            total_top3_temp_dist += top3_temp_dist
            total_top5_temp_dist += top5_temp_dist
            total_top10_temp_dist += top10_temp_dist
            total_top1_dist += top1_dist
            total_top3_dist += top3_dist
            total_top5_dist += top5_dist
            total_top10_dist += top10_dist

    #TODO: compute top-K matching scores
    top1_temp_match_score = num_top1_correct_temp / num_eval
    top1_string_match_score = num_top1_correct / num_eval
    avg_top1_temp_dist = (total_top1_temp_dist + 0.0) / num_eval
    avg_top1_dist = (total_top1_dist + 0.0) / num_eval
    print("%d examples evaluated" % num_eval)
    print("Percentage of top 1 Match (template-only) = %.3f" % top1_temp_match_score)
    print("Percentage of top 1 Match (whole-string) = %.3f" % top1_string_match_score)
    print("Average top 1 Tree Edit Distance (template-only) = %.2f" % avg_top1_temp_dist)
    print("Average top 1 Tree Edit Distance (whole-string) = %.2f" % avg_top1_dist)
    if len(predictions) > 1:
        print("Top 3 Template Match Score = %.3f" % (num_top3_correct_temp/num_eval))
        print("Top 3 String Match Score = %.3f" % (num_top3_correct/num_eval))
        avg_top3_temp_dist = (total_top3_temp_dist + 0.0) / num_eval
        avg_top3_dist = (total_top3_dist + 0.0) / num_eval
        print("Average top 3 Tree Edit Distance (template-only) = %.2f" % avg_top3_temp_dist)
        print("Average top 3 Tree Edit Distance (whole-string) = %.2f" % avg_top3_dist)
    if len(predictions) > 3:
        print("Top 5 Template Match Score = %.3f" % (num_top5_correct_temp/num_eval))
        print("Top 5 String Match Score = %.3f" % (num_top5_correct/num_eval))
        avg_top5_temp_dist = (total_top5_temp_dist + 0.0) / num_eval
        avg_top5_dist = (total_top5_dist + 0.0) / num_eval
        print("Average top 5 Tree Edit Distance (template-only) = %.2f" % avg_top5_temp_dist)
        print("Average top 5 Tree Edit Distance (whole-string) = %.2f" % avg_top5_dist)
    if len(predictions) > 5:
        print("Top 10 Template Match Score = %.3f" % (num_top10_correct_temp/num_eval))
        print("Top 10 String Match Score = %.3f" % (num_top10_correct/num_eval))
        avg_top10_temp_dist = (total_top10_temp_dist + 0.0) / num_eval
        avg_top10_dist = (total_top10_dist + 0.0) / num_eval
        print("Average top 10 Tree Edit Distance (template-only) = %.2f" % avg_top10_temp_dist)
        print("Average top 10 Tree Edit Distance (whole-string) = %.2f" % avg_top10_dist)
    print()

    return top1_temp_match_score, top1_string_match_score, avg_top1_temp_dist, avg_top1_dist


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

    grouped_dataset = data_utils.group_data_by_nl(
        dataset, use_bucket=False).values()
    random.shuffle(grouped_dataset, lambda: 0.5208484091114275)

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

            top1_correct_temp, top3_correct_temp, top5_correct_temp, top10_correct_temp = \
                False, False, False, False
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
        grouped_dataset = data_utils.group_data_by_nl(dataset, use_temp=False)

        with DBConnection() as db:
            for nl_temp in grouped_dataset:
                nl_strs, cm_strs, nls, search_historys = grouped_dataset[nl_temp]
                nl_str = nl_strs[0].decode('utf-8')

                gt_trees = [cmd_parser(cmd) for cmd in cm_strs]
                gt_trees = gt_trees + [cmd_parser(cmd) for cmd in db.get_correct_temps(nl_str)]

                predictions = db.get_top_k_predictions(model, nl_str, k=10)

                example_id += 1
                output_str = '{},{},'.format(example_id, nl_temp)

                for i in xrange(min(1, len(predictions))):
                    pred_cmd, score = predictions[i]
                    tree = cmd_parser(pred_cmd)
                    # evaluation ignoring flag orders
                    temp_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(gt_trees, tree, ignore_arg_value=False)
                    if i < len(cm_strs):
                        output_str += '{},'.format(cm_strs[i])
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

