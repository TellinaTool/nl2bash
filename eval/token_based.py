"""
Compute keyword overlap between two commands.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import nltk
import numpy as np

from bashlint import data_tools, nast


smoothing = nltk.translate.bleu_score.SmoothingFunction()


def get_content_tokens(ast):
    content_tokens = collections.defaultdict(int)
    for compound_token in data_tools.ast2tokens(ast, loose_constraints=True,
            arg_type_only=True, with_prefix=True, with_flag_argtype=True):
        kind_token = compound_token.split(nast.KIND_PREFIX)
        if len(kind_token) == 2:
            kind, token = kind_token
        else:
            kind = ''
            token = kind_token[0]
        if kind.lower() != 'argument':
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
    if norm1 == 0 or norm2 == 0:
        return 0
    else:
        return num_overlap / np.sqrt(norm1) / np.sqrt(norm2)


def command_match_score(gts, ast):
    max_cms = 0.0
    for gt in gts:
        if CMS(ast, gt) > max_cms:
            max_cms = CMS(ast, gt)
    return max_cms


def sentence_bleu_score(gt_asts, pred_ast):
    gt_tokens = [data_tools.bash_tokenizer(ast, ignore_flag_order=True) for ast in gt_asts]
    pred_tokens = data_tools.bash_tokenizer(pred_ast, loose_constraints=True, ignore_flag_order=True)
    bleu = nltk.translate.bleu_score.sentence_bleu(gt_tokens, pred_tokens,
                                                   smoothing_function=smoothing.method1, auto_reweigh=True) 
    return bleu 


def corpus_bleu_score(gt_asts_list, pred_ast_list):
    gt_tokens_list = [[data_tools.bash_tokenizer(ast, ignore_flag_order=True) for ast in gt_asts] for gt_asts in gt_asts_list]
    pred_tokens_list = [data_tools.bash_tokenizer(pred_ast, loose_constraints=True, ignore_flag_order=True) for pred_ast in pred_ast_list]
    # print(gt_tokens, pred_tokens)
    bleu = nltk.translate.bleu_score.corpus_bleu(gt_tokens_list, pred_tokens_list, 
                                                 smoothing_function=smoothing.method1, auto_reweigh=True)
    return bleu
