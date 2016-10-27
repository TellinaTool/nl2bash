import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))

import data_tools, nast
import zss
import extract_rewrites as er
import eval_archive as ea

def ignore_differences(cmd):
    cmd = cmd.replace('-ls', '')
    cmd = cmd.replace('-print', '')
    cmd = cmd.replace('-print0', '')
    cmd = cmd.replace('-name', '-iname')
    cmd = cmd.replace('-regex', '-iregex')
    return cmd

def local_dist(s1, s2, skip_argument=False):
    score_list = {
        "FLAG_-ls:::":0,
        ":::FLAG_-ls":0,
        "FLAG_-print:::":0,
        ":::FLAG_-print":0,
        "FLAG_-print0:::":0,
        ":::FLAG_-print0":0,
        "FLAG_-name:::FLAG_-iname":0,
        "FLAG_-iname:::FLAG_-name":0,
        "FLAG_-regex:::FLAG_-iregex":0,
        "FLAG_-iregex:::FLAG_-regex":0,
        "FLAG_-name:::FLAG_-regex":0,
        "FLAG_-regex:::FLAG_-name":0,
        "FLAG_-name:::FLAG_-iregex":0,
        "FLAG_-iregex:::FLAG_-name":0,
        "FLAG_-iname:::FLAG_-regex":0,
        "FLAG_-regex:::FLAG_-iname":0,
        "FLAG_-iname:::FLAG_-iregex":0,
        "FLAG_-iregex:::FLAG_-iname":0
    }

    pair_key = ":::".join((s1, s2))
    if pair_key in score_list:
        return score_list[pair_key]
    else:
        if s1 == s2:
            return 0
        else:
            if s1.startswith("ARGUMENT_") and s2.startswith("ARGUMENT_") \
                    and skip_argument:
                return 0
            else:
                return 1

def str_local_dist(s1, s2):
    return local_dist(s1, s2)

def temp_local_dist(s1, s2):
    return local_dist(s1, s2, skip_argument=True)

def str_dist(ast1, ast2):
    return zss.simple_distance(ast1, ast2, nast.Node.get_children,
                               nast.Node.get_label, str_local_dist)

def temp_dist(ast1, ast2):
    return zss.simple_distance(ast1, ast2, nast.Node.get_children,
                               nast.Node.get_label, temp_local_dist)

def get_rewrite_templates(temps, db):
    rewrites = set()
    for temp in temps:
        rewrites |= db.get_rewrite_templates(temp)
    return rewrites

def get_rewrites(asts, db):
    rewrites = set()
    for ast in asts:
        if ast is not None:
            rewrites |= db.get_rewrites(ast)
    return rewrites

def min_dist(asts, ast2, rewrite=True, ignore_arg_value=False):
    """
    Compute the minimum tree edit distance of the prediction to the set of ground truth ASTs.
    :param asts: set of gold ASTs.
    :param ast2: predicted AST.
    :param rewrite: set to true if rewrite ground truths with templates.
    :param ignore_arg_value: set to true if ignore literal values in the ASTs.
    :return:
    """
    # tolerate ungrammatical predictions
    if not ast2:
        ast2 = data_tools.bash_parser("find")

    if rewrite:
        with er.DBConnection() as db:
            ast_rewrites = get_rewrites(asts, db)
    else:
        ast_rewrites = asts

    with ea.DBConnection() as db:
        min_dist = sys.maxint
        cmd2 = data_tools.ast2template(ast2, loose_constraints=True)
        for ast1 in ast_rewrites:
            cmd1 = data_tools.ast2template(ast1)
            # t_dist = db.get_temp_dist(cmd1, cmd2)
            # s_dist = db.get_str_dist(cmd1, cmd2)
            if ignore_arg_value:
                dist = temp_dist(ast1, ast2)
            else:
                dist = str_dist(ast1, ast2)
            if dist < min_dist:
                min_dist = dist

    return min_dist

def one_match(asts, ast2, rewrite=True, ignore_arg_value=False):
    if rewrite:
        with er.DBConnection() as db:
            ast_rewrites = get_rewrites(asts, db)
    else:
        ast_rewrites = asts

    cmd2 = ignore_differences(data_tools.ast2template(
        ast2, loose_constraints=True, arg_type_only=ignore_arg_value))
    for ast1 in ast_rewrites:
        cmd1 = data_tools.ast2template(
            ast1, loose_constraints=True, arg_type_only=ignore_arg_value)
        cmd1 = ignore_differences(cmd1)
        if cmd1 == cmd2:
            return True
    return False

def template_match(ast1, ast2):
    temp1 = ignore_differences(
        data_tools.ast2template(ast1, loose_constraints=True))
    temp2 = ignore_differences(
        data_tools.ast2template(ast2, loose_constraints=True))
    return temp1 == temp2

def string_match(ast1, ast2):
    str1 = ignore_differences(
        data_tools.ast2template(ast1, loose_constraints=True, arg_type_only=False))
    str2 = ignore_differences(
        data_tools.ast2template(ast2, loose_constraints=True, arg_type_only=False))
    return str1 == str2
