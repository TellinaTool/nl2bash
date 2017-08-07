"""
Functions for converting raw data into feature vectors.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import collections
import functools
import numpy as np
import random
import re
import os, sys

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import nast, data_tools
from nlp_tools import constants, ops, slot_filling, tokenizer

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
    nast._H_NO_EXPAND,
    nast._V_NO_EXPAND,
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


class DataSet(object):
    def __init__(self):
        self.data_points = []
        self.max_sc_length = -1
        self.max_tg_length = -1
        self.buckets = None


class DataPoint(object):
    def __init__(self):
        self.sc_txt = None
        self.tg_txt = None
        self.sc_ids = None
        self.tg_ids = None
        self.mappings = None        # CopyNet training
        self.sc_fillers = None      # TODO: this field is no longer used


class Vocab(object):
    def __init__(self):
        self.sc_vocab = None
        self.tg_vocab = None
        self.rev_sc_vocab = None
        self.rev_tg_vocab = None
        self.max_sc_token_size = -1
        self.max_tg_token_size = -1


# --- Data IO --- #

def load_data(FLAGS, use_buckets=True, load_mappings=False):
    print("Loading data from %s" % FLAGS.data_dir)

    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')

    train_set = read_data(FLAGS, 'train', source, target,
        use_buckets=use_buckets, add_start_token=True, add_end_token=True)
    dev_set = read_data(FLAGS, 'dev', source, target,
        use_buckets=use_buckets, buckets=train_set.buckets,
        add_start_token=True, add_end_token=True)
    test_set = read_data(FLAGS, 'test', source, target,
        use_buckets=use_buckets, buckets=train_set.buckets,
        add_start_token=True, add_end_token=True)

    return train_set, dev_set, test_set


def read_data(FLAGS, split, source, target, use_buckets=True, buckets=None,
              add_start_token=False, add_end_token=False):

    def get_data_file_path(data_dir, split, lang, extension):
        return os.path.join(data_dir, '{}.{}.{}'.format(split, lang, extension))

    def get_source_ids(s):
        return [int(x) for x in s.split()]

    def get_target_ids(s):
        tg_ids = [int(x) for x in s.split()]
        if add_start_token:
            tg_ids.insert(0, ROOT_ID)
        if add_end_token:
            tg_ids.append(EOS_ID)
        return tg_ids

    data_dir = FLAGS.data_dir
    sc_path = get_data_file_path(data_dir, split, source, 'filtered')
    tg_path = get_data_file_path(data_dir, split, target, 'filtered')
    id_ext = 'ids.char' if FLAGS.char else 'ids.token'
    sc_id_path = get_data_file_path(data_dir, split, source, id_ext)
    tg_id_path = get_data_file_path(data_dir, split, target, id_ext)
    print("source file: {}".format(sc_path))
    print("target file: {}".format(tg_path))
    print("source sequence indices file: {}".format(sc_id_path))
    print("target sequence indices file: {}".format(tg_id_path))

    dataset = []

    num_data = 0
    max_sc_length = 0
    max_tg_length = 0
    with open(sc_path) as sc_file:
        with open(tg_path) as tg_file:
            with open(sc_id_path) as sc_id_file:
                with open(tg_id_path) as tg_id_file:
                    for sc_txt in sc_file.readlines():
                        data_point = DataPoint()
                        data_point.sc_txt = sc_txt
                        data_point.tg_txt = tg_file.readline().strip()
                        data_point.sc_ids = \
                            get_source_ids(sc_id_file.readline().strip())
                        if len(data_point.sc_ids) > max_sc_length:
                            max_sc_length = len(data_point.sc_ids)
                        data_point.tg_ids = \
                            get_target_ids(tg_id_file.readline().strip())
                        if len(data_point.tg_ids) > max_tg_length:
                            max_tg_length = len(data_point.tg_ids)
                        dataset.append(data_point)
                        num_data += 1

    print('{} data points read.'.format(num_data))
    print('max_source_length = {}'.format(max_sc_length))
    print('max_target_length = {}'.format(max_tg_length))

    def print_bucket_size(bs):
        print('bucket size = ({}, {})'.format(bs[0], bs[1]))

    if use_buckets:
        print('Group data points into buckets...')
        # determine bucket sizes
        sorted_dataset = sorted(
            dataset, key=lambda x:(len(x.sc_ids) * 1e6 + len(x.tg_ids)))

        dataset = []
        if split == 'train':
            bucket_sizes = []
            if FLAGS.char:
                bucket_size = (100, 100)
                inc = 50
            else:
                bucket_size = (30, 30)
                inc = 10
            print_bucket_size(bucket_size)
            bucket = []
            for i in range(len(sorted_dataset)):
                data_point = sorted_dataset[i]
                if len(data_point.sc_ids) < bucket_size[0] \
                        and len(data_point.tg_ids) < bucket_size[1]:
                    bucket.append(data_point)
                else:
                    # determine if a new bucket is needed
                    if split == 'train' and i / num_data >= 0.98:
                        break
                    else:
                        dataset.append(bucket)
                        bucket_sizes.append(bucket_size)
                        bucket = []
                        bucket_size = (bucket_size[0]+inc, bucket_size[1]+inc)
                        print_bucket_size(bucket_size)
            if bucket:
                dataset.append(bucket)
                bucket_sizes.append(bucket_size)
        else:
            bucket_id = 0
            bucket_size = buckets[bucket_id]
            print_bucket_size(bucket_size)
            bucket = []
            for i in range(len(sorted_dataset)):
                data_point = sorted_dataset[i]
                if len(data_point.sc_ids) < bucket_size[0] \
                        and len(data_point.tg_ids) < bucket_size[1]:
                    bucket.append(data_point)
                else:
                    dataset.append(bucket)
                    # determine if a new bucket is available
                    if bucket_id < len(buckets) - 1:
                        bucket_id += 1
                        bucket_size = buckets[bucket_id]
                        print_bucket_size(bucket_size)
            if bucket:
                dataset.append(bucket)

    D = DataSet()
    D.data_points = dataset
    if split == 'train':
        D.max_sc_length = max_sc_length
        D.max_tg_length = max_tg_length
        if use_buckets:
            D.buckets = bucket_sizes

    return D


def load_vocabulary(FLAGS):
    data_dir = FLAGS.data_dir
    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')
    vocab_ext = 'vocab.char' if FLAGS.char else 'vocab.token'

    source_vocab_path = os.path.join(data_dir, '{}.{}'.format(source, vocab_ext))
    target_vocab_path = os.path.join(data_dir, '{}.{}'.format(target, vocab_ext))

    vocab = Vocab()
    vocab.sc_vocab, vocab.rev_sc_vocab = initialize_vocabulary(source_vocab_path)
    vocab.tg_vocab, vocab.rev_tg_vocab = initialize_vocabulary(target_vocab_path)

    max_sc_token_size = 0
    for v in vocab.sc_vocab:
        if len(v) > max_sc_token_size:
            max_sc_token_size = len(v)
    max_tg_token_size = 0
    for v in vocab.tg_vocab:
        if len(v) > max_tg_token_size:
            max_tg_token_size = len(v)
    vocab.max_sc_token_size = max_sc_token_size
    vocab.max_tg_token_size = max_tg_token_size

    print('source vocabulary size = {}'.format(len(vocab.sc_vocab)))
    print('target vocabulary size = {}'.foramt(len(vocab.tg_vocab)))
    print('max source token size = {}'.format(vocab.max_sc_token_size))
    print('max target token size = {}'.format(vocab.max_tg_token_size))

    return vocab


def initialize_vocabulary(vocab_path):
    """Initialize vocabulary from file.

    We assume the vocabulary is stored one-item-per-line, so a file:
      dog
      cat
    will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
    also return the reversed-vocabulary ["dog", "cat"].

    Args:
      vocab_path: path to the file containing the vocabulary.

    Returns:
      a pair: the vocabulary (a dictionary mapping string to integers), and
      the reversed vocabulary (a list, which reverses the vocabulary mapping).

    Raises:
      ValueError: if the provided vocab_path does not exist.
    """
    if tf.gfile.Exists(vocab_path):
        rev_vocab = []
        with tf.gfile.GFile(vocab_path, mode="r") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        rev_vocab = dict([(y, x) for (y, x) in enumerate(rev_vocab)])
        assert(len(vocab) == len(rev_vocab))
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocab_path)


# --- Data Preparation --- #

def prepare_data(FLAGS):
    """
    Read a specified dataset, tokenize data, create vocabularies and save
    feature files.

    Save to disk:
        (1) nl vocabulary
        (2) cm vocabulary
        (3) nl token ids
        (4) cm token ids
    """
    data_dir = FLAGS.data_dir
    prepare_dataset(data_dir, 'train')
    prepare_dataset(data_dir, 'dev')
    prepare_dataset(data_dir, 'test')


def prepare_dataset(data_dir, split):
    nl_path = os.path.join(data_dir, split + '.nl.filtered')
    cm_path = os.path.join(data_dir, split + '.cm.filtered')
    nl_list, cm_list = read_parallel_data(nl_path, cm_path)

    # character-based processing
    nl_chars, cm_chars = characterize_parallel_data(nl_list, cm_list)
    nl_char_vocab_path = os.path.join(data_dir, 'nl.vocab.char')
    cm_char_vocab_path = os.path.join(data_dir, 'cm.vocab.char')
    if split == 'train':
        nl_char_vocab = create_nl_vocabulary(nl_char_vocab_path, nl_chars)
        cm_char_vocab = create_cm_vocabulary(cm_char_vocab_path, cm_chars)
    else:
        nl_char_vocab, _ = initialize_vocabulary(nl_char_vocab_path)
        cm_char_vocab, _ = initialize_vocabulary(cm_char_vocab_path)
    with open(os.path.join(data_dir, split + '.nl.ids.char'), 'w') as nl_char_file:
        for data_point in nl_chars:
            nl_char_ids = string_to_char_ids(data_point, nl_char_vocab)
            nl_char_file.write('{}\n'.format(' '.join([str(x) for x in nl_char_ids])))
    with open(os.path.join(data_dir, split + '.cm.ids.char'), 'w') as cm_char_file:
        for data_point in cm_chars:
            cm_char_ids = string_to_char_ids(data_point, cm_char_vocab)
            cm_char_file.write('{}\n'.format(' '.join([str(x) for x in cm_char_ids])))

    # token-based processing
    nl_tokens, cm_tokens = tokenize_parallel_data(nl_list, cm_list)
    nl_vocab_path = os.path.join(data_dir, 'nl.vocab.token')
    cm_vocab_path = os.path.join(data_dir, 'cm.vocab.token')
    if split == 'train':
        nl_vocab = create_nl_vocabulary(
            nl_vocab_path, nl_tokens, min_word_frequency=2)
        cm_vocab = create_nl_vocabulary(
            cm_vocab_path, cm_tokens, min_word_frequency=1)
    else:
        nl_vocab, _ = initialize_vocabulary(nl_vocab_path)
        cm_vocab, _ = initialize_vocabulary(cm_vocab_path)
    with open(os.path.join(data_dir, split + '.nl.ids.token'), 'w') as nl_token_file:
        for data_point in nl_tokens:
            nl_token_ids = nl_to_token_ids(data_point, None, nl_vocab)
            nl_token_file.write('{}\n'.format(' '.join([str(x) for x in nl_token_ids])))
    with open(os.path.join(data_dir, split + '.cm.ids.token'), 'w') as cm_token_file:
        for data_point in cm_tokens:
            cm_token_ids = cm_to_token_ids(data_point, None, cm_vocab)
            cm_token_file.write('{}\n'.format(' '.join([str(x) for x in cm_token_ids])))


def read_parallel_data(nl_path, cm_path):
    with open(nl_path) as f:
        nl_list = [nl.strip() for nl in f.readlines()]
    with open(cm_path) as f:
        cm_list = [cm.strip() for cm in f.readlines()]
    return nl_list, cm_list


def characterize_parallel_data(nl_list, cm_list):
    nl_data = []
    for nl in nl_list:
        nl_data_point = []
        for c in nl:
            if c == ' ':
                nl_data_point.append(constants._SPACE)
            else:
                nl_data_point.append(c)
        nl_data.append(nl_data_point)
    cm_data = []
    for cm in cm_list:
        cm_data_point = []
        for c in cm:
            if c == ' ':
                cm_data_point.append(constants._SPACE)
            else:
                cm_data_point.append(c)
        cm_data.append(cm_data_point)
    return nl_data, cm_data


def tokenize_parallel_data(nl_list, cm_list):
    nl_data = [nl_to_tokens(nl, tokenizer.basic_tokenizer)
                         for nl in nl_list]
    cm_data = [cm_to_tokens(cm, data_tools.bash_tokenizer)
                         for cm in cm_list]
    return nl_data, cm_data


def string_to_char_ids(s, vocabulary):
    """
    Split a string into a sequence of characters and map the characters into
    their indices in the vocabulary.
    """
    char_ids = []
    for c in s:
        if c in vocabulary:
            char_ids.append(vocabulary[c])
        else:
            if c == ' ':
                char_ids.append(vocabulary[constants._SPACE])
            else:
                char_ids.append(CUNK_ID)
    return char_ids


def nl_to_tokens(s, tokenizer):
    """
    Split a natural language string into a sequence of tokens.
    """
    tokens, _ = tokenizer(s)
    return tokens


def nl_to_token_ids(s, tokenizer, vocabulary):
    """
    Split a natural language string into a sequence of tokens and map the
    tokens into their indices in the vocabulary.
    """
    tokens = nl_to_tokens(s, tokenizer) if not isinstance(s, list) else s
    token_ids = []
    for token in tokens:
        if token in vocabulary:
            token_ids.append(vocabulary[token])
        else:
            token_ids.append(UNK_ID)
    return token_ids


def cm_to_tokens(s, tokenizer, loose_constraints=True, with_suffix=True):
    """
    Split a command string into a sequence of tokens.
    """
    tokens = tokenizer(s, loose_constraints=loose_constraints, 
                       with_suffix=with_suffix)
    return tokens


def cm_to_token_ids(s, tokenizer, vocabulary):
    """
    Split a command string into a sequence of tokens and map the tokens into
    their indices in the vocabulary.
    """
    tokens = cm_to_tokens(s, tokenizer) if not isinstance(s, list) else s
    token_ids = []
    for token in tokens:
        if token in vocabulary:
            token_ids.append(vocabulary[token])
        else:
            token_ids.append(UNK_ID)
    return token_ids


def create_nl_vocabulary(vocab_path, dataset, min_word_frequency=1,
                         tokenizer=None, is_character_model=False):
    """
    Compute the natural language vocabulary and save to file.
    """
    vocab = collections.defaultdict(int)
    for data_point in dataset:
        tokens = nl_to_tokens(data_point, tokenizer) \
            if not isinstance(data_point, list) else data_point
        for token in tokens:
            vocab[token] += 1
    sorted_vocab = [x for x, y in sorted(vocab.items(), key=lambda x:x[1],
                        reverse=True) if y >= min_word_frequency]
    
    if is_character_model:
        # Character model
        init_vocab = CHAR_INIT_VOCAB
    else:
        init_vocab = TOKEN_INIT_VOCAB
    vocab = list(init_vocab)
    for v in sorted_vocab:
        if not v in init_vocab:
            vocab.append(v)

    with open(vocab_path, 'w') as vocab_file:
        for v in vocab:
            vocab_file.write('{}\n'.format(v))

    return dict([(x, y) for y, x in enumerate(vocab)])


def create_cm_vocabulary(vocab_path, dataset, min_word_frequency=1,
                         tokenizer=None, is_character_model=False):
    """
    Compute the natural language vocabulary and save to file.
    """
    vocab = collections.defaultdict(int)
    for data_point in dataset:
        tokens = cm_to_tokens(data_point, tokenizer) \
            if not isinstance(data_point, list) else data_point
        for token in tokens:
            vocab[token] += 1
    sorted_vocab = [x for x, y in sorted(vocab.items(), key=lambda x:x[1],
                        reverse=True) if y >= min_word_frequency]
            
    if is_character_model:
        # Character model
        init_vocab = CHAR_INIT_VOCAB
    else:
        init_vocab = TOKEN_INIT_VOCAB
    vocab = list(init_vocab)
    for v in sorted_vocab:
        if not v in init_vocab:
            vocab.append(v)

    with open(vocab_path, 'w') as vocab_file:
        for v in vocab:
            vocab_file.write('{}\n'.format(v))

    return dict([(x, y) for y, x in enumerate(vocab)])


def group_parallel_data(dataset, attribute='source', use_bucket=False,
                        use_temp=False, tokenizer_selector='nl'):
    """
    Group parallel dataset by a certain attribute.

    :param dataset: a list of training quadruples (nl_str, cm_str, nl, cm)
    :param attribute: attribute by which the data is grouped
    :param bucket_input: if the input is grouped in buckets
    :param use_temp: set to true if the dataset is to be grouped by the natural
        language template; false if the dataset is to be grouped by the natural
        language strings
    :param tokenizer_selector: specify which tokenizer to use for making
        templates

    :return: list of (key, data group) tuples sorted by the key value.
    """
    if use_bucket:
        dataset = functools.reduce(lambda x, y: x + y, dataset)

    grouped_dataset = {}
    for i in xrange(len(dataset)):
        attr = dataset[i].sc_txt \
            if attribute == 'source' else dataset[i].tg_txt
        if use_temp:
            if tokenizer_selector == 'nl':
                words, _ = tokenizer.ner_tokenizer(attr)
            else:
                words = data_tools.bash_tokenizer(attr, arg_type_only=True)
            temp = ' '.join(words)
        else:
            temp = attr
        if temp in grouped_dataset:
            grouped_dataset[temp].append(dataset[i])
        else:
            grouped_dataset[temp] = [dataset[i]]

    return sorted(grouped_dataset.items(), key=lambda x: x[0])