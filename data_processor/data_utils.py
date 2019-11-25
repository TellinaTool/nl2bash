"""
Library for converting raw data into feature vectors.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import bashlint
from nlp_tools import constants

# Special token symbols
_PAD = "__SP__PAD"
_EOS = "__SP__EOS"
_UNK = "__SP__UNK"
_ARG_UNK = "__SP__ARGUMENT_UNK"
_UTL_UNK = "__SP__UTILITY_UNK"
_FLAG_UNK = "__SP__FLAG_UNK"
_ARG_START = "__SP__ARG_START"
_ARG_END = "__SP__ARG_END"

_GO = "__SP__GO"                   # seq2seq start symbol
_ROOT = "__SP__ROOT"               # seq2tree start symbol

PAD_ID = 0
EOS_ID = 1
UNK_ID = 2
ARG_UNK_ID = 3
UTL_UNK_ID = 4
FLAG_UNK_ID = 5
H_NO_EXPAND_ID = 6
V_NO_EXPAND_ID = 7
GO_ID = 8
ROOT_ID = 9
ARG_START_ID = 10                  # start argument sketch
ARG_END_ID = 11                    # end argument sketch
NUM_ID = 12                        # 1, 2, 3, 4, ...
NUM_ALPHA_ID = 13                  # 10k, 20k, 50k, 100k, ...
NON_ENGLISH_ID = 14                # /local/bin, hello.txt, ...

TOKEN_INIT_VOCAB = [
    _PAD,
    _EOS,
    _UNK,
    _ARG_UNK,
    _UTL_UNK,
    _FLAG_UNK,
    bashlint._H_NO_EXPAND,
    bashlint._V_NO_EXPAND,
    _GO,
    _ROOT,
    _ARG_START,
    _ARG_END,
    constants._NUMBER,
    constants._NUMBER_ALPHA,
    constants._REGEX
]

# Special char symbols
_CPAD = "__SP__CPAD"
_CEOS = "__SP__CEOS"
_CUNK = "__SP__CUNK"
_CATOM = "__SP__CATOM"
_CGO = "__SP__CGO"

CPAD_ID = 0
CEOS_ID = 1
CUNK_ID = 2
CATOM_ID = 3
CLONG_ID = 4
CGO_ID = 5

CHAR_INIT_VOCAB = [
    _CPAD,
    _CEOS,
    _CUNK,
    _CATOM,
    constants._LONG_TOKEN_IND,
    _CGO
]

data_splits = ['train', 'dev', 'test']
TOKEN_SEPARATOR = '<TOKEN_SEPARATOR>'


class DataSet(object):
    def __init__(self, examples=list()):
        self.examples = examples
        self.max_sc_length = -1
        self.max_tg_length = -1
        self.buckets = None

    def add_example(self, example):
        self.examples.append(example)


class ExampleGroup(object):
    def __init__(self, signature):
        self.examples = []
        self.group_signature = signature

    def add_example(self, example):
        self.examples.append(example)


class Example(object):
    def __init__(self, source=None, target=None):
        self.source = source
        self.target = target
        self.sc_ids = None
        self.tg_ids = None
        self.csc_ids = None         # CopyNet training source ids
        self.ctg_ids = None         # CopyNet training target ids
        self.alignments = None
        self.sc_fillers = None      # TODO: this field is no longer used


class Vocab(object):
    def __init__(self):
        self.sc_vocab = None
        self.tg_vocab = None
        self.rev_sc_vocab = None
        self.rev_tg_vocab = None
        self.max_sc_token_size = -1
        self.max_tg_token_size = -1


def compute_copy_indices(sc_tokens, tg_tokens, sc_copy_tokens, tg_copy_tokens, tg_vocab, channel):
    assert (len(sc_tokens) == len(sc_copy_tokens))
    assert (len(tg_tokens) == len(tg_copy_tokens))
    csc_ids, ctg_ids = [], []
    init_vocab = CHAR_INIT_VOCAB if channel == 'char' else TOKEN_INIT_VOCAB
    for i, sc_token in enumerate(sc_tokens):
        if (not sc_token in init_vocab) and sc_token in tg_vocab:
            csc_ids.append(tg_vocab[sc_token])
        else:
            csc_ids.append(len(tg_vocab) + sc_tokens.index(sc_token))
    for j, tg_token in enumerate(tg_tokens):
        tg_copy_token = tg_copy_tokens[j]
        if tg_token in tg_vocab:
            ctg_ids.append(tg_vocab[tg_token])
        else:
            if tg_copy_token in sc_copy_tokens:
                ctg_ids.append(
                    len(tg_vocab) + sc_copy_tokens.index(tg_copy_token))
            else:
                if channel == 'char':
                    ctg_ids.append(CUNK_ID)
                else:
                    ctg_ids.append(UNK_ID)
    # Append EOS symbol
    if channel == 'char':
        ctg_ids.append(CEOS_ID)
    else:
        ctg_ids.append(EOS_ID)
    return csc_ids, ctg_ids


def load_pair_alignment(in_path):
    alignments = []
    with open(in_path) as f:
        for line in f:
            source_len, target_len, pairs = line.strip().split(':::')
            source_len, target_len = int(source_len), int(target_len)
            A = np.zeros([source_len, target_len], dtype=np.int32)
            alignments_ = [pair.split('-') for pair in pairs.split()]
            for pair in alignments_:
                A[int(pair[0]), int(pair[1])] = 1
            alignments.append(A)


def save_pair_alignment(alignments, out_path):
    with open(out_path, 'w') as o_f:
        for alignments_ in alignments:
            source, target = alignments_.nonzero()
            o_f.write('{}:::{}:::'.format(len(source), len(target)))
            for i in range(len(source)):
                o_f.write('{}-{} '.format(source[i], target[i]))
            o_f.write('\n')