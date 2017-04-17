from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import numpy as np

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
    content_tokens = collections.defaultdict(int)
    for token in data_tools.ast2tokens(
            ast, loose_constraints=True, arg_type_only=True):
        if ((token.isalnum() and token.islower()) or (token.startswith('-')
           or token.startswith('+') and len(token) > 1)) or token in whitelist\
           and not token in blacklist:
            content_tokens[token] += 1
    return content_tokens


def CMS(ast1, ast2):
    token_dict1 = get_content_tokens(ast1)
    token_dict2 = get_content_tokens(ast2)
    num_overlap = 0.0
    for t in token_dict2:
        if t in token_dict1:
            num_overlap += token_dict1[t] * token_dict2[t]
    norm1 = 0.0
    for t in token_dict1:
        norm1 += token_dict1[t] * token_dict1[t]
    norm2 = 0.0
    for t in token_dict2:
        norm2 += token_dict2[t] * token_dict2[t]

    return num_overlap / np.sqrt(norm1) / np.sqrt(norm2)


def command_match_score(gts, ast):
    max_cms = 0.0
    for gt in gts:
        if CMS(ast, gt) > max_cms:
            max_cms = CMS(ast, gt)
    return max_cms
