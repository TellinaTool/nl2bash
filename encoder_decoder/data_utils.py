"""
Library for converting raw data into feature vectors.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import os
import pickle
import sys

import numpy as np
import scipy.sparse as ssp
import tensorflow as tf

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlint import bash, nast, data_tools
from nlp_tools import constants, tokenizer

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
TOKEN_SEPARATOR = '<TOKEN_SEPARATOR>'


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


# --- Data IO --- #

def load_data(FLAGS, use_buckets=True, load_features=True):
    print("Loading data from %s" % FLAGS.data_dir)

    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')

    train_set = read_data(FLAGS, 'train', source, target, load_features=load_features,
                          use_buckets=use_buckets, add_start_token=True, add_end_token=True)
    dev_set = read_data(FLAGS, 'dev', source, target, load_features=load_features,
                        use_buckets=use_buckets, buckets=train_set.buckets,
                        add_start_token=True, add_end_token=True)
    test_set = read_data(FLAGS, 'test', source, target, load_features=load_features,
                         use_buckets=use_buckets, buckets=train_set.buckets,
                         add_start_token=True, add_end_token=True)

    return train_set, dev_set, test_set


def read_data(FLAGS, split, source, target, use_buckets=True, buckets=None,
              add_start_token=False, add_end_token=False, load_features=True):

    def get_data_file_path(data_dir, split, lang, channel):
        return os.path.join(data_dir, '{}.{}.{}'.format(split, lang, channel))

    def get_source_ids(s):
        source_ids = []
        for token in s.split(TOKEN_SEPARATOR):
            if token in vocab.sc_vocab:
                source_ids.append(vocab.sc_vocab[token])
            else:
                source_ids.append(UNK_ID)
        return source_ids

    def get_target_input_ids(s):
        target_ids = []
        for token in s.split(TOKEN_SEPARATOR):
            if token in vocab.tg_vocab:
                target_ids.append(vocab.tg_vocab[token])
            else:
                target_ids.append(UNK_ID)
        if add_start_token:
            target_ids.insert(0, ROOT_ID)
        if add_end_token:
            target_ids.append(EOS_ID)
        return target_ids

    if load_features:
        vocab = load_vocabulary(FLAGS)

    data_dir = FLAGS.data_dir
    sc_path = get_data_file_path(data_dir, split, source, 'filtered')
    tg_path = get_data_file_path(data_dir, split, target, 'filtered')
    print("source file: {}".format(sc_path))
    print("target file: {}".format(tg_path))
    sc_file = open(sc_path, encoding='utf-8')
    tg_file = open(tg_path, encoding='utf-8')

    if load_features:
        token_ext = 'normalized.{}'.format(FLAGS.channel) \
            if FLAGS.normalized else FLAGS.channel
        sc_token_path = get_data_file_path(data_dir, split, source, token_ext)
        tg_token_path = get_data_file_path(data_dir, split, target, token_ext)
        print("source tokenized sequence file: {}".format(sc_token_path))
        print("target tokenized sequence file: {}".format(tg_token_path))
        sc_token_file = open(sc_token_path, encoding='utf-8')
        tg_token_file = open(tg_token_path, encoding='utf-8')
        with open(os.path.join(data_dir, '{}.{}.align'.format(split, FLAGS.channel)), 'rb') as f:
            alignments = pickle.load(f)

    dataset = []
    num_data = 0
    max_sc_length = 0
    max_tg_length = 0

    for i, sc_txt in enumerate(sc_file.readlines()):
        data_point = DataPoint()
        data_point.sc_txt = sc_txt.strip()
        data_point.tg_txt = tg_file.readline().strip()
        if load_features:
            data_point.sc_ids = \
                get_source_ids(sc_token_file.readline().strip())
            if len(data_point.sc_ids) > max_sc_length:
                max_sc_length = len(data_point.sc_ids)
            data_point.tg_ids = \
                get_target_input_ids(tg_token_file.readline().strip())
            data_point.alignments = alignments[i]
            if len(data_point.tg_ids) > max_tg_length:
                max_tg_length = len(data_point.tg_ids)
        dataset.append(data_point)
        num_data += 1
    data_size = len(dataset)
    sc_file.close()
    tg_file.close()
    if load_features:
        sc_token_file.close()
        tg_token_file.close()

    print('{} data points read.'.format(num_data))
    if load_features:
        print('max_source_length = {}'.format(max_sc_length))
        print('max_target_length = {}'.format(max_tg_length))

        if FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
            copy_token_ext = 'copy.{}'.format(token_ext)
            sc_copy_token_path = get_data_file_path(data_dir, split, source,
                                                    copy_token_ext)
            tg_copy_token_path = get_data_file_path(data_dir, split, target,
                                                    copy_token_ext)
            sc_token_file = open(sc_token_path, encoding='utf-8')
            tg_token_file = open(tg_token_path, encoding='utf-8')
            sc_copy_token_file = open(sc_copy_token_path, encoding='utf-8')
            tg_copy_token_file = open(tg_copy_token_path, encoding='utf-8')
            for i, data_point in enumerate(dataset):
                sc_tokens = sc_token_file.readline().strip().split(TOKEN_SEPARATOR)
                tg_tokens = tg_token_file.readline().strip().split(TOKEN_SEPARATOR)
                sc_copy_tokens = \
                    sc_copy_token_file.readline().strip().split(TOKEN_SEPARATOR)
                tg_copy_tokens = \
                    tg_copy_token_file.readline().strip().split(TOKEN_SEPARATOR)
                data_point.csc_ids, data_point.ctg_ids = \
                    compute_copy_indices(sc_tokens, tg_tokens,
                        sc_copy_tokens, tg_copy_tokens, vocab.tg_vocab, token_ext)
            sc_token_file.close()
            tg_token_file.close()
            sc_copy_token_file.close()
            tg_copy_token_file.close()

    if load_features and use_buckets:
        print('Group data points into buckets...')
        if split == 'train':
            # Determine bucket sizes based on the characteristics of the dataset
            num_buckets = FLAGS.num_buckets
            bucket_capacity = int(len(dataset) / num_buckets)
            assert(bucket_capacity > 0)
            # Excluding outliers (very long sequences)
            length_cutoff = 0.01
            # A. Determine maximum source length
            sorted_dataset = sorted(dataset, key=lambda x:len(x.sc_ids), reverse=True)
            max_sc_length = len(sorted_dataset[int(len(sorted_dataset) * length_cutoff)].sc_ids)
            # B. Determine maximum target length
            sorted_dataset = sorted(dataset, key=lambda x:len(x.tg_ids), reverse=True)
            max_tg_length = len(sorted_dataset[int(len(sorted_dataset) * length_cutoff)].tg_ids)
            print('max_source_length after filtering = {}'.format(max_sc_length))
            print('max_target_length after filtering = {}'.format(max_tg_length))
            # Determine thresholds for buckets of equal capacity
            buckets = []
            sorted_dataset = sorted(dataset, key=lambda x:len(x.sc_ids), reverse=False)
            max_tg_len_so_far = 0
            for i, dp in enumerate(sorted_dataset):
                if len(dp.sc_ids) > max_sc_length:
                    break
                if len(dp.tg_ids) > max_tg_len_so_far:
                    max_tg_len_so_far = len(dp.tg_ids)
                if i > 0 and i % bucket_capacity == 0:
                    buckets.append((len(dp.sc_ids)+1, min(max_tg_len_so_far, max_tg_length)+1))
            if len(buckets) == 0 or buckets[-1][0] < max(max_sc_length, max_tg_length):
                buckets.append((max_sc_length+1,
                                min(max_tg_len_so_far, max_tg_length)+1))
        else:
            num_buckets = len(buckets)
            assert(num_buckets >= 1)

        dataset2 = [[] for _ in buckets]
        for i in range(len(dataset)):
            data_point = dataset[i]
            # Compute bucket id
            bucket_ids = [b for b in xrange(len(buckets))
                          if buckets[b][0] > len(data_point.sc_ids) and
                          buckets[b][1] > len(data_point.tg_ids)]
            if bucket_ids:
                bucket_id = min(bucket_ids)
                dataset2[bucket_id].append(data_point)
            else:
                if split != 'train':
                    bucket_id = len(buckets) - 1
                    dataset2[bucket_id].append(data_point)
        dataset = dataset2
        if split != 'train':
            assert(len(functools.reduce(lambda x, y: x + y, dataset)) == data_size)
      
    D = DataSet()
    D.data_points = dataset
    if split == 'train' and load_features:
        D.max_sc_length = max_sc_length
        D.max_tg_length = max_tg_length
        if use_buckets:
            D.buckets = buckets

    return D


def load_vocabulary(FLAGS):
    data_dir = FLAGS.data_dir
    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')
    token_ext = 'normalized.{}'.format(FLAGS.channel) \
        if FLAGS.normalized else FLAGS.channel
    vocab_ext = 'vocab.{}'.format(token_ext)

    source_vocab_path = os.path.join(data_dir, '{}.{}'.format(source, vocab_ext))
    target_vocab_path = os.path.join(data_dir, '{}.{}'.format(target, vocab_ext))

    vocab = Vocab()
    min_vocab_frequency = 1 if FLAGS.channel == 'char' else FLAGS.min_vocab_frequency
    vocab.sc_vocab, vocab.rev_sc_vocab = initialize_vocabulary(
        source_vocab_path, min_vocab_frequency)
    vocab.tg_vocab, vocab.rev_tg_vocab = initialize_vocabulary(
        target_vocab_path, min_vocab_frequency)

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
    print('target vocabulary size = {}'.format(len(vocab.tg_vocab)))
    print('max source token size = {}'.format(vocab.max_sc_token_size))
    print('max target token size = {}'.format(vocab.max_tg_token_size))

    return vocab


def initialize_vocabulary(vocab_path, min_frequency=1):
    """Initialize vocabulary from file.

    The vocabulary is stored one-item-per-line, followed by its frequency in
    in the training set:
      dog   4
      cat   3
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
    if tf.io.gfile.exists(vocab_path):
        V = []
        with tf.io.gfile.GFile(vocab_path, mode="r") as f:
            while(True):
                line = f.readline()
                if line:
                    if line.startswith('\t'):
                        v = line[0]
                        freq = line.strip()   
                    else:
                        v, freq = line[:-1].rsplit('\t', 1)
                    if int(freq) >= min_frequency \
                            or data_tools.flag_suffix in v:
                        V.append(v)
                else:
                    break
        vocab = dict([(x, y) for (y, x) in enumerate(V)])
        rev_vocab = dict([(y, x) for (y, x) in enumerate(V)])
        assert(len(vocab) == len(rev_vocab))
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocab_path)


def load_vocabulary_frequency(FLAGS):
    data_dir = FLAGS.data_dir
    source, target = ('nl', 'cm') if not FLAGS.explain else ('cm', 'nl')
    token_ext = 'normalized.{}'.format(FLAGS.channel) \
        if FLAGS.normalized else FLAGS.channel
    vocab_ext = 'vocab.{}'.format(token_ext)

    source_vocab_path = os.path.join(data_dir, '{}.{}'.format(source, vocab_ext))
    target_vocab_path = os.path.join(data_dir, '{}.{}'.format(target, vocab_ext))

    sc_vocab_freq = initialize_vocabulary_frequency(source_vocab_path)
    tg_vocab_freq = initialize_vocabulary_frequency(target_vocab_path)

    return sc_vocab_freq, tg_vocab_freq


def initialize_vocabulary_frequency(vocab_path):
    vocab_freq = {}
    with open(vocab_path) as f:
        counter = 0
        for line in f:
            if line.startswith('\t'):
                v = line[0]
                freq = line.strip()
            else:
                v, freq = line.rsplit('\t', 1)
            vocab_freq[counter] = int(freq)
            counter += 1
    return vocab_freq


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
    channel = FLAGS.channel if FLAGS.channel else ''
    if channel and FLAGS.normalized:
        channel = 'normalized.{}'.format(channel)
    prepare_dataset_split(data_dir, 'train', channel=channel)
    prepare_dataset_split(data_dir, 'dev', channel=channel)
    prepare_dataset_split(data_dir, 'test', channel=channel)


def prepare_dataset_split(data_dir, split, channel=''):
    """
    Process a specific dataset split.
    """
    def read_parallel_data(nl_path, cm_path):
        with open(nl_path, encoding='utf-8') as f:
            nl_list = [nl.strip() for nl in f.readlines()]
        with open(cm_path, encoding='utf-8') as f:
            cm_list = [cm.strip() for cm in f.readlines()]
        return nl_list, cm_list

    print("Split - {}".format(split))
    nl_path = os.path.join(data_dir, split + '.nl.filtered')
    cm_path = os.path.join(data_dir, split + '.cm.filtered')
    nl_list, cm_list = read_parallel_data(nl_path, cm_path)

    # character based processing
    if not channel or channel == 'char':
        prepare_channel(data_dir, nl_list, cm_list, split, channel='char',
                        parallel_data_to_tokens=parallel_data_to_characters)
    # partial-token based processing
    if not channel or channel == 'partial.token':
        prepare_channel(data_dir, nl_list, cm_list, split, channel='partial.token',
                        parallel_data_to_tokens=parallel_data_to_partial_tokens)
    # token based processing
    if not channel or channel == 'token':
        prepare_channel(data_dir, nl_list, cm_list, split, channel='token',
                        parallel_data_to_tokens=parallel_data_to_tokens)
    # normalized token based processing
    if not channel or channel == 'normalized.token':
        prepare_channel(data_dir, nl_list, cm_list, split, channel='normalized.token',
                        parallel_data_to_tokens=parallel_data_to_normalized_tokens)


def prepare_channel(data_dir, nl_list, cm_list, split, channel,
                    parallel_data_to_tokens):
    print("    channel - {}".format(channel))
    # Tokenize data
    nl_tokens, cm_tokens = \
        parallel_data_to_tokens(nl_list, cm_list)
    save_channel_features_to_file(data_dir, split, channel, nl_tokens, cm_tokens,
                                  feature_separator=TOKEN_SEPARATOR)
    # Create or load vocabulary
    nl_vocab_path = os.path.join(data_dir, 'nl.vocab.{}'.format(channel))
    cm_vocab_path = os.path.join(data_dir, 'cm.vocab.{}'.format(channel))
    nl_vocab = create_vocabulary(nl_vocab_path, nl_tokens) \
        if split == 'train' else initialize_vocabulary(nl_vocab_path)[0]
    cm_vocab = create_vocabulary(cm_vocab_path, cm_tokens) \
        if split == 'train' else initialize_vocabulary(cm_vocab_path)
    nl_ids = [tokens_to_ids(data_point, nl_vocab) for data_point in nl_tokens]
    cm_ids = [tokens_to_ids(data_point, cm_vocab) for data_point in cm_tokens]
    save_channel_features_to_file(data_dir, split, 'ids.{}'.format(channel),
                                  nl_ids, cm_ids, feature_separator=' ')
    # For copying
    if channel == 'char':
        nl_copy_tokens, cm_copy_tokens = nl_tokens, cm_tokens
    else:
        if channel == 'partial.token':
            nl_copy_tokens = [nl_to_partial_tokens(nl, tokenizer.basic_tokenizer,
                to_lower_case=False, lemmatization=False) for nl in nl_list]
        else:
            nl_copy_tokens = [nl_to_tokens(nl, tokenizer.basic_tokenizer,
                to_lower_case=False, lemmatization=False) for nl in nl_list]
        cm_copy_tokens = cm_tokens
    save_channel_features_to_file(data_dir, split, 'copy.{}'.format(channel),
        nl_copy_tokens, cm_copy_tokens, feature_separator=TOKEN_SEPARATOR)
    alignments = compute_alignments(data_dir, nl_tokens, cm_tokens, split, channel)
    with open(os.path.join(data_dir, '{}.{}.align'.format(split, channel)),
              'wb') as o_f:
        pickle.dump(alignments, o_f)


def save_channel_features_to_file(data_dir, split, channel, nl_features,
                                  cm_features, feature_separator):
    convert_to_str = channel.startswith('ids')
    nl_feature_path = os.path.join(data_dir, '{}.nl.{}'.format(split, channel))
    cm_feature_path = os.path.join(data_dir, '{}.cm.{}'.format(split, channel))
    with open(nl_feature_path, 'w', encoding='utf-8') as o_f:
        for data_point in nl_features:
            if convert_to_str:
                o_f.write('{}\n'.format(feature_separator.join(
                    [str(x) for x in data_point])))
            else:
                o_f.write('{}\n'.format(feature_separator.join(data_point)))
    with open(cm_feature_path, 'w', encoding='utf-8') as o_f:
        for data_point in cm_features:
            if convert_to_str:
                o_f.write('{}\n'.format(feature_separator.join(
                    [str(x) for x in data_point])))
            else:
                o_f.write('{}\n'.format(feature_separator.join(data_point)))


def parallel_data_to_characters(nl_list, cm_list):
    nl_data = [nl_to_characters(nl) for nl in nl_list]
    cm_data = [cm_to_characters(cm) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_partial_tokens(nl_list, cm_list):
    nl_data = [nl_to_partial_tokens(nl, tokenizer.basic_tokenizer) for nl in nl_list]
    cm_data = [cm_to_partial_tokens(cm, data_tools.bash_tokenizer) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_tokens(nl_list, cm_list):
    nl_data = [nl_to_tokens(nl, tokenizer.basic_tokenizer) for nl in nl_list]
    cm_data = [cm_to_tokens(cm, data_tools.bash_tokenizer) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_normalized_tokens(nl_list, cm_list):
    nl_data = [nl_to_tokens(nl, tokenizer.ner_tokenizer) for nl in nl_list]
    cm_data = [cm_to_tokens(cm, data_tools.bash_tokenizer, arg_type_only=True)
               for cm in cm_list]
    return nl_data, cm_data


def string_to_characters(s):
    assert(isinstance(s, str))
    chars = []
    for c in s:
        if c == ' ':
            chars.append(constants._SPACE)
        else:
            chars.append(c)
    return chars


def nl_to_characters(nl, use_preprocessing=False):
    nl_data_point = []
    if use_preprocessing:
        nl_tokens = nl_to_tokens(nl, tokenizer.basic_tokenizer, lemmatization=False)
        for c in ' '.join(nl_tokens):
            if c == ' ':
                nl_data_point.append(constants._SPACE)
            else:
                nl_data_point.append(c)
    else:
        nl_data_point = string_to_characters(nl)
    return nl_data_point


def cm_to_characters(cm, use_preprocessing=False):
    cm_data_point = []
    if use_preprocessing:
        cm_tokens = cm_to_tokens(
            cm, data_tools.bash_tokenizer, with_prefix=True,
            with_flag_argtype=True)
        for i, t in enumerate(cm_tokens):
            if not nast.KIND_PREFIX in t:
                cm_data_point.append(t)
            else:
                kind, token = t.split(nast.KIND_PREFIX, 1)
                if kind.lower() == 'utility':
                    cm_data_point.append(token)
                elif kind.lower() == 'flag':
                    cm_data_point.append(token)
                else:
                    for c in token:
                        cm_data_point.append(c)
            if i < len(cm_tokens) - 1:
                cm_data_point.append(constants._SPACE)
    else:
        cm = data_tools.correct_errors_and_normalize_surface(cm)
        cm_data_point = string_to_characters(cm)
    return cm_data_point


def nl_to_partial_tokens(s, tokenizer, to_lower_case=True, lemmatization=True):
    return string_to_partial_tokens(
        nl_to_tokens(s, tokenizer, to_lower_case=to_lower_case,
                     lemmatization=lemmatization), use_arg_start_end=False)


def cm_to_partial_tokens(s, tokenizer):
    s = data_tools.correct_errors_and_normalize_surface(s)
    return string_to_partial_tokens(cm_to_tokens(s, tokenizer))


def string_to_partial_tokens(s, use_arg_start_end=True):
    """
    Split a sequence of tokens into a sequence of partial tokens.

    A partial token sequence may consist of
        1. continuous span of alphabetical letters
        2. continuous span of digits
        3. a non-alpha-numerical character
        4. _ARG_START which indicates the beginning of an argument token
        5. _ARG_END which indicates the end of an argument token
    """
    partial_tokens = []

    for token in s:
        if not token:
            continue
        if token.isalpha() or token.isnumeric() \
                or data_tools.flag_suffix in token \
                or token in bash.binary_logic_operators \
                or token in bash.left_associate_unary_logic_operators \
                or token in bash.right_associate_unary_logic_operators:
            partial_tokens.append(token)
        else:
            arg_partial_tokens = []
            pt = ''
            reading_alpha = False
            reading_numeric = False
            for c in token:
                if reading_alpha:
                    if c.isalpha():
                        pt += c
                    else:
                        arg_partial_tokens.append(pt)
                        reading_alpha = False
                        pt = c
                        if c.isnumeric():
                            reading_numeric = True
                elif reading_numeric:
                    if c.isnumeric():
                        pt += c
                    else:
                        arg_partial_tokens.append(pt)
                        reading_numeric = False
                        pt = c
                        if c.isalpha():
                            reading_alpha = True
                else:
                    if pt:
                        arg_partial_tokens.append(pt)
                    pt = c
                    if c.isalpha():
                        reading_alpha = True
                    elif c.isnumeric():
                        reading_numeric = True
            if pt:
                arg_partial_tokens.append(pt)
            if len(arg_partial_tokens) > 1:
                if use_arg_start_end:
                    partial_tokens.append(_ARG_START)
                partial_tokens.extend(arg_partial_tokens)
                if use_arg_start_end:
                    partial_tokens.append(_ARG_END)
            else:
                partial_tokens.extend(arg_partial_tokens)

    return partial_tokens


def nl_to_tokens(s, tokenizer, to_lower_case=True, lemmatization=True):
    """
    Split a natural language string into a sequence of tokens.
    """
    tokens, _ = tokenizer(
        s, to_lower_case=to_lower_case, lemmatization=lemmatization)
    return tokens


def cm_to_tokens(s, tokenizer, loose_constraints=True, arg_type_only=False,
                 with_prefix=False, with_flag_argtype=True):
    """
    Split a command string into a sequence of tokens.
    """
    tokens = tokenizer(s, loose_constraints=loose_constraints,
                       arg_type_only=arg_type_only, 
                       with_prefix=with_prefix,
                       with_flag_argtype=with_flag_argtype)
    return tokens


def tokens_to_ids(tokens, vocabulary):
    """
    Map tokens into their indices in the vocabulary.
    """
    token_ids = []
    for t in tokens:
        if t in vocabulary:
            token_ids.append(vocabulary[t])
        else:
            token_ids.append(UNK_ID)
    return token_ids


def compute_copy_indices(sc_tokens, tg_tokens, sc_copy_tokens, tg_copy_tokens,
                         tg_vocab, channel):
    assert(len(sc_tokens) == len(sc_copy_tokens))
    assert(len(tg_tokens) == len(tg_copy_tokens))
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


def compute_alignments(data_dir, nl_list, cm_list, split, channel):
    alignments = []
    output_path = os.path.join(data_dir, '{}.{}.align.readable'.format(split, channel))
    with open(output_path, 'w') as o_f:
        for nl_tokens, cm_tokens in zip(nl_list, cm_list):
            alignments.append(compute_pair_alignment(nl_tokens, cm_tokens, o_f))
    return alignments


def compute_pair_alignment(nl_tokens, cm_tokens, out_file):
    """
    Compute the alignments between two parallel sequences.
    """
    init_vocab = set(TOKEN_INIT_VOCAB + CHAR_INIT_VOCAB)
    m = len(nl_tokens)
    n = len(cm_tokens)

    A = np.zeros([m, n], dtype=np.int32)

    for i, x in enumerate(nl_tokens):
        for j, y in enumerate(cm_tokens):
            if not x in init_vocab and x == y:
                A[i, j] = 1
                out_file.write('{}-{} '.format(i, j))
    out_file.write('\n')

    return ssp.lil_matrix(A)


def create_vocabulary(vocab_path, dataset, min_word_frequency=1,
                      is_character_model=False, parallel_dataset=None):
    """
    Compute the vocabulary of a tokenized dataset and save to file.
    """
    vocab = collections.defaultdict(int)
    num_copy = collections.defaultdict(int)
    if parallel_dataset:
        for i, data_point in enumerate(dataset):
            parallel_data_point = parallel_dataset[i]
            for token in data_point:
                vocab[token] += 1
                if token in parallel_data_point:
                    num_copy[token] += 1
        for v in vocab:
            if vocab[v] == num_copy[v]:
                vocab[v] = 0
    else:
        for data_point in dataset:
            for token in data_point:
                vocab[token] += 1
    sorted_vocab = [(x, y) for x, y in sorted(
            vocab.items(), key=lambda x:(x[1], x[0]), reverse=True) 
            if y >= min_word_frequency]
    
    if is_character_model:
        # Character model
        init_vocab = CHAR_INIT_VOCAB
    else:
        init_vocab = TOKEN_INIT_VOCAB
    vocab = [(v, 1000000) for v in init_vocab]
    for v, f in sorted_vocab:
        if not v in init_vocab:
            vocab.append((v, f))

    with open(vocab_path, 'w', encoding='utf-8') as vocab_file:
        for v, f in vocab:
            vocab_file.write('{}\t{}\n'.format(v, f))

    return dict([(x[0], y) for y, x in enumerate(vocab)])


def group_parallel_data(dataset, attribute='source', use_temp=False,
                        tokenizer_selector='nl'):
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
    if dataset.data_points and isinstance(dataset.data_points, list):
        if isinstance(dataset.data_points[0], list):
            data_points = functools.reduce(lambda x, y: x + y, dataset.data_points)
        else:
            data_points = dataset.data_points
    else:
        raise ValueError

    grouped_dataset = {}
    for i in xrange(len(data_points)):
        data_point = data_points[i]
        attr = data_point.sc_txt \
            if attribute == 'source' else data_point.tg_txt
        if use_temp:
            if tokenizer_selector == 'nl':
                words, _ = tokenizer.ner_tokenizer(attr)
            else:
                words = data_tools.bash_tokenizer(attr, arg_type_only=True)
            temp = ' '.join(words)
        else:
            if tokenizer_selector == 'nl':
                words, _ = tokenizer.basic_tokenizer(attr)
                temp = ' '.join(words)
            else:
                temp = attr
        if temp in grouped_dataset:
            grouped_dataset[temp].append(data_point)
        else:
            grouped_dataset[temp] = [data_point]
    return sorted(grouped_dataset.items(), key=lambda x: x[0])


if __name__ == '__main__':
    print(nl_to_partial_tokens('Execute md5sum command on files found by the find command',
                               tokenizer=tokenizer.basic_tokenizer))
    print(cm_to_partial_tokens("find . -perm -600 -print",
                               tokenizer=data_tools.bash_tokenizer))
