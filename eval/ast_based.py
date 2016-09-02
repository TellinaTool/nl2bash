import sys
sys.path.append("../bashlex")

import data_tools

def one_template_match(asts, ast2):
    temp2 = data_tools.ast2template(ast2, loose_constraints=True)
    for ast1 in asts:
        temp1 = data_tools.ast2template(ast1, loose_constraints=True)
        if temp1 == temp2:
            return True
    return False

def one_string_match(asts, ast2):
    str2 = data_tools.ast2template(ast2, loose_constraints=True, arg_type_only=False)
    for ast1 in asts:
        str1 = data_tools.ast2template(ast1, loose_constraints=True, arg_type_only=False)
        if str1 == str2:
            return True
    return False

def template_match(ast1, ast2):
    temp1 = data_tools.ast2template(ast1, loose_constraints=True)
    temp2 = data_tools.ast2template(ast2, loose_constraints=True)
    return temp1 == temp2

def string_match(ast1, ast2):
    str1 = data_tools.ast2template(ast1, loose_constraints=True, arg_type_only=False)
    str2 = data_tools.ast2template(ast2, loose_constraints=True, arg_type_only=False)
    return str1 == str2
