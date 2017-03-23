from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from bashlex import data_tools

blacklist = [
    "xargs",
    "ls",
    "-ls",
    "-exec",
    "-print",
    "-print0"
]


def get_content_tokens(ast):
    content_tokens = set()
    for token in data_tools.ast2tokens(
            ast, loose_constraints=True, arg_type_only=True):
        if not token.isupper() and not token in blacklist:
            content_tokens.add(token)
    return content_tokens


def CMS(ast1, ast2):
    token_set1 = get_content_tokens(ast1)
    token_set2 = get_content_tokens(ast2)
    return float(len(token_set1) & len(token_set2)) /\
           (len(token_set1) + len(token_set2))


def command_match_score(ast, gts):
    avg_cms = 0.0
    for gt in gts:
        avg_cms += CMS(ast, gt)
    return avg_cms / len(gts)