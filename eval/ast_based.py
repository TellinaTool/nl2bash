import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bashlex"))

import data_tools
from extract_rewrites import DBConnection

def ignore_differences(cmd):
    cmd = cmd.replace('-ls', '')
    cmd = cmd.replace('-print', '')
    cmd = cmd.replace('-print0', '')
    cmd = cmd.replace('-name', '-iname')
    cmd = cmd.replace('-regex', '-iregex')
    return cmd

def label_distance(s1, s2):
    score_list = {
        "-ls:::":0,
        ":::-ls":0,
        "-print:::":0,
        ":::-print":0,
        "-print0:::":0,
        ":::-print0":0,
        "-name:::-iname":0,
        "-iname:::-name":0,
        "-regex:::-iregex":0,
        "-iregex:::-regex":0
    }

    pair_key = ":::".join((s1, s2))
    if pair_key in score_list:
        return score_list[pair_key]
    else:
        return 1

def get_rewrite_templates(temps, db):
    rewrites = set()
    for temp in temps:
        rewrites |= db.get_rewrite_templates(temp)
    return rewrites

def get_rewrites(asts, db):
    rewrites = set()
    for ast in asts:
        rewrites |= db.get_rewrites(ast)
    return rewrites

def one_template_match(asts, ast2, rewrite=True):
    temp2 = ignore_differences(
        data_tools.ast2template(ast2, loose_constraints=True))

    temps = [data_tools.ast2template(ast1, loose_constraints=True)
             for ast1 in asts]
    if rewrite:
        with DBConnection() as db:
            rewrite_temps = get_rewrite_templates(temps, db)
    else:
        rewrite_temps = temps

    for temp1 in rewrite_temps:
        temp1 = ignore_differences(temp1)
        if temp1 == temp2:
            return True
    return False

def one_string_match(asts, ast2, rewrite=True):
    cmd2 = ignore_differences(data_tools.ast2template(
        ast2, loose_constraints=True, arg_type_only=False))

    if rewrite:
        with DBConnection() as db:
            rewrites = get_rewrites(asts, db)
    else:
        rewrites = asts

    for ast1 in rewrites:
        cmd1 = data_tools.ast2template(
            ast1, loose_constraints=True, arg_type_only=False)
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
