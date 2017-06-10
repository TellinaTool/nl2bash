# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
Utilities for tokenizing & generating vocabularies.
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

from numpy.linalg import norm

if sys.version_info > (3, 0):
    from six.moves import xrange

from bashlex import normalizer, data_tools
from nlp_tools import constants, tokenizer, slot_filling

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

_TOKEN_START_VOCAB = [
    _PAD,
    _EOS,
    _UNK,
    _ARG_UNK,
    _UTL_UNK,
    _FLAG_UNK,
    normalizer._H_NO_EXPAND,
    normalizer._V_NO_EXPAND,
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

_CHAR_START_VOCAB = [_CPAD, _CEOS, _CUNK, _CATOM, constants._LONG_TOKEN_IND,
                     _CGO]

_data_splits = ['train', 'dev', 'test']


def create_vocabulary(vocab_path, data, max_vocabulary_size, min_word_frequency,
                      tokenizer=None, base_tokenizer=None, append_to_vocab=False):
    """Create vocabulary file (if it does not exist yet) from data file.

    Data file is assumed to contain one sentence per line. Each sentence is
    tokenized and digits are normalized (if normalize_digits is set).
    Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
    We write it to vocab_path in a one-token-per-line format, so that later
    token in the first line gets id=0, second line gets id=1, and so on.

    Args:
      vocab_path: path where the vocabulary will be created.
      data: list of lines each of which corresponds to a data point.
      max_vocabulary_size: limit on the size of the created vocabulary.
      min_word_frequency: word frequency threshold below which a word is
        goint to be marked as _UNK.
      tokenizer: a function to use to tokenize each data sentence;
        if None, basic_tokenizer will be used.
      base_tokenizer: base_tokenizer used for separating a string into chars.
      append_to_vocab: set to true to append new words as unseen to the vocab
      (used for simplifying testing sentences with unseen tokens).
    """

    MIN_ARG_FREQ = 30

    vocab = {}

    if not tf.gfile.Exists(vocab_path):
        print("Creating vocabulary %s from data (%d)" %
              (vocab_path, len(data)))
        sorted_vocab = {}
    else:
        print("Reading vocabulary %s from path" % vocab_path)
        sorted_vocab, _ = initialize_vocabulary(vocab_path)

    if not tf.gfile.Exists(vocab_path) or append_to_vocab:
        counter = 0
        for line in data:
            counter += 1
            if counter % 1000 == 0:
                print("  processing line %d" % counter)
            if type(line) is list:
                tokens = line
            else:
                if base_tokenizer:
                    tokens = tokenizer(line, base_tokenizer)
                else:
                    tokens = tokenizer(line)
            if not tokens:
                continue
            for word in tokens:
                if "char" in vocab_path and word == ' ':
                    word = constants._SPACE
                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1
        if append_to_vocab:
            for v in vocab:
                if not v in sorted_vocab and not ('__LF__' + v) in sorted_vocab \
                        and not v[len('__LF__'):] in sorted_vocab:
                    if v.startswith('__LF__'):
                        sorted_vocab[v] = 1e12
                    else:
                        sorted_vocab['__LF__' + v] = 1e12
            sorted_vocab = [x for (x, y) in
                sorted(sorted_vocab.items(), key=lambda x:x[1])]
        else:
            for v in vocab:
                if v.startswith('__SP__'):
                    sorted_vocab[v] = vocab[v]
                elif v.startswith('__FLAG__'):
                    sorted_vocab[v] = vocab[v]
                elif v.startswith('__ARG__'):
                    if vocab[v] >= MIN_ARG_FREQ:
                        sorted_vocab[v] = vocab[v]
                    else:
                        sorted_vocab['__LF__' + v] = \
                            min(vocab[v], min_word_frequency-1)
                else:
                    if 'bash' in vocab_path and '.nl' in vocab_path and \
                            not constants.is_english_word(v) and \
                            not v in constants.type_conversion and \
                            not v in constants.punctuation:
                        # print("Infrequent token: %s"  % v)
                        sorted_vocab['__LF__' + v] = \
                            min(vocab[v], min_word_frequency-1)
                    elif vocab[v] >= min_word_frequency:
                        sorted_vocab[v] = vocab[v]
                    else:
                        sorted_vocab['__LF__' + v] = vocab[v]
            sorted_vocab = [x for (x, y) in
                sorted(sorted_vocab.items(), key=lambda x:x[1], reverse=True)]

        start_vocab = _CHAR_START_VOCAB \
            if "char" in vocab_path else _TOKEN_START_VOCAB
        vocab = list(start_vocab)
        for v in sorted_vocab:
            if not v in start_vocab:
                vocab.append(v)

        if len(vocab) > max_vocabulary_size:
            vocab = vocab[:max_vocabulary_size]
        with tf.gfile.GFile(vocab_path, mode="wb") as vocab_file:
            for w in vocab:
                try:
                    vocab_file.write(w + b"\n")
                except Exception:
                    vocab_file.write(w.encode('utf-8') + b"\n")


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
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocab_path)


def data_to_token_ids(data, tg_id_path, vocab_path, tokenizer=None,
        base_tokenizer=None, use_unk=True, parallel_data=None,
        use_source_placeholder=False, use_unk_placeholder=False,
        parallel_vocab_path=None, parallel_vocab_size=None,
        coarse_typing=False, add_type_prefix=False, remove_type_prefix=False):
    """Tokenize data file and turn into token-ids using given vocabulary file.

    This function loads data line-by-line from data_path, calls the above
    sentence_to_token_ids, and saves the result to tg_id_path. See comment
    for sentence_to_token_ids on the details of token-ids format.

    Args:
      data: list of lines each of which corresponds to a data point.
      tg_id_path: path where the file with token-ids will be created.
      vocab_path: path to the vocabulary file.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      base_tokenizer: base tokenizer used for splitting strings into characters.
      use_unk: if set, set low-frequency tokens to UNK.
      parallel_data: Used for computing the CopyNet training objective
        (if a target token has appeared in the source, store its vocabulary
         index; otherwise, marked as unknown).
      use_source_placeholder: If set, map tokens to placeholder indices instead of
        indices in the vocabulary. Used for generating source copy indices in
        copy mode.
      parallel_vocab_size: Vocabulary size of the parallel language, used for
        creading dummy indices in CopyNet.
      coarse_typing: If set, replace tokens with coarse types.
      add_type_prefix: If set, add type prefix of the token while indexing.
      remove_type_prefix: If set, remove type prefix of the token while indexing.
    """
    max_token_num = 0
    if not tf.gfile.Exists(tg_id_path):
        print("Tokenizing data {} ({})".format(tg_id_path, len(data)))
        tokens_file = tf.gfile.GFile(tg_id_path, mode="w")
        vocab, _ = initialize_vocabulary(vocab_path)

        if parallel_vocab_path is not None:
            parallel_vocab, _ = initialize_vocabulary(parallel_vocab_path)
        else:
            parallel_vocab = None
        if parallel_data is not None:
            assert(len(data) == len(parallel_data))

        counter = 0
        for i in xrange(len(data)):
            counter += 1
            if counter % 1000 == 0:
                print("  tokenizing line %d" % counter)
            if parallel_data is None:
                parallel_line = None
            else:
                parallel_line = parallel_data[i]
            token_ids, _ = sentence_to_token_ids(data[i], vocab, tokenizer,
                base_tokenizer, use_unk=use_unk,
                use_typed_unk=('bash' in vocab_path and '.cm' in vocab_path),
                parallel_sequence=parallel_line,
                use_source_placeholder=use_source_placeholder,
                use_unk_placeholder=use_unk_placeholder,
                parallel_vocabulary=parallel_vocab,
                parallel_vocab_size=parallel_vocab_size,
                coarse_typing=coarse_typing,
                add_type_prefix=add_type_prefix,
                remove_type_prefix=remove_type_prefix)
            if len(token_ids) > max_token_num:
                max_token_num = len(token_ids)
            tokens_file.write(" ".join([str(tok) for tok in token_ids]) + "\n")
        tokens_file.close()
    return max_token_num


def sentence_to_token_ids(sentence, vocabulary, tokenizer, base_tokenizer,
        use_unk=True, use_typed_unk=False, parallel_sequence=None,
        use_source_placeholder=False, use_unk_placeholder=False,
        parallel_vocabulary=None, parallel_vocab_size=-1,
        coarse_typing=False, add_type_prefix=False, remove_type_prefix=False):
    """
    Convert a string to a list of integers representing token-ids.

    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].

    Args:
        sentence: The sentence in bytes format to convert to token-ids.
        vocabulary: A dictionary mapping tokens to integers.
        tokenizer: A function to use to tokenize each sentence;
            if None, basic_tokenizer will be used.
        base_tokenizer: Used to tokenize a sentence prior to character feature
            extraction.

        use_unk: If set, replace the low-frequency tokens with UNK.
        use_typed_unk: If set, add type prefix to UNK tokens.
        parallel_sequence: Used for computing the CopyNet training objective
          (if a target token has appeared in the source, store its vocabulary
           index; otherwise, marked as unknown).
        use_source_placeholder: If set, map tokens to placeholder indices instead of
            indices in the vocabulary. Used for generating source copy indices
            in copy mode.
        parallel_vocab_size: Vocabulary size of the parallel data, used for
            creating dummy indices in CopyNet.
        coarse_typing: If set, replace tokens with coarse types.
        add_type_prefix: If set, add type prefix of the token while indexing.
        remove_type_prefix: If set, remove type prefix of the token while indexing.
    Returns:
        a list of integers, the token-ids for the sentence.
    """
    if type(sentence) is list:
        words = sentence
        entities = None
    else:
        if base_tokenizer:
            words = tokenizer(sentence, base_tokenizer)
            entities = None
        else:
            words, entities = tokenizer(sentence)

    token_ids = []

    def get_index(w, vocab):
        if w in vocab:
            return vocab[w]

        if add_type_prefix:
            if '__ARG__' + w in vocab:
                return vocab['__ARG__' + w]
            elif '__FLAG__' + w in vocab:
                return vocab['__FLAG__' + w]
        if remove_type_prefix:
            if w.startswith('__ARG__') and w[len('__ARG__'):] in vocab:
                return vocab[w[len('__ARG__'):]]
            elif w.startswith('__FLAG__') and w[len('__FLAG__'):] in vocab:
                return vocab[w[len('__FLAG__'):]]

        if '__LF__' + w in vocab:
            return vocab['__LF__' + w]
        elif '__LF____ARG__' + w in vocab:
            return vocab['__LF____ARG__' + w]
        elif '__LF____FLAG__' + w in vocab:
            return vocab['__LF____FLAG__' + w]

        if w.startswith('__ARG__'):
            return ARG_UNK_ID
        if w.startswith('__FLAG__'):
            return FLAG_UNK_ID

        return UNK_ID

    def get_unk_symbol(w):
        if use_typed_unk:
            if '__ARG__' in w:
                return ARG_UNK_ID
            elif '__FLAG__' in w:
                return FLAG_UNK_ID
            else:
                return UNK_ID
        else:
            return UNK_ID

    if use_source_placeholder:
        assert(parallel_vocab_size != -1)

    for (i, w) in enumerate(words):
        if parallel_vocabulary:
            word_id = get_index(w, parallel_vocabulary)
            is_unk = not w in parallel_vocabulary or is_low_frequency(w)
        else:
            word_id = get_index(w, vocabulary)
            is_unk = not w in vocabulary or is_low_frequency(w)

        if is_unk:
            # out-of-vocabulary word
            if parallel_sequence is not None and (
                (w.startswith('__ARG__') and w[len('__ARG__'):] in parallel_sequence)
                or (w.startswith('__FLAG__') and w[len('__FLAGS__'):] in parallel_sequence)
                or (('__ARG__' + w) in parallel_sequence)
                or (('__FLAG__' + w) in parallel_sequence)):
                # If the token has appeared in the parallel sequence, store its
                # vocabulary index. Used to compute the CopyNet training objective.
                token_ids.append(word_id)
            elif coarse_typing:
                if is_low_frequency(w):
                    w = w[len('__LF__'):]
                if w.isdigit():
                    token_ids.append(NUM_ID)
                elif re.match(re.compile('[0-9]+[A-Za-z]+'), w):
                    token_ids.append(NUM_ALPHA_ID)
                elif not constants.is_english_word(w):
                    token_ids.append(NON_ENGLISH_ID)
                else:
                    if use_unk:
                        token_ids.append(UNK_ID)
                    else:
                        token_ids.append(word_id)
            elif use_source_placeholder:
                if (not w in vocabulary or is_low_frequency(w)) \
                        and use_unk_placeholder:
                    token_ids.append(get_unk_symbol(w))
                else:
                    token_ids.append(parallel_vocab_size + i)
            else:
                if use_unk:
                    token_ids.append(get_unk_symbol(w))
                else:
                    token_ids.append(word_id)
        else:
            # in-vocabulary word
            token_ids.append(word_id)

    return token_ids, entities


def token_to_char_ids(token, vocabulary):
    """
    Convert a token to a list of integers representing character-ids.
    """
    char_ids = []
    if len(token) <= 20:
        characters = token
    else:
        characters = list(token[:14]) \
            + [constants._LONG_TOKEN_IND] + list(token[-5:])

    for c in characters:
        if c in vocabulary:
            char_ids.append(vocabulary[c])
        else:
            if c == ' ':
                char_ids.append(vocabulary[constants._SPACE])
            else:
                # Unknown character
                char_ids.append(CUNK_ID)
    return char_ids


def token_ids_to_sentences(inputs, rev_vocab, head_appended=False,
                           char_model=False):
    """
    Convert a batch of token-id lists to a list of strings.
    """
    batch_size = len(inputs[0])
    sentences = []
    for i in xrange(batch_size):
        if head_appended:
            outputs = [decoder_input[i] for decoder_input in inputs[1:]]
        else:
            outputs = [decoder_input[i] for decoder_input in inputs]
        # If there is an EOS symbol in outputs, cut them at that point.
        if EOS_ID in outputs:
            outputs = outputs[:outputs.index(EOS_ID)]
        # If there is a PAD symbol in outputs, cut them at that point.
        if PAD_ID in outputs:
            outputs = outputs[:outputs.index(PAD_ID)]
        # Print out command corresponding to outputs.
        if char_model:
            sentences.append("".join([tf.compat.as_str(rev_vocab[output])
                for output in outputs]).replace(constants._SPACE, ' '))
        else:
            sentences.append(" ".join([tf.compat.as_str(rev_vocab[output])
                                       for output in outputs]))
    return sentences


def fold_split_bucket(data_set, num_folds):
    # if a dataset is grouped by buckets
    # randomly split each bucket
    num_buckets = len(data_set)
    data_folds = [[] for _ in xrange(num_folds)]
    for bucket_id in xrange(num_buckets):
        bucket_data_folds = fold_split(data_set[bucket_id], num_folds)
        for fold_id in xrange(num_folds):
            data_folds[fold_id].append(bucket_data_folds[fold_id])
    return data_folds


def fold_split(data_set, num_folds):
    # randomly split a dataset for cross validation
    data_folds = [[] for _ in xrange(num_folds)]
    num_rep = int(len(data_set) / num_folds) + 1
    fold_ids = range(num_folds) * num_rep
    random.shuffle(fold_ids)
    for i in xrange(len(data_set)):
        data_point = data_set[i]
        fold_id = fold_ids[i]
        data_folds[fold_id].append(data_point)
    return data_folds


def read_raw_data(data_dir):
    nl_list = DataSet()
    cm_list = DataSet()
    for split in _data_splits:
        data_path = os. path.join(data_dir, split)
        if os.path.exists(data_path + ".nl"):
            with open(data_path + '.nl') as f:
                setattr(nl_list, split,
                        [line.strip() for line in f.readlines()])
        if os.path.exists(data_path + ".cm"):
            with open(data_path + ".cm") as f:
                setattr(cm_list, split,
                        [line.strip() for line in f.readlines()])
    return nl_list, cm_list


def prepare_dataset(data, data_dir, suffix, vocab_size, vocab_path,
                    create_vocab=True, parallel_vocab_size=-1,
                    parallel_vocab_path=None, parallel_data=None):
    if isinstance(data.train[0], list):
        # save indexed token sequences
        is_bash_nl = 'bash' in data_dir and suffix.endswith('.nl')
        is_bash_cm = 'bash' in data_dir and suffix.endswith('.cm')
        is_regex_turk_nl = 'regex-turk' in data_dir and suffix.endswith('.nl')
        is_regex_kb13_nl = 'regex-kb13' in data_dir and suffix.endswith('.nl')

        if create_vocab:
            MIN_WORD_FREQ = 2 if is_bash_nl or is_bash_cm \
                or is_regex_turk_nl or is_regex_kb13_nl \
                else 1
            create_vocabulary(vocab_path, data.train, vocab_size,
                              min_word_frequency=MIN_WORD_FREQ)
            if suffix.endswith('.nl') or suffix.endswith('.cm'):
                create_vocabulary(vocab_path, data.dev, vocab_size,
                    min_word_frequency=MIN_WORD_FREQ, append_to_vocab=True)
                create_vocabulary(vocab_path, data.test, vocab_size,
                    min_word_frequency=MIN_WORD_FREQ, append_to_vocab=True)
        for split in _data_splits:
            data_path = os.path.join(data_dir, split)
            if suffix.endswith('.copy'):
                assert(parallel_vocab_size != -1)
                assert(parallel_vocab_path is not None)
                assert(parallel_data is not None)
                parallel_split = getattr(parallel_data, split) \
                    if split in ['train', 'dev'] else None
                # compute CopyNet source indices
                data_to_token_ids(getattr(data, split), data_path + suffix + '.sc',
                    vocab_path=vocab_path, use_source_placeholder=True,
                    use_unk_placeholder=(split in ['train']),
                    parallel_vocab_path=parallel_vocab_path,
                    parallel_vocab_size=parallel_vocab_size,
                    parallel_data=parallel_split,
                    add_type_prefix=is_bash_nl,
                    remove_type_prefix=is_bash_cm)
                # compute CopyNet target indices
                data_to_token_ids(getattr(data, split), data_path + suffix + '.tg',
                    vocab_path, parallel_data=parallel_split,
                    add_type_prefix=False,
                    remove_type_prefix=False)
            else:
                data_to_token_ids(getattr(data, split), data_path + suffix,
                    vocab_path, coarse_typing=is_bash_nl)
                if suffix.endswith('.nl') or suffix.endswith('.cm'):
                    data_to_token_ids(getattr(data, split),
                        data_path + suffix + '.full', vocab_path, use_unk=False)
    else:
        # save plain string
        for split in _data_splits:
            data_path = os.path.join(data_dir, split)
            with open(data_path + suffix, 'w') as o_f:
                for line in getattr(data, split):
                    print(line)
                    o_f.write(line.strip() + '\n')

    # compute max training sequence length to determine bucket size
    max_len = 0
    for d in data.train:
        if len(d) > max_len:
            max_len = len(d)
    return max_len


def compute_channel_representations(vocab_path, char_vocab_path,
                                    pad_start=False, add_eos=False):
    vocab, _ = initialize_vocabulary(vocab_path)
    char_vocab, _ = initialize_vocabulary(char_vocab_path)
    vocab_token_feature_path = vocab_path + ".token.feature"
    vocab_char_feature_path = vocab_path + ".char.feature"

    # token channel
    vocab_token_features = np.zeros(len(vocab), dtype=np.int64)
    for v in vocab:
        idx = vocab[v]
        vocab_token_features[idx] = UNK_ID \
            if v.startswith('__LF__') else idx
    np.save(vocab_token_feature_path, vocab_token_features)

    # character channel
    max_token_size = 0
    char_ids_list = []
    with open(vocab_char_feature_path, 'w') as o_f:
        for token, _ in sorted(vocab.items(), key=lambda x:x[1]):
            if token.startswith("__SP__"):
                # special tokens are non-decomposable
                char_ids = [CATOM_ID]
            else:
                if token.startswith("__LF__"):
                    # remove prefix for low-frequency words
                    char_ids = token_to_char_ids(token[6:], char_vocab)
                elif "@@" in token:
                    char_ids = token_to_char_ids(
                        token.split('@@')[1], char_vocab)
                else:
                    char_ids = token_to_char_ids(token, char_vocab)
                if len(char_ids) > max_token_size:
                    max_token_size = len(char_ids)
            char_ids_list.append(char_ids)
            o_f.write(' '.join([str(c_id) for c_id in char_ids]) + '\n')
    print("maximum token size in {} = {}".format(vocab_path, max_token_size))

    if add_eos:
        vocab_char_features = np.zeros(
            [len(vocab), max_token_size+1], dtype=np.int64)
    else:
        vocab_char_features = np.zeros(
            [len(vocab), max_token_size], dtype=np.int64)
    for token_id in xrange(len(char_ids_list)):
        char_ids = char_ids_list[token_id]
        if add_eos:
            char_ids.append(CEOS_ID)
        # padding character indices
        if pad_start:
            padded_char_ids = \
                [CPAD_ID] * (max_token_size - len(char_ids)) + char_ids
        else:
            padded_char_ids = \
                char_ids + [CPAD_ID] * (max_token_size - len(char_ids))
        for j in xrange(len(padded_char_ids)):
            c_id = padded_char_ids[j]
            vocab_char_features[token_id][j] = c_id
    np.save(vocab_char_feature_path, vocab_char_features)


def prepare_jobs(FLAGS):
    data_dir = FLAGS.data_dir
    nl_vocab_size = FLAGS.nl_vocab_size
    cm_vocab_size = FLAGS.cm_vocab_size

    def add_to_set(nl_data, cm_data, split):
        for nl, cm in zip(getattr(nl_data, split), getattr(cm_data, split)):
            if FLAGS.dataset in ['regex-turk', 'regex-kb13']:
                nl_tokenizer = tokenizer.basic_tokenizer
            else:
                nl_tokenizer = tokenizer.space_tokenizer
            nl_tokens, _ = nl_tokenizer(nl)
            cm_tokens = cm.split()
            nl_chars = data_tools.char_tokenizer(nl, nl_tokenizer)
            cm_chars = data_tools.char_tokenizer(cm, None)
            getattr(nl_list, split).append(nl)
            getattr(cm_list, split).append(cm)
            getattr(nl_char_list, split).append(nl_chars)
            getattr(cm_char_list, split).append(cm_chars)
            getattr(nl_token_list, split).append(nl_tokens)
            getattr(cm_token_list, split).append(cm_tokens)

    # unfiltered data
    nl_data, cm_data = read_raw_data(data_dir)

    nl_list = DataSet()
    cm_list = DataSet()
    nl_char_list = DataSet()
    cm_char_list = DataSet()
    nl_token_list = DataSet()
    cm_token_list = DataSet()

    add_to_set(nl_data, cm_data, "train")
    add_to_set(nl_data, cm_data, "dev")
    add_to_set(nl_data, cm_data, "test")

    nl_vocab_path = os.path.join(data_dir, "vocab%d.nl" % nl_vocab_size)
    cm_vocab_path = os.path.join(data_dir, "vocab%d.cm" % cm_vocab_size)
    nl_char_vocab_path = os.path.join(data_dir, "vocab%d.nl.char" % nl_vocab_size)
    cm_char_vocab_path = os.path.join(data_dir, "vocab%d.cm.char" % cm_vocab_size)

    nl_suffix = ".%d.nl" % nl_vocab_size
    cm_suffix = ".%d.cm" % cm_vocab_size
    nl_char_suffix = ".ids%d.nl.char" % nl_vocab_size
    cm_char_suffix = ".ids%d.cm.char" % cm_vocab_size
    nl_token_suffix = ".ids%d.nl" % nl_vocab_size
    cm_token_suffix = ".ids%d.cm" % cm_vocab_size

    _ = prepare_dataset(nl_list, data_dir, nl_suffix, nl_vocab_size, None)
    _ = prepare_dataset(cm_list, data_dir, cm_suffix, cm_vocab_size, None)
    max_nl_char_len = prepare_dataset(nl_char_list, data_dir, nl_char_suffix,
        nl_vocab_size, nl_char_vocab_path)
    max_cm_char_len = prepare_dataset(cm_char_list, data_dir, cm_char_suffix,
        cm_vocab_size, cm_char_vocab_path)
    max_nl_token_len = prepare_dataset(nl_token_list, data_dir,
                                       nl_token_suffix, nl_vocab_size,
                                       nl_vocab_path)
    max_cm_token_len = prepare_dataset(cm_token_list, data_dir,
                                       cm_token_suffix, cm_vocab_size,
                                       cm_vocab_path)

    print("maximum num chars in description = %d" % max_nl_char_len)
    print("maximum num chars in command = %d" % max_cm_char_len)
    print("maximum num tokens in description = %d" % max_nl_token_len)
    print("maximum num tokens in command = %d" % max_cm_token_len)

    compute_channel_representations(
        nl_vocab_path, nl_char_vocab_path, pad_start=True)
    compute_channel_representations(
        cm_vocab_path, cm_char_vocab_path, add_eos=True)

    nl_token_copy_suffix = ".ids%d.nl.copy" % nl_vocab_size
    prepare_dataset(nl_token_list, data_dir, nl_token_copy_suffix,
                    nl_vocab_size, nl_vocab_path, create_vocab=False,
                    parallel_vocab_size=cm_vocab_size,
                    parallel_vocab_path=cm_vocab_path,
                    parallel_data=cm_token_list)
    cm_token_copy_suffix = ".ids%d.cm.copy" % cm_vocab_size
    prepare_dataset(cm_token_list, data_dir, cm_token_copy_suffix,
                    cm_vocab_size, cm_vocab_path, create_vocab=False,
                    parallel_vocab_size=nl_vocab_size,
                    parallel_vocab_path=nl_vocab_path,
                    parallel_data=nl_token_list)

    generation_mask = np.ones(
        [FLAGS.tg_vocab_size + FLAGS.max_sc_length],
        dtype=np.float32)
    np.save(os.path.join(data_dir, "generation_mask"), generation_mask)


def prepare_bash(FLAGS, verbose=False):
    data_dir = FLAGS.data_dir
    nl_vocab_size = FLAGS.nl_vocab_size
    cm_vocab_size = FLAGS.cm_vocab_size

    def add_to_set(nl_data, cm_data, split):
        for nl, cm in zip(getattr(nl_data, split), getattr(cm_data, split)):
            ast = data_tools.bash_parser(cm)
            if ast:
                if data_tools.is_simple(ast):
                    mappings = slot_filling.slot_filler_alignment_induction(nl, cm)
                    nl_chars = data_tools.char_tokenizer(nl, tokenizer.basic_tokenizer)
                    cm_chars = data_tools.char_tokenizer(cm, data_tools.bash_tokenizer)
                    nl_tokens, _ = tokenizer.basic_tokenizer(nl)
                    cm_tokens = data_tools.ast2tokens(
                        ast, with_parent=True, with_prefix=True)
                    cm_seq = data_tools.ast2list(ast, _list=[], with_parent=True)
                    pruned_ast = normalizer.prune_ast(ast)
                    cm_pruned_tokens = data_tools.ast2tokens(
                        pruned_ast, loose_constraints=True, with_parent=True)
                    cm_pruned_seq = data_tools.ast2list(
                        pruned_ast, _list=[], with_parent=True)
                    nl_normalized_tokens, _ = tokenizer.ner_tokenizer(nl)
                    cm_normalized_tokens = data_tools.ast2tokens(
                        ast, arg_type_only=True, keep_common_args=False,
                        with_parent=True, with_prefix=True)
                    cm_normalized_seq = data_tools.ast2list(
                        ast, arg_type_only=True, keep_common_args=False,
                        _list=[], with_parent=True, with_prefix=True)
                    cm_canonical_tokens = data_tools.ast2tokens(
                        ast, arg_type_only=True, keep_common_args=False,
                        with_parent=True, ignore_flag_order=True,
                        with_prefix=True)
                    cm_canonical_seq = data_tools.ast2list(
                        ast, arg_type_only=True, keep_common_args=False,
                        _list=[], with_parent=True, ignore_flag_order=True,
                        with_prefix=True)
                    nl_partial_tokens, cm_partial_tokens = split_arguments(
                        nl_tokens, cm_tokens, cm_normalized_tokens)
                    # Debugging
                    # print(nl_partial_tokens)
                    # print(cm_partial_tokens)
                    getattr(slot_argument_mappings, split).append(mappings)
                    getattr(nl_list, split).append(nl)
                    getattr(cm_list, split).append(cm)
                    getattr(nl_char_list, split).append(nl_chars)
                    getattr(cm_char_list, split).append(cm_chars)
                    getattr(nl_token_list, split).append(nl_tokens)
                    getattr(cm_token_list, split).append(cm_tokens)
                    getattr(cm_seq_list, split).append(cm_seq)
                    getattr(cm_pruned_token_list, split).append(cm_pruned_tokens)
                    getattr(cm_pruned_seq_list, split).append(cm_pruned_seq)
                    getattr(nl_partial_token_list, split).append(nl_partial_tokens)
                    getattr(cm_partial_token_list, split).append(cm_partial_tokens)
                    getattr(nl_norm_token_list, split).append(nl_normalized_tokens)
                    getattr(cm_norm_token_list, split).append(cm_normalized_tokens)
                    getattr(cm_normalized_seq_list, split).append(cm_normalized_seq)
                    getattr(cm_canonical_token_list, split).append(cm_canonical_tokens)
                    getattr(cm_canonical_seq_list, split).append(cm_canonical_seq)
                else:
                    if verbose:
                        print("Rare command: " + cm)

    def save_slot_argument_mappings(dataset, mapping_suffix):
        for split in _data_splits:
            with open(os.path.join(FLAGS.data_dir,
                    '{}{}'.format(split, mapping_suffix)), 'w') as o_f:
                for mappings in getattr(dataset, split):
                    if mappings:
                        for i, j in sorted(mappings, key=lambda x:x[0]):
                            o_f.write('{}-{} '.format(i, j))
                    o_f.write('\n')

    def split_arguments(nl_tokens, cm_tokens, verbose=False):
        """
        Example:
            nl: find all '.txt' files
            cm: find . -name "*.txt"

            splitted_nl_tokens = ['find', 'all', "'", '.txt', "'", 'files']
            splitted_cm_tokens = ['find', '.', '-name', _ARG_START, '"', '*',
                '.txt', '"', _ARG_END]
        """

        nl_tokens_wsq = []                  # nl tokens with separated quotes
        cm_tokens_wsq = []                  # cm tokens with separated quotes
        for word in nl_tokens:
            if constants.with_quotation(word):
                nl_tokens_wsq.append(word[0])
                nl_tokens_wsq.append(word[1:-1])
                nl_tokens_wsq.append(word[-1])
            else:
                nl_tokens_wsq.append(word)
        for token in cm_tokens:
            if constants.with_quotation(token):
                if token.startswith('__FLAG__'):
                    token = token[len('__FLAG__'):]
                if token.startswith('__ARG__'):
                    token = token[len('__ARG__'):]
                cm_tokens_wsq.append(token[0])
                cm_tokens.wsq.append(token[1:-1])
                cm_tokens.wsq.append(token[-1])
            else:
                cm_tokens_wsq.append(token)

        M = collections.defaultdict(dict)
        for i in xrange(len(nl_tokens_wsq)):
            word = nl_tokens_wsq[i]
            for j in xrange(len(cm_tokens_wsq)):
                token = cm_tokens_wsq[j]
                if word == token and not constants.is_quotation(word) \
                        and constants.is_quotation(token):
                    M[i][j] = 1
                elif word in token or token in word:
                    if np.abs(len(token) - len(word)) > 10 \
                            or constants.is_quotation(word) \
                            or constants.is_quotation(token):
                        if verbose:
                            print("False match: {}, {}".format(token, word))
                        M[i][j] = -np.inf
                    else:
                        M[i][j] = (len(word) + 0.0) / len(token)
                else:
                    M[i][j] = -np.inf

        mappings, _ = slot_filling.stable_marriage_alignment(M)
        mapping_dict = dict([(y, x) for (x, y) in mappings])

        splitted_cm_tokens = []
        for j in xrange(len(cm_tokens)):
            token = cm_tokens[j]
            low_freq = is_low_frequency(token)
            if low_freq:
                basic_token = remove_low_frequency_prefix(token)
            else:
                basic_token = token
            if basic_token.startswith('__ARG__'):
                basic_token = basic_token[len('__ARG__'):]
            if j in mapping_dict:
                i = mapping_dict[j]
                word = splitted_nl_tokens[i]
                if word == basic_token:
                    splitted_cm_tokens.append(token)
                else:
                    pos_start = basic_token.index(word)
                    pos_end = pos_start + len(word)
                    splitted_cm_tokens.append(_ARG_START)
                    for k in xrange(pos_start):
                        splitted_cm_tokens.append(basic_token[k])
                    if low_freq:
                        splitted_cm_tokens.append(add_low_frequency_prefix(word))
                    else:
                        splitted_cm_tokens.append(word)
                    for k in xrange(pos_end, len(basic_token)):
                        splitted_cm_tokens.append(basic_token[k])
                    splitted_cm_tokens.append(_ARG_END)
            else:
                splitted_cm_tokens.append(token)

        return splitted_nl_tokens, splitted_cm_tokens

    # Read unfiltered data
    nl_data, cm_data = read_raw_data(data_dir)

    nl_list = DataSet()
    cm_list = DataSet()
    slot_argument_mappings = DataSet()
    nl_char_list = DataSet()
    cm_char_list = DataSet()
    nl_token_list = DataSet()
    cm_token_list = DataSet()
    cm_seq_list = DataSet()
    cm_pruned_token_list = DataSet()
    cm_pruned_seq_list = DataSet()
    nl_partial_token_list = DataSet()
    cm_partial_token_list = DataSet()
    nl_norm_token_list = DataSet()
    cm_norm_token_list = DataSet()
    cm_normalized_seq_list = DataSet()
    cm_canonical_token_list = DataSet()
    cm_canonical_seq_list = DataSet()

    add_to_set(nl_data, cm_data, "train")
    add_to_set(nl_data, cm_data, "dev")
    add_to_set(nl_data, cm_data, "test")

    # Create vocabularies of the appropriate sizes.
    nl_char_vocab_path = os.path.join(data_dir, "vocab%d.nl.char" % nl_vocab_size)
    cm_char_vocab_path = os.path.join(data_dir, "vocab%d.cm.char" % cm_vocab_size)
    nl_vocab_path = os.path.join(data_dir, "vocab%d.nl" % nl_vocab_size)
    cm_vocab_path = os.path.join(data_dir, "vocab%d.cm" % cm_vocab_size)
    nl_partial_vocab_path = os.path.join(data_dir, "vocab%d.nl.break" % nl_vocab_size)
    cm_partial_vocab_path = os.path.join(data_dir, "vocab%d.cm.break" % cm_vocab_size)
    nl_norm_vocab_path = os.path.join(data_dir, "vocab%d.nl.norm" % nl_vocab_size)
    cm_norm_vocab_path = os.path.join(data_dir, "vocab%d.cm.norm" % cm_vocab_size)
    cm_ast_vocab_path = os.path.join(data_dir, "vocab%d.cm.ast" % cm_vocab_size)
    cm_ast_norm_vocab_path = os.path.join(data_dir, "vocab%d.cm.ast.norm" % cm_vocab_size)

    nl_suffix = ".%d.nl" % nl_vocab_size
    cm_suffix = ".%d.cm" % cm_vocab_size
    nl_char_suffix = ".ids%d.nl.char" % nl_vocab_size
    cm_char_suffix = ".ids%d.cm.char" % cm_vocab_size
    nl_token_suffix = ".ids%d.nl" % nl_vocab_size
    cm_token_suffix = ".ids%d.cm" % cm_vocab_size
    nl_token_break_suffix = ".ids%d.nl.break" % nl_vocab_size
    cm_token_break_suffix = ".ids%d.cm.break" % cm_vocab_size
    nl_token_norm_suffix = ".ids%d.nl.norm" % nl_vocab_size
    cm_token_norm_suffix = ".ids%d.cm.norm" % cm_vocab_size
    cm_token_norm_order_suffix = ".ids%d.cm.norm.ordered" % cm_vocab_size
    cm_token_pruned_suffix = ".ids%d.cm.pruned" % cm_vocab_size
    cm_seq_suffix = ".seq%d.cm" % cm_vocab_size
    cm_seq_norm_suffix = ".seq%d.cm.norm" % cm_vocab_size
    cm_seq_norm_order_suffix = ".seq%d.cm.norm.ordered" % cm_vocab_size
    cm_seq_pruned_suffix = ".seq%d.cm.pruned" % cm_vocab_size

    _ = prepare_dataset(nl_list, data_dir, nl_suffix, nl_vocab_size, None)
    _ = prepare_dataset(cm_list, data_dir, cm_suffix, cm_vocab_size, None)
    max_nl_char_len = prepare_dataset(nl_char_list, data_dir, nl_char_suffix, 
        nl_vocab_size, nl_char_vocab_path)
    max_cm_char_len = prepare_dataset(cm_char_list, data_dir, cm_char_suffix, 
        cm_vocab_size, cm_char_vocab_path)
    max_nl_token_len = prepare_dataset(nl_token_list, data_dir, nl_token_suffix,
        nl_vocab_size, nl_vocab_path)
    max_cm_token_len = prepare_dataset(cm_token_list, data_dir, cm_token_suffix,
        cm_vocab_size, cm_vocab_path)
    max_nl_token_break_len = prepare_dataset(nl_partial_token_list, data_dir,
        nl_token_break_suffix, nl_vocab_size, nl_partial_vocab_path)
    max_cm_token_break_len = prepare_dataset(cm_partial_token_list, data_dir,
        cm_token_break_suffix, cm_vocab_size, cm_partial_vocab_path)
    max_nl_token_norm_len = prepare_dataset(nl_norm_token_list, data_dir,
        nl_token_norm_suffix, nl_vocab_size, nl_norm_vocab_path)
    max_cm_token_norm_len = prepare_dataset(cm_norm_token_list, data_dir,
        cm_token_norm_suffix, cm_vocab_size, cm_norm_vocab_path)
    max_cm_token_norm_order_len = prepare_dataset(cm_canonical_token_list, data_dir,
        cm_token_norm_order_suffix, cm_vocab_size, cm_norm_vocab_path)
    max_cm_token_pruned_len = prepare_dataset(cm_pruned_token_list, data_dir,
        cm_token_pruned_suffix, cm_vocab_size, cm_vocab_path)
    max_cm_seq_len = prepare_dataset(cm_seq_list, data_dir, cm_seq_suffix,
        cm_vocab_size, cm_ast_vocab_path)
    max_cm_seq_norm_len = prepare_dataset(cm_normalized_seq_list, data_dir,
        cm_seq_norm_suffix, cm_vocab_size, cm_ast_norm_vocab_path)
    max_cm_seq_norm_order_len = prepare_dataset(cm_canonical_seq_list, data_dir,
        cm_seq_norm_order_suffix, cm_vocab_size, cm_ast_norm_vocab_path)
    max_cm_seq_pruned_len = prepare_dataset(cm_pruned_seq_list, data_dir,
        cm_seq_pruned_suffix, cm_vocab_size, cm_ast_vocab_path)
    save_slot_argument_mappings(slot_argument_mappings, mapping_suffix='.mappings')
    
    print("maximum num chars in description = %d" % max_nl_char_len)
    print("maximum num chars in command = %d" % max_cm_char_len)
    print("maximum num tokens in description = %d" % max_nl_token_len)
    print("maximum num tokens in command = %d" % max_cm_token_len)
    print("maximum num AST search steps = %d" % max_cm_seq_len)
    print("maximum num tokens in splitted description = %d" %
          max_nl_token_break_len)
    print("maximum num tokens in splitted command = %d" %
          max_cm_token_break_len)
    print("maximum num tokens in normalized description = %d" %
          max_nl_token_norm_len)
    print("maximum num tokens in normalized command = %d" %
          max_cm_token_norm_len)
    print("maximum num normalized AST search steps = %d" %
          max_cm_seq_norm_len)
    print("maximum num tokens in canonical command = %d" %
          max_cm_token_norm_order_len)
    print("maximum num canonical AST search steps = %d" %
          max_cm_seq_norm_order_len)
    print("maximum num tokens in pruned command = %d" % max_cm_token_pruned_len)
    print("maximum num pruned AST search steps = %d" % max_cm_seq_pruned_len)

    # compute channel (character or other features) representations
    compute_channel_representations(
        nl_vocab_path, nl_char_vocab_path, pad_start=True)
    compute_channel_representations(
        cm_vocab_path, cm_char_vocab_path, add_eos=True)

    # compute CopyNet representations
    def prepare_generation_mask(nl_vocab_path, cm_vocab_path, output_file):
        """
        Set the generation probability of low-frequency words in the target
        vocabulary to 0.
        """
        nl_vocab, rev_nl_vocab = initialize_vocabulary(nl_vocab_path)
        cm_vocab, rev_cm_vocab = initialize_vocabulary(cm_vocab_path)
        generation_mask = np.zeros(
            [FLAGS.tg_vocab_size + FLAGS.max_sc_length],
            dtype=np.float32)
        if FLAGS.explain:
            for v in nl_vocab:
                if not v.startswith("__LF__"):
                    generation_mask[nl_vocab[v]] = 1
        else:
            for v in cm_vocab:
                if not v.startswith("__LF__"):
                    print(v, cm_vocab[v])
                    generation_mask[cm_vocab[v]] = 1
        np.save(os.path.join(data_dir, output_file), generation_mask)

    # Two types of sequence indices are prepared for CopyNet.
    #   A) '.copy.sc' - indices of source tokens in the target vocab, used to
    #       compute the copying part of the output mixture probability; if
    #       a source token is not in the target vocab, use a positional
    #       placeholder to indicate a 'copy' operation
    #   B) '.copy.tg' - indices of target tokens where low-frequency words are
    #       not replaced with _UNK iff they appeared in the source sequence
    nl_token_copy_suffix = ".ids%d.nl.copy" % nl_vocab_size
    prepare_dataset(nl_token_list, data_dir, nl_token_copy_suffix,
                    nl_vocab_size, nl_vocab_path, create_vocab=False,
                    parallel_vocab_size=cm_vocab_size,
                    parallel_vocab_path=cm_vocab_path,
                    parallel_data=cm_token_list)
    cm_token_copy_suffix = ".ids%d.cm.copy" % cm_vocab_size
    prepare_dataset(cm_token_list, data_dir, cm_token_copy_suffix,
                    cm_vocab_size, cm_vocab_path, create_vocab=False,
                    parallel_vocab_size=nl_vocab_size,
                    parallel_vocab_path=nl_vocab_path,
                    parallel_data=nl_token_list)
    prepare_generation_mask(nl_vocab_path, cm_vocab_path, "generation_mask")

    nl_token_break_copy_suffix = ".ids%d.nl.break.copy" % nl_vocab_size
    prepare_dataset(nl_partial_token_list, data_dir, nl_token_break_copy_suffix,
                    nl_vocab_size, nl_partial_vocab_path, create_vocab=False,
                    parallel_vocab_size=cm_vocab_size,
                    parallel_vocab_path=cm_vocab_path,
                    parallel_data=cm_partial_token_list)
    cm_token_break_copy_suffix = ".ids%d.cm.break.copy" % cm_vocab_size
    prepare_dataset(cm_partial_token_list, data_dir, cm_token_break_copy_suffix,
                    cm_vocab_size, cm_partial_vocab_path, create_vocab=False,
                    parallel_vocab_size=nl_vocab_size,
                    parallel_vocab_path=nl_vocab_path,
                    parallel_data=nl_partial_token_list)
    prepare_generation_mask(nl_partial_vocab_path, cm_partial_vocab_path,
                            "generation_mask.break")


def merge_vocab_for_copy(nl_vocab_path, cm_vocab_path, output_path):
    with open(nl_vocab_path) as f:
        nl_vocab = f.readlines()
    with open(cm_vocab_path) as f:
        cm_vocab = f.readlines()

    for v in cm_vocab:
        if v in nl_vocab:
            continue
        if '__LF__' + v in nl_vocab:
            continue
        if v.startswith('__LF__') and v[len('__LF__'):] in nl_vocab:
            continue
        nl_vocab.append(v)

    with open(output_path, 'w') as o_f:
        for v in nl_vocab:
            o_f.write(v)


def prepare_data(FLAGS):
    """Get data into data_dir, create vocabularies and tokenize data.

    Args:
      data: { 'train': [cm_list, nl_list],
              'dev': [cm_list, nl_list],
              'test': [cm_list, nl_list] }.
      data_dir: directory in which the data sets will be stored.
      nl_vocabulary_size: size of the English vocabulary to create and use.
      cm_vocabulary_size: size of the Command vocabulary to create and use.

    Returns:
      A tuple of 8 elements:
        (1) path to the token-ids for English training data-set,
        (2) path to the token-ids for Command training data-set,
        (3) path to the token-ids for English development data-set,
        (4) path to the token-ids for Command development data-set,
        (5) path to the token-ids for English test data-set,
        (6) path to the token-ids for Command test data-set,
        (7) path to the English vocabulary file,
        (8) path to the Command vocabulary file.
    """

    if FLAGS.dataset.startswith("bash"):
        prepare_bash(FLAGS)
    if FLAGS.dataset == "jobs":
        prepare_jobs(FLAGS)
    if FLAGS.dataset == "geo":
        prepare_jobs(FLAGS)
    if FLAGS.dataset == "atis":
        prepare_jobs(FLAGS)
    if FLAGS.dataset == "dummy":
        prepare_jobs(FLAGS)
    if FLAGS.dataset.startswith("regex"):
        prepare_jobs(FLAGS)


def load_slot_filling_data(input_path):
    data = np.load(input_path)
    train_X, train_Y = data['arr_0']

    print('{} slot filling examples loaded'.format(len(train_X)))
    return train_X, train_Y

# --- Load Datasets -- #

def bucket_grouped_data(grouped_dataset, buckets):
    batch_sc_strs = [[] for _ in buckets]
    batch_tg_strs = [[] for _ in buckets]
    batch_scs = [[] for _ in buckets]
    batch_tgs = [[] for _ in buckets]

    for sc_temp in grouped_dataset:
        sc_strs, tg_strs, scs, _ = grouped_dataset[sc_temp]

        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(buckets))
                        if buckets[b][0] > len(scs[0])])

        batch_sc_strs[bucket_id].append(sc_strs[0])
        batch_tg_strs[bucket_id].append(tg_strs)
        batch_scs[bucket_id].append(scs[0])
        batch_tgs[bucket_id].append([ROOT_ID])

    return batch_sc_strs, batch_tg_strs, batch_scs, batch_tgs


def group_data(dataset, attribute='source', use_bucket=False, use_temp=False,
               tokenizer_selector='nl'):
    """
    Group dataset by the natural language sentence.

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
        dataset = functools.reduce(lambda x,y: x + y, dataset)

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


def load_vocab(FLAGS):
    nl_ext = ".nl"
    if FLAGS.decoder_topology in ['rnn']:
        if FLAGS.normalized or FLAGS.canonical:
            nl_ext = ".nl.norm"
            cm_ext = ".cm.norm"
        elif FLAGS.partial_token:
            nl_ext = ".nl.break"
            cm_ext = ".cm.break"
        elif FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
            cm_ext = ".cm"
        else:
            cm_ext = ".cm.norm" if FLAGS.dataset.startswith('bash') \
                else '.cm'
    elif FLAGS.decoder_topology in ['basic_tree']:
        if FLAGS.normalized or FLAGS.canonical:
            cm_ext = ".cm.ast.norm"
        else:
            cm_ext = ".cm.ast"
    else:
        raise ValueError("Unrecognized decoder topology: {}.".format(
            FLAGS.decoder_topology))

    nl_vocab_path = os.path.join(FLAGS.data_dir, 'vocab{}{}'.format(
        FLAGS.nl_vocab_size, nl_ext))
    cm_vocab_path = os.path.join(FLAGS.data_dir, 'vocab{}{}'.format(
        FLAGS.cm_vocab_size, cm_ext))

    nl_vocab, rev_nl_vocab = initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = initialize_vocabulary(cm_vocab_path)

    nl_full_ext = 'vocab%d.nl' % FLAGS.nl_vocab_size
    cm_full_ext = 'vocab%d.cm' % FLAGS.cm_vocab_size
    nl_full_vocab_path = os.path.join(FLAGS.data_dir, nl_full_ext)
    cm_full_vocab_path = os.path.join(FLAGS.data_dir, cm_full_ext)
    nl_full_vocab, rev_nl_full_vocab = \
        initialize_vocabulary(nl_full_vocab_path)
    cm_full_vocab, rev_cm_full_vocab = initialize_vocabulary(
        cm_full_vocab_path)

    V = Vocab()
    if FLAGS.explain:
        V.sc_vocab, V.rev_sc_vocab = cm_vocab, rev_cm_vocab
        V.tg_vocab, V.rev_tg_vocab = nl_vocab, rev_nl_vocab
        V.sc_full_vocab, V.rev_sc_full_vocab = cm_full_vocab, rev_cm_full_vocab
        V.tg_full_vocab, V.rev_tg_full_vocab = nl_full_vocab, rev_nl_full_vocab
    else:
        V.sc_vocab, V.rev_sc_vocab = nl_vocab, rev_nl_vocab
        V.tg_vocab, V.rev_tg_vocab = cm_vocab, rev_cm_vocab
        V.sc_full_vocab, V.rev_sc_full_vocab = nl_full_vocab, rev_nl_full_vocab
        V.tg_full_vocab, V.rev_tg_full_vocab = cm_full_vocab, rev_cm_full_vocab

    if FLAGS.sc_char or FLAGS.tg_char:
        nl_char_vocab_path = os.path.join(
            FLAGS.data_dir, "vocab%d.nl.char" % FLAGS.sc_vocab_size)
        cm_char_vocab_path = os.path.join(
            FLAGS.data_dir, "vocab%d.cm.char" % FLAGS.tg_vocab_size)
        nl_char_vocab, rev_nl_char_vocab = \
            initialize_vocabulary(nl_char_vocab_path)
        cm_char_vocab, rev_cm_char_vocab = \
            initialize_vocabulary(cm_char_vocab_path)

        if FLAGS.explain:
            V.sc_char_vocab, V.rev_sc_char_vocab = cm_char_vocab, rev_cm_char_vocab
            V.tg_char_vocab, V.rev_tg_char_vocab = nl_char_vocab, rev_nl_char_vocab
        else:
            V.sc_char_vocab, V.rev_sc_char_vocab = nl_char_vocab, rev_nl_char_vocab
            V.tg_char_vocab, V.rev_tg_char_vocab = cm_char_vocab, rev_cm_char_vocab

    return V


def load_data(FLAGS, buckets=None, load_mappings=False, load_pointers=False):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = FLAGS.data_dir
    nl_vocab_size = FLAGS.nl_vocab_size
    cm_vocab_size = FLAGS.cm_vocab_size

    append_head_token = True
    append_end_token = True
    
    # Set up natural language file extensions
    nl_ext = ".nl"
    nl_full_ext = ".nl.full"
    nl_copy_sc_ext = ".nl.copy.sc"
    nl_copy_tg_ext = ".nl.copy.tg"
    if FLAGS.char:
        nl_ext = ".nl.char"
    elif FLAGS.partial_token:
        nl_ext = ".nl.break"
        nl_full_ext = ".nl.break.full"
        nl_copy_sc_ext = ".nl.break.copy.sc"
        nl_copy_tg_ext = ".nl.break.copy.tg"
    elif FLAGS.full:
        nl_ext = ".nl.full"
    elif FLAGS.normalized or FLAGS.canonical:
        nl_ext = ".nl.norm"

    # Set up command files extensions
    cm_ext = ".cm.norm" if FLAGS.dataset.startswith('bash') else '.cm'
    cm_full_ext = ".cm.full"
    cm_copy_sc_ext = ".cm.copy.sc"
    cm_copy_tg_ext = ".cm.copy.tg"
    if FLAGS.char:
        cm_ext = ".cm.char"
    elif FLAGS.partial_token:
        cm_ext = ".cm.break"
        cm_full_ext = ".cm.break.full"
        cm_copy_sc_ext = ".cm.break.copy.sc"
        cm_copy_tg_ext = ".cm.break.copy.tg"
    elif FLAGS.full:
        cm_ext = ".cm.full"
    elif FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
        cm_ext = ".cm"
    elif FLAGS.normalized:
        cm_ext = ".cm.norm"
    elif FLAGS.canonical:
        cm_ext = ".cm.norm.ordered"

    nl_ext = ".ids{}{}".format(nl_vocab_size, nl_ext)
    nl_full_ext = ".ids{}{}".format(nl_vocab_size, nl_full_ext)
    nl_copy_sc_ext = ".ids{}{}".format(nl_vocab_size, nl_copy_sc_ext)
    nl_copy_tg_ext = ".ids{}{}".format(nl_vocab_size, nl_copy_tg_ext)
    if FLAGS.decoder_topology in ["basic_tree"]:
        cm_ext = ".seq{}{}".format(cm_vocab_size, cm_ext)
        cm_full_ext = ".seq{}{}".format(cm_vocab_size, cm_full_ext)
        cm_copy_sc_ext = ".seq{}{}".format(cm_vocab_size, cm_copy_sc_ext)
        cm_copy_tg_ext = ".seq{}{}".format(cm_vocab_size, cm_copy_tg_ext)
        append_head_token = False
        append_end_token = False
    else:
        cm_ext = ".ids{}{}".format(cm_vocab_size, cm_ext)
        cm_full_ext = ".ids{}{}".format(cm_vocab_size, cm_full_ext)
        cm_copy_sc_ext = ".ids{}{}".format(cm_vocab_size, cm_copy_sc_ext)
        cm_copy_tg_ext = ".ids{}{}".format(cm_vocab_size, cm_copy_tg_ext)

    datasets = []

    for split in ["train", "dev", "test"]:
        data_path = os.path.join(data_dir, split)
        nl_txt = data_path + ".%d.nl" % FLAGS.nl_vocab_size
        cm_txt = data_path + ".%d.cm" % FLAGS.cm_vocab_size
        nl = data_path + nl_ext
        nl_full = data_path + nl_full_ext
        nl_copy_sc = data_path + nl_copy_sc_ext
        nl_copy_tg = data_path + nl_copy_tg_ext
        cm = data_path + cm_ext
        cm_full = data_path + cm_full_ext
        cm_copy_sc = data_path + cm_copy_sc_ext
        cm_copy_tg = data_path + cm_copy_tg_ext
        if FLAGS.explain:
            dataset = read_data(cm_txt, nl_txt, cm, nl, cm_full, nl_full,
                                cm_copy_sc, nl_copy_tg, FLAGS, buckets,
                                append_head_token=append_head_token,
                                append_end_token=append_end_token,
                                load_mappings=load_mappings,
                                load_pointers=load_pointers)
        else:
            dataset = read_data(nl_txt, cm_txt, nl, cm, nl_full, cm_full,
                                nl_copy_sc, cm_copy_tg, FLAGS, buckets,
                                append_head_token=append_head_token,
                                append_end_token=append_end_token,
                                load_mappings=load_mappings,
                                load_pointers=load_pointers)
        datasets.append(dataset)

    return datasets


def read_data(sc_path, tg_path, sc_id_path, tg_id_path, sc_full_id_path,
              tg_full_id_path, sc_copy_id_path, tg_copy_id_path,
              FLAGS, buckets=None, append_head_token=False,
              append_end_token=False, load_mappings=False,
              load_pointers=False):
    """
    Read preprocessed data from source and target files (grouped into buckets
    when the buckets argument is not None).

    :param sc_path: path to the file containing the original source strings.
    :param tg_path: path to the file containing the original target strings.
    :param sc_id_path: path to the file with token-ids for the source language.
    :param tg_id_path: path to the file with token-ids for the target language.
    :param sc_id_full_path: path to the file with full-vocabulary token-ids for
        the source language.
    :param tg_id_full_path: path to the file with full-vocabulary token-ids for
        the target language.
    :param sc_copy_full_id_path: path to the file with full-vocabulary token_ids
        of tokens in the source language that can be mapped to the target.
    :param buckets: bucket sizes for training.
    :param max_num_examples: maximum number of lines to read. Read complete
        data files if this entry is 0 or None.
    :param load_mappings: load the slot-filler mappings.
    :param load_pointers: load copying indices.
    """

    max_num_examples = FLAGS.max_train_data_size

    def get_target_ids(tg):
        tg_ids = [int(x) for x in tg.split()]
        if append_head_token:
            tg_ids.insert(0, ROOT_ID)
        if append_end_token:
            tg_ids.append(EOS_ID)
        return tg_ids

    if buckets:
        data_set = [[] for _ in buckets]
    else:
        data_set = []

    print("source file: {}".format(sc_path))
    print("target file: {}".format(tg_path))
    print("source token indices file: {}".format(sc_id_path))
    print("target token indices file: {}".format(tg_id_path))
    print("source full token indices file: {}".format(sc_full_id_path))
    print("target full token indices file: {}".format(tg_full_id_path))
    sc_file = tf.gfile.GFile(sc_path, mode="r")
    tg_file = tf.gfile.GFile(tg_path, mode="r")
    sc_id_file = tf.gfile.GFile(sc_id_path, mode="r")
    tg_id_file = tf.gfile.GFile(tg_id_path, mode="r")
    sc_full_id_file = tf.gfile.GFile(sc_full_id_path, mode="r")
    tg_full_id_file = tf.gfile.GFile(tg_full_id_path, mode="r")
    sc_copy_id_file = tf.gfile.GFile(sc_copy_id_path, mode="r")
    tg_copy_id_file = tf.gfile.GFile(tg_copy_id_path, mode="r")
    if load_mappings or load_pointers:
        data_dir, file_name = os.path.split(sc_path)
        mapping_path = os.path.join(
            data_dir, file_name.split('.')[0] + '.mappings')
        mapping_file = tf.gfile.GFile(mapping_path, mode="r")

    data_idx = 0
    while True:
        sc_txt, tg_txt = sc_file.readline().strip(), \
                         tg_file.readline().strip()
        sc, tg = sc_id_file.readline(), tg_id_file.readline()
        sc_full = sc_full_id_file.readline()
        tg_full = tg_full_id_file.readline()
        sc_copy = sc_copy_id_file.readline()
        tg_copy = tg_copy_id_file.readline()
        if load_mappings or load_pointers:
            mapping = mapping_file.readline()
        if not sc or not tg:
            break
        if max_num_examples and data_idx < max_num_examples:
            break

        if data_idx % 1000 == 0:
            print("  reading data line %d" % data_idx)
            sys.stdout.flush()

        dp = DataPoint()
        dp.sc_txt = sc_txt
        dp.tg_txt = tg_txt
        dp.sc_ids = [int(x) for x in sc.split()]
        dp.tg_ids = get_target_ids(tg)
        dp.sc_full_ids = [int(x) for x in sc_full.split()]
        dp.tg_full_ids = get_target_ids(tg_full)
        dp.sc_copy_ids = [int(x) for x in sc_copy.split()]
        dp.tg_copy_ids = get_target_ids(tg_copy)

        if load_mappings:
            mappings = []
            if mapping.strip():
                for mp in mapping.strip().split():
                    mappings.append([int(x) for x in mp.split('-')])
            dp.mappings = mappings
        if load_pointers:
            tg_pointers = np.zeros(
                [1, FLAGS.max_tg_length, FLAGS.max_sc_length])
            if mapping.strip():
                for mp in mapping.strip().split():
                    i, j = [int(x) for x in mp.split('-')]
                    if j < FLAGS.max_tg_length and i < FLAGS.max_sc_length:
                        tg_pointers[0, j, -(i+1)] = 1
            dp.pointer_targets = tg_pointers

        data_idx += 1
        
        if buckets:
            for bucket_id, (sc_size, tg_size) in enumerate(buckets):
                if len(dp.sc_ids) < sc_size and len(dp.tg_ids) < tg_size:
                    data_set[bucket_id].append(dp)
                    break
        else:
            data_set.append(dp)
    print("  %d data points read." % data_idx)
    return data_set


def is_low_frequency(w):
    return w.startswith('__LF__')


def add_low_frequency_prefix(w):
    return '__LF__' + w


def remove_low_frequency_prefix(w):
    if is_low_frequency(w):
        return w[len('__LF__'):]
    else:
        return w


class DataSet(object):
    def __init__(self):
        self.train = []
        self.dev = []
        self.test = []


class DataPoint(object):
    def __init__(self):
        self.sc_txt = None
        self.tg_txt = None
        self.sc_ids = None
        self.tg_ids = None
        self.sc_full_ids = None
        self.tg_full_ids = None
        self.sc_copy_ids = None
        self.tg_copy_ids = None
        self.mappings = None
        self.pointer_targets = None
        self.sc_fillers = None


class Vocab(object):
    def __init__(self):
        self.sc_vocab = None
        self.tg_vocab = None
        self.sc_full_vocab = None
        self.tg_full_vocab = None
        self.sc_char_vocab = None
        self.tg_char_vocab = None
        self.rev_sc_vocab = None
        self.rev_tg_vocab = None
        self.rev_sc_full_vocab = None
        self.rev_tg_full_vocab = None
        self.rev_sc_char_vocab = None
        self.rev_tg_char_vocab = None
