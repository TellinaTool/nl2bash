"""
Library for converting raw data into feature vectors.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from src import bashlint
from src.nlp_tools import constants


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
    def __init__(self, examples=None):
        self.examples = examples if examples else list()
        self.max_nl_seq_len = -1
        self.max_cm_seq_len = -1
        self.buckets = None

    def add_example(self, example):
        self.examples.append(example)

    @property
    def example_list(self):
        exp_list = []
        for example in self.examples:
            if isinstance(example, ExampleGroup):
                example_group = example
                for exp in example_group.examples:
                    exp_list.append(exp)
            else:
                exp_list.append(example)
        return exp_list


class ExampleGroup(object):
    def __init__(self, signature):
        self.examples = []
        self.group_signature = signature

    def add_example(self, example):
        self.examples.append(example)


class Example(object):
    def __init__(self, nl=None, cm=None):
        self.nl = nl
        self.cm = cm
        self.nl_tokens = None
        self.nl_tokens_orig = None
        self.cm_tokens = None
        self.nl_chars = None
        self.cm_chars = None
        self.nl_partial_tokens = None
        self.nl_partial_tokens_orig = None
        self.cm_partial_tokens = None
        self.nl_normalized_tokens = None
        self.cm_normalized_tokens = None

        self.nl_ids = None
        self.cm_ids = None
        self.copy_sc_ids = None         # CopyNet training source ids
        self.copy_tg_ids = None         # CopyNet training target ids
        self.alignments = None


class Vocab(object):
    def __init__(self):
        self.nl_vocab = None
        self.cm_vocab = None
        self.rev_nl_vocab = None
        self.rev_cm_vocab = None
        self.max_nl_token_size = -1
        self.max_cm_token_size = -1


def compute_copy_indices(sc_tokens, tg_tokens, sc_copy_tokens, tg_copy_tokens, tg_vocab, channel):
    assert (len(sc_tokens) == len(sc_copy_tokens))
    assert (len(tg_tokens) == len(tg_copy_tokens))
    copy_sc_ids, copy_tg_ids = [], []
    init_vocab = CHAR_INIT_VOCAB if channel == 'char' else TOKEN_INIT_VOCAB
    for i, sc_token in enumerate(sc_tokens):
        if sc_token not in init_vocab and sc_token in tg_vocab:
            copy_sc_ids.append(tg_vocab[sc_token])
        else:
            copy_sc_ids.append(len(tg_vocab) + sc_tokens.index(sc_token))
    for j, tg_token in enumerate(tg_tokens):
        tg_copy_token = tg_copy_tokens[j]
        if tg_token in tg_vocab:
            copy_tg_ids.append(tg_vocab[tg_token])
        else:
            if tg_copy_token in sc_copy_tokens:
                copy_tg_ids.append(
                    len(tg_vocab) + sc_copy_tokens.index(tg_copy_token))
            else:
                if channel == 'char':
                    copy_tg_ids.append(CUNK_ID)
                else:
                    copy_tg_ids.append(UNK_ID)
    # Append EOS symbol
    if channel == 'char':
        copy_tg_ids.append(CEOS_ID)
    else:
        copy_tg_ids.append(EOS_ID)
    return copy_sc_ids, copy_tg_ids
