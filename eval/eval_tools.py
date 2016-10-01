"""
The set of functions used at test time.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "eval"))

import data_utils, data_tools
import nast
import ast_based, zss
from eval_archive import DBConnection


def eval_set(model, dataset, rev_nl_vocab, verbose=True):
    num_top1_correct_temp = 0.0
    num_top5_correct_temp = 0.0
    num_top10_correct_temp = 0.0
    num_top1_correct = 0.0
    num_top5_correct = 0.0
    num_top10_correct = 0.0
    num_eval = 0

    use_bucket = False if model == "knn" else True
    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=use_bucket)

    with DBConnection() as db:
        for nl_temp in grouped_dataset:
            nl_strs, cm_strs, nls, search_historys = grouped_dataset[nl_temp]
            nl_str = nl_strs[0]
            nl = nls[0]

            gt_trees = [data_tools.bash_parser(cmd) for cmd in cm_strs]

            predictions = db.get_top_k_predictions(model, nl_str, k=10)

            if verbose:
                print("Example %d (%d)" % (num_eval, len(cm_strs)))
                print("Original English: " + nl_str.strip())
                print("English: " + nl_temp)
                for j in xrange(len(cm_strs)):
                    print("GT Command {}: ".format(j+1) + cm_strs[j].strip())
            num_eval += 1

            top1_correct_temp, top5_correct_temp, top10_correct_temp = False, False, False
            top1_correct, top5_correct, top10_correct = False, False, False
            for i in xrange(len(predictions)):
                pred_cmd, score = predictions[i]
                tree = data_tools.bash_parser(pred_cmd)
                # evaluation ignoring flag orders
                if ast_based.one_match(gt_trees, tree, ignore_arg_value=True):
                    if i < 1:
                        top1_correct_temp = True
                        top5_correct_temp = True
                        top10_correct_temp = True
                    elif i < 5:
                        top5_correct_temp = True
                        top10_correct_temp = True
                    elif i < 10:
                        top10_correct_temp = True
                if ast_based.one_match(gt_trees, tree, ignore_arg_value=False):
                    if i < 1:
                        top1_correct = True
                        top5_correct = True
                        top10_correct = True
                    elif i < 5:
                        top5_correct = True
                        top10_correct = True
                    elif i < 10:
                        top10_correct = True
                if verbose:
                    print("Prediction {}: {} ({})".format(i+1, pred_cmd, score))
                    # print("AST: ")
                    # data_tools.pretty_print(tree, 0)
            print()
            if top1_correct_temp:
                num_top1_correct_temp += 1
            if top5_correct_temp:
                num_top5_correct_temp += 1
            if top10_correct_temp:
                num_top10_correct_temp += 1
            if top1_correct:
                num_top1_correct += 1
            if top5_correct:
                num_top5_correct += 1
            if top10_correct:
                num_top10_correct += 1

    #TODO: compute top-K matching scores
    top1_temp_match_score = num_top1_correct_temp/num_eval
    top1_string_match_score = num_top1_correct/num_eval
    print("%d examples evaluated" % num_eval)
    print("Percentage of Template Match = %.2f" % top1_temp_match_score)
    print("Percentage of String Match = %.2f" % top1_string_match_score)
    if len(predictions) > 1:
        print("Top 5 Template Match Score = %.2f" % (num_top5_correct_temp/num_eval))
        print("Top 5 String Match Score = %.2f" % (num_top5_correct/num_eval))
        print("Top 10 Template Match Score = %.2f" % (num_top10_correct_temp/num_eval))
        print("Top 10 String Match Score = %.2f" % (num_top10_correct/num_eval))
    print()

    return top1_temp_match_score, top1_string_match_score


def manual_eval(model, dataset, rev_nl_vocab, output_dir, num_eval=30):
    num_top1_correct_temp = 0.0
    num_top5_correct_temp = 0.0
    num_top10_correct_temp = 0.0
    num_top1_correct = 0.0
    num_top5_correct = 0.0
    num_top10_correct = 0.0
    num_evaled = 0

    grouped_dataset = data_utils.group_data_by_nl(dataset, use_bucket=False) \
                                .values()
    random.shuffle(grouped_dataset, lambda: 0.5208484091114275)

    o_f = open(os.path.join(output_dir, "manual.eval.results"), 'w')

    with DBConnection() as db:
        db.create_schema()
        for i in xrange(len(grouped_dataset)):
            nl_strs, cm_strs, nls, search_historys = grouped_dataset[i]
            nl_str = nl_strs[0]
            nl = nls[0]

            if num_evaled == num_eval:
                break

            gt_trees = [data_tools.bash_parser(cmd) for cmd in cm_strs]

            predictions = db.get_top_k_predictions(model, nl_str, k=10)

            # evaluation ignoring ordering of flags
            print("Example %d (%d)" % (num_evaled+1, len(cm_strs)))
            o_f.write("Example %d (%d)" % (num_evaled+1, len(cm_strs)) + "\n")
            print("English: " + nl_str.strip())
            o_f.write("English: " + nl_str)
            for j in xrange(len(cm_strs)):
                print("GT Command %d: " % (j+1) + cm_strs[j].strip())
                o_f.write("GT Command %d: " % (j+1) + cm_strs[j].strip() + "\n")
            for i in xrange(len(predictions)):
                pred_cmd, score = predictions[i]
                tree = data_tools.bash_parser(pred_cmd)
                print("Prediction {}: {} ({})".format(i+1, pred_cmd, score))
                o_f.write("Prediction {}: {} ({})\n".format(i+1, pred_cmd, score))
                print("AST: ")
                data_tools.pretty_print(tree, 0)
                print()
                pred_temp = data_tools.ast2template(tree, loose_constraints=True)
                str_judge = db.get_str_judgement((nl_str, pred_cmd))
                temp_judge = db.get_temp_judgement((nl_str, pred_temp))
                if temp_judge is not None:
                    judgement_str = "y" if temp_judge else "n"
                    print("Correct template [y/n]: %s" % judgement_str)
                else:
                    temp_judge = ast_based.one_match(gt_trees, tree, rewrite=False,
                                                     ignore_arg_value=True)
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
                    if i < 1:
                        num_top1_correct_temp = True
                        num_top5_correct_temp = True
                        num_top10_correct_temp = True
                    elif i < 5:
                        num_top5_correct_temp = True
                        num_top10_correct_temp = True
                    elif i < 10:
                        num_top10_correct_temp = True
                    o_f.write("C")
                    if str_judge is not None:
                        judgement_str = "y" if str_judge else "n"
                        print("Correct command [y/n]: %s" % judgement_str)
                    else:
                        str_judge = ast_based.one_match(gt_trees, tree, rewrite=False,
                                                        ignore_arg_value=False)
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
                        if i < 1:
                            num_top1_correct = True
                            num_top5_correct = True
                            num_top10_correct = True
                        elif i < 5:
                            num_top5_correct = True
                            num_top10_correct = True
                        elif i < 10:
                            num_top10_correct = True
                        o_f.write("C")
                    else:
                        o_f.write("W")
                else:
                    o_f.write("WW")

                o_f.write("\n")
                o_f.write("\n")

            num_evaled = True

    print()
    print("%d examples evaluated" % num_eval)
    print("Top 1 Template Match Score = %.2f" % (num_top1_correct_temp/num_eval))
    print("Top 1 String Match Score = %.2f" % (num_top1_correct/num_eval))
    if len(predictions) > 1:
        print("Top 5 Template Match Score = %.2f" % (num_top5_correct_temp/num_eval))
        print("Top 5 String Match Score = %.2f" % (num_top5_correct/num_eval))
        print("Top 10 Template Match Score = %.2f" % (num_top10_correct_temp/num_eval))
        print("Top 10 String Match Score = %.2f" % (num_top10_correct/num_eval))
    print()

    o_f.write("\n")
    o_f.write("%d examples evaluated" % num_eval + "\n")
    o_f.write("Top 1 Template Match Score = %.2f" % (num_top1_correct_temp/num_eval) + "\n")
    o_f.write("Top 1 String Match Score = %.2f" % (num_top1_correct/num_eval) + "\n")
    if len(predictions) > 1:
        o_f.write("Top 5 Template Match Score = %.2f" % (num_top5_correct_temp/num_eval) + "\n")
        o_f.write("Top 5 String Match Score = %.2f" % (num_top5_correct/num_eval) + "\n")
        o_f.write("Top 10 Template Match Score = %.2f" % (num_top10_correct_temp/num_eval) + "\n")
        o_f.write("Top 10 String Match Score = %.2f" % (num_top10_correct/num_eval) + "\n")
    o_f.write("\n")

def test_ted():
    while True:
        cmd1 = raw_input(">cmd1: ")
        cmd2 = raw_input(">cmd2: ")
        ast1 = data_tools.bash_parser(cmd1)
        ast2 = data_tools.bash_parser(cmd2)
        dist = zss.simple_distance(
            ast1, ast2, nast.Node.get_children, nast.Node.get_label,
            ast_based.temp_local_dist
        )
        print("ted = {}".format(dist))
        print()

if __name__ == "__main__":
    test_ted()

