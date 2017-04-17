from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bashlex import data_tools

whitelist = [
    '!',
    '&',
    '&&'
]


blacklist = [
    'ls',
    '-ls',
    '-a',
    '-and',
    '-exec',
    '-print',
    '-print0'
]


def get_content_tokens(ast):
    content_tokens = list()
    for token in data_tools.ast2tokens(
            ast, loose_constraints=True, arg_type_only=True):
        if ((token.isalnum() and token.islower()) or (token.startswith('-')
           or token.startswith('+') and len(token) > 1)) or token in whitelist\
           and not token in blacklist:
            content_tokens.append(token)
    return content_tokens


def CMS(ast1, ast2):
    token_list1 = get_content_tokens(ast1)
    token_list2 = get_content_tokens(ast2)
    num_overlap = 0.0
    for t in token_list2:
        if t in token_list1:
            num_overlap += 1
    return num_overlap / (len(token_list1) + len(token_list2) - num_overlap)


def command_match_score(gts, ast):
    max_cms = 0.0
    for gt in gts:
        if CMS(ast, gt) > max_cms:
            max_cms = CMS(ast, gt)
    return max_cms
