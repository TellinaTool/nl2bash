import os, sys
import re
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

def one_template_match(asts, ast2):
    temp2 = ignore_differences(
        data_tools.ast2template(ast2, loose_constraints=True))

    temps = [data_tools.ast2template(ast1, loose_constraints=True)
             for ast1 in asts]
    with DBConnection() as db:
        rewrite_temps = get_rewrite_templates(temps, db)

    for temp1 in rewrite_temps:
        temp1 = ignore_differences(temp1)
        if temp1 == temp2:
            return True
    return False

def one_string_match(asts, ast2):
    cmd2 = ignore_differences(data_tools.ast2template(
        ast2, loose_constraints=True, arg_type_only=False))

    with DBConnection() as db:
        rewrite_cmds = get_rewrites(asts, db)

    for cmd1 in rewrite_cmds:
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
