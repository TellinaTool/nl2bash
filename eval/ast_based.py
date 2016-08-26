import sys
sys.path.append("../bashlex")

import normalizer

def template_match(ast1, ast2):
    temp1 = normalizer.to_template(ast1, loose_constraints=False)
    temp2 = normalizer.to_template(ast2, loose_constraints=True)
    return temp1 == temp2

def string_match(ast1, ast2):
    str1 = normalizer.to_template(ast1, loose_constraints=False, arc_type_only=False)
    str2 = normalizer.to_template(ast2, loose_constraints=True, arc_type_only=False)
    return str1 == str2