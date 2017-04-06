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

"""Utilities for tokenizing & generating vocabularies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import functools
from numpy.linalg import norm
import numpy as np
import random
import os, sys

if sys.version_info > (3, 0):
    from six.moves import xrange
    import _pickle as pickle
else:
    import cPickle as pickle

from bashlex import normalizer, data_tools
from nlp_tools import constants, tokenizer, slot_filling

# Special token symbols
_PAD = "__SP__PAD"
_EOS = "__SP__EOS"
_UNK = "__SP__UNK"
_ARG_UNK = "__SP__ARGUMENT_UNK"
_UTL_UNK = "__SP__HEADCOMMAND_UNK"
_FLAG_UNK = "__SP__FLAG_UNK"

_GO = "__SP__GO"                    # seq2seq start symbol
_ROOT = "__SP__ROOT"                # seq2tree start symbol

PAD_ID = 0
EOS_ID = 1
UNK_ID = 2
ARG_ID = 3
UTL_ID = 4
FLAG_ID = 5
H_NO_EXPAND_ID = 6
V_NO_EXPAND_ID = 7
GO_ID = 8
ROOT_ID = 9

_TOKEN_START_VOCAB = [_PAD, _EOS, _UNK, _ARG_UNK, _UTL_UNK, _FLAG_UNK,
                normalizer._H_NO_EXPAND, normalizer._V_NO_EXPAND, _GO, _ROOT]

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
CGO_ID = 4

_CHAR_START_VOCAB = [_CPAD, _CEOS, _CUNK, _CATOM, _CGO]


def clean_dir(dir):
    for f_name in os.listdir(dir):
        f_path = os.path.join(dir, f_name)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception as e:
            print(e)


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
    if not tf.gfile.Exists(vocab_path):
        print("Creating vocabulary %s from data (%d)" %
              (vocab_path, len(data)))
        vocab = {}
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
        sorted_vocab = {}
        for v in vocab:
            if vocab[v] >= min_word_frequency:
                sorted_vocab[v] = vocab[v]
            else:
                # print("Infrequent token: %s"  % v)
                sorted_vocab['__LF__' + v] = vocab[v]
        sorted_vocab = sorted(sorted_vocab, key=vocab.get, reverse=True)
    else:
        print("Reading vocabulary %s from path" % vocab_path)
        vocab, _ = initialize_vocabulary(vocab_path)
        sorted_vocab = sorted(vocab, key=vocab.get)
        if append_to_vocab:
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
                    if not word in vocab:
                        sorted_vocab.append('__LF__' + word)

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
        with tf.gfile.GFile(vocab_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocab_path)


def data_to_token_ids(data, tg_id_path, vocab_path, tokenizer=None,
                      base_tokenizer=None, with_arg_types=False, use_unk=True):
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
      with_arg_types:
    """
    max_token_num = 0
    if not tf.gfile.Exists(tg_id_path):
        print("Tokenizing data (%d)" % len(data))
        vocab, _ = initialize_vocabulary(vocab_path)
        tokens_file = tf.gfile.GFile(tg_id_path, mode="w")
        counter = 0
        for line in data:
            counter += 1
            if counter % 1000 == 0:
                print("  tokenizing line %d" % counter)
            token_ids, _ = sentence_to_token_ids(line, vocab, tokenizer,
                base_tokenizer, with_arg_types, use_unk=use_unk)
            if len(token_ids) > max_token_num:
                max_token_num = len(token_ids)
            tokens_file.write(" ".join([str(tok) for tok in token_ids])
                              + "\n")
        tokens_file.close()
    return max_token_num


def sentence_to_token_ids(sentence, vocabulary, tokenizer, base_tokenizer,
                          with_arg_type=False, use_unk=True):
    """Convert a string to a list of integers representing token-ids.

    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].

    Args:
      sentence: The sentence in bytes format to convert to token-ids.
      vocabulary: A dictionary mapping tokens to integers.
      tokenizer: A function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.

      with_arg_type: If the vocabulary contains argument type (used for
      deciding which type of UNK tokens to use).
      use_unk: Set to true to replace the low-frequency tokens with UNK.

    Returns:
      a list of integers, the token-ids for the sentence.
    """
    if type(sentence) is list:
        words = sentence
        entities = None
        with_arg_type = True
    else:
        if base_tokenizer:
            words = tokenizer(sentence, base_tokenizer)
            entities = None
        else:
            words, entities = tokenizer(sentence)

    token_ids = []
    for w in words:
        if w in vocabulary:
            token_ids.append(vocabulary[w])
        else:
            # Unknown token
            if not use_unk and ('__LF__' + w) in vocabulary:
                token_ids.append(vocabulary['__LF__' + w])
            else:
                if with_arg_type:
                    kind = w.split('_')[0].lower()
                    if kind == "flag":
                        token_ids.append(FLAG_ID)
                    elif kind == "headcommand":
                        token_ids.append(UTL_ID)
                    else:
                        token_ids.append(ARG_ID)
                else:
                    token_ids.append(UNK_ID)
            if w.startswith("FLAG_"):
                print(w, sentence)

    return token_ids, entities


def token_to_char_ids(token, vocabulary):
    """
    Convert a token to a list of integers representing character-ids.
    """
    char_ids = []
    for c in token:
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


class Dataset(object):
    def __init__(self):
        self.train = []
        self.dev = []
        self.test = []


def read_raw_data(data_dir):
    nl_list = Dataset()
    cm_list = Dataset()
    for split in ['train', 'dev', 'test']:
        data_path = os.path.join(data_dir, split)
        if os.path.exists(data_path + ".nl"):
            with open(data_path + '.nl') as f:
                setattr(nl_list, split, [line.strip() for line in f.readlines()])
        if os.path.exists(data_path + ".cm"):
            with open(data_path + ".cm") as f:
                setattr(cm_list, split, [line.strip() for line in f.readlines()])
    return nl_list, cm_list


def prepare_dataset(data, data_dir, suffix, vocab_size, vocab_path):
    if isinstance(data.train[0], list):
        # save indexed token sequences
        min_word_freq = 4 \
            if ("bash" in data_dir and not ".cm" in vocab_path) else 0
        create_vocabulary(vocab_path, data.train, vocab_size,
                          min_word_frequency=min_word_freq)
        if suffix.endswith('.nl'):
            create_vocabulary(vocab_path, data.dev, vocab_size,
                    min_word_frequency=min_word_freq, append_to_vocab=True)
            create_vocabulary(vocab_path, data.test, vocab_size,
                    min_word_frequency=min_word_freq, append_to_vocab=True)
        for split in ['train', 'dev', 'test']:
            data_path = os.path.join(data_dir, split)
            data_to_token_ids(getattr(data, split), data_path + suffix,
                              vocab_path)
            if suffix.endswith('.nl') or suffix.endswith('.cm'):
                data_to_token_ids(getattr(data, split),
                                  data_path + suffix + '.full',
                                  vocab_path, use_unk=False)
    else:
        # save string data
        for split in ['train', 'dev', 'test']:
            data_path = os.path.join(data_dir, split)
            with open(data_path + suffix, 'w') as o_f:
                for line in getattr(data, split):
                    o_f.write(line.strip() + '\n')

    # compute max training sequence length to determine bucket size
    max_len = 0
    for d in data.train:
        if len(d) > max_len:
            max_len = len(d)
    return max_len


def prepare_jobs(data_dir, nl_vocab_size, cm_vocab_size):
    def add_to_set(nl_data, cm_data, split):
        for nl, cm in zip(getattr(nl_data, split), getattr(cm_data, split)):
            nl_tokens = nl.split()
            cm_tokens = cm.split()
            getattr(nl_list, split).append(nl)
            getattr(cm_list, split).append(cm)
            getattr(nl_token_list, split).append(nl_tokens)
            getattr(cm_token_list, split).append(cm_tokens)

    # unfiltered data
    nl_data, cm_data = read_raw_data(data_dir)

    nl_list = Dataset()
    cm_list = Dataset()
    nl_token_list = Dataset()
    cm_token_list = Dataset()

    add_to_set(nl_data, cm_data, "train")
    add_to_set(nl_data, cm_data, "dev")
    add_to_set(nl_data, cm_data, "test")

    nl_vocab_path = os.path.join(data_dir, "vocab%d.nl" % nl_vocab_size)
    cm_vocab_path = os.path.join(data_dir, "vocab%d.cm" % cm_vocab_size)

    nl_suffix = ".%d.nl" % nl_vocab_size
    cm_suffix = ".%d.cm" % cm_vocab_size
    nl_token_suffix = ".ids%d.nl" % nl_vocab_size
    cm_token_suffix = ".ids%d.cm" % cm_vocab_size

    _ = prepare_dataset(nl_list, data_dir, nl_suffix, nl_vocab_size, None)
    _ = prepare_dataset(cm_list, data_dir, cm_suffix, cm_vocab_size, None)
    max_nl_token_len = prepare_dataset(nl_token_list, data_dir,
                                       nl_token_suffix, nl_vocab_size,
                                       nl_vocab_path)
    max_cm_token_len = prepare_dataset(cm_token_list, data_dir,
                                       cm_token_suffix, cm_vocab_size,
                                       cm_vocab_path)

    print("maximum num tokens in description = %d" % max_nl_token_len)
    print("maximum num tokens in command = %d" % max_cm_token_len)


def prepare_bash(data_dir, nl_vocab_size, cm_vocab_size):

    def add_to_set(nl_data, cm_data, split):
        with_parent = True
        for nl, cm in zip(getattr(nl_data, split), getattr(cm_data, split)):
            ast = data_tools.bash_parser(cm)
            if ast:
                if data_tools.is_simple(ast):
                    nl_chars = data_tools.char_tokenizer(nl, tokenizer.basic_tokenizer)
                    cm_chars = data_tools.char_tokenizer(cm, data_tools.bash_tokenizer)
                    nl_tokens = tokenizer.basic_tokenizer(nl, lemmatization=False)
                    cm_tokens = data_tools.ast2tokens(ast, with_parent=with_parent)
                    cm_seq = data_tools.ast2list(ast, list=[], with_parent=with_parent)
                    pruned_ast = normalizer.prune_ast(ast)
                    cm_pruned_tokens = data_tools.ast2tokens(
                        pruned_ast, loose_constraints=True, with_parent=with_parent)
                    cm_pruned_seq = data_tools.ast2list(
                        pruned_ast, list=[], with_parent=with_parent)
                    nl_normalized_tokens, _ = tokenizer.ner_tokenizer(nl)
                    cm_normalized_tokens = data_tools.ast2tokens(
                        ast, loose_constraints=True, arg_type_only=True, with_parent=with_parent)
                    cm_normalized_seq = data_tools.ast2list(
                        ast, arg_type_only=True, list=[], with_parent=with_parent)
                    cm_canonical_tokens = data_tools.ast2tokens(
                        ast, loose_constraints=True, arg_type_only=True, ignore_flag_order=True,
                        with_parent=with_parent)
                    cm_canonical_seq = data_tools.ast2list(
                        ast, arg_type_only=True, ignore_flag_order=True, list=[],
                        with_parent=with_parent)
                    getattr(nl_list, split).append(nl)
                    getattr(cm_list, split).append(cm)
                    getattr(nl_char_list, split).append(nl_chars)
                    getattr(nl_token_list, split).append(nl_tokens)
                    getattr(cm_char_list, split).append(cm_chars)
                    getattr(cm_token_list, split).append(cm_tokens)
                    getattr(cm_seq_list, split).append(cm_seq)
                    getattr(cm_pruned_token_list, split).append(cm_pruned_tokens)
                    getattr(cm_pruned_seq_list, split).append(cm_pruned_seq)
                    getattr(nl_normalized_token_list, split).append(nl_normalized_tokens)
                    getattr(cm_normalized_token_list, split).append(cm_normalized_tokens)
                    getattr(cm_normalized_seq_list, split).append(cm_normalized_seq)
                    getattr(cm_canonical_token_list, split).append(cm_canonical_tokens)
                    getattr(cm_canonical_seq_list, split).append(cm_canonical_seq)
                else:
                    print("Rare command: " + cm)

    # unfiltered data
    nl_data, cm_data = read_raw_data(data_dir)

    nl_list = Dataset()
    cm_list = Dataset()
    nl_char_list = Dataset()
    cm_char_list = Dataset()
    nl_token_list = Dataset()
    cm_token_list = Dataset()
    cm_seq_list = Dataset()
    cm_pruned_token_list = Dataset()
    cm_pruned_seq_list = Dataset()
    nl_normalized_token_list = Dataset()
    cm_normalized_token_list = Dataset()
    cm_normalized_seq_list = Dataset()
    cm_canonical_token_list = Dataset()
    cm_canonical_seq_list = Dataset()

    add_to_set(nl_data, cm_data, "train")
    add_to_set(nl_data, cm_data, "dev")
    add_to_set(nl_data, cm_data, "test")

    # Create vocabularies of the appropriate sizes.
    nl_char_vocab_path = os.path.join(data_dir, "vocab%d.nl.char" % nl_vocab_size)
    cm_char_vocab_path = os.path.join(data_dir, "vocab%d.cm.char" % cm_vocab_size)
    nl_vocab_path = os.path.join(data_dir, "vocab%d.nl" % nl_vocab_size)
    cm_vocab_path = os.path.join(data_dir, "vocab%d.cm" % cm_vocab_size)
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
    nl_token_norm_suffix = ".ids%d.nl.norm" % nl_vocab_size
    cm_token_norm_suffix = ".ids%d.cm.norm" % cm_vocab_size
    cm_token_norm_order_suffix = ".ids%d.cm.norm.order" % cm_vocab_size
    cm_token_pruned_suffix = ".ids%d.cm.pruned" % cm_vocab_size
    cm_seq_suffix = ".seq%d.cm" % cm_vocab_size
    cm_seq_norm_suffix = ".seq%d.cm.norm" % cm_vocab_size
    cm_seq_norm_order_suffix = ".seq%d.cm.norm.order" % cm_vocab_size
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
    max_nl_token_norm_len = prepare_dataset(nl_normalized_token_list, data_dir,
        nl_token_norm_suffix, nl_vocab_size, nl_norm_vocab_path)
    max_cm_token_norm_len = prepare_dataset(cm_normalized_token_list, data_dir,
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

    print("maximum num chars in description = %d" % max_nl_char_len)
    print("maximum num tokens in description = %d" % max_nl_token_len)
    print("maximum num chars in command = %d" % max_cm_char_len)
    print("maximum num tokens in command = %d" % max_cm_token_len)
    print("maximum num AST search steps = %d" % max_cm_seq_len)
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

    # compute character representation of tokens
    nl_vocab, _ = initialize_vocabulary(nl_vocab_path)
    nl_char_vocab, _ = initialize_vocabulary(nl_char_vocab_path)
    nl_decomposed_vocab_path = os.path.join(data_dir,
                            "vocab%d.nl.char.decompose" % nl_vocab_size)
    max_nl_token_size = 0
    char_ids_list = []
    with open(nl_decomposed_vocab_path, 'w') as o_f:
        for token, _ in sorted(nl_vocab.items(), key=lambda x:x[1]):
            if token.startswith("__SP__"):
                # special tokens are non-decomposable
                char_ids = [CATOM_ID]
            else:
                if token.startswith("__LF__"):
                    # remove prefix for low-frequency words
                    char_ids = token_to_char_ids(token[6:], nl_char_vocab)
                else:
                    char_ids = token_to_char_ids(token, nl_char_vocab)
                if len(char_ids) > max_nl_token_size:
                    max_nl_token_size = len(char_ids)
            char_ids_list.append(char_ids)
            o_f.write(' '.join([str(c_id) for c_id in char_ids]) + '\n')
    print("maximum token size in description = %d" % max_nl_token_size)

    nl_token_char_indices = np.zeros([len(nl_vocab), max_nl_token_size])
    for token_id in xrange(len(char_ids_list)):
        char_ids = char_ids_list[token_id]
        # padding character indices
        padded_char_ids = [CPAD_ID] * (max_nl_token_size - len(char_ids)) \
            + char_ids
        for j in xrange(len(padded_char_ids)):
            nl_token_char_indices[token_id][j] = c_id
    np.save(nl_decomposed_vocab_path, nl_token_char_indices)


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
        prepare_bash(FLAGS.data_dir, FLAGS.sc_vocab_size, FLAGS.sc_vocab_size)
    if FLAGS.dataset == "jobs":
        prepare_jobs(FLAGS.data_dir, FLAGS.sc_vocab_size, FLAGS.sc_vocab_size)
    if FLAGS.dataset == "geo":
        prepare_jobs(FLAGS.data_dir, FLAGS.sc_vocab_size, FLAGS.sc_vocab_size)
    if FLAGS.dataset == "atis":
        prepare_jobs(FLAGS.data_dir, FLAGS.sc_vocab_size, FLAGS.sc_vocab_size)
    if FLAGS.dataset == "dummy":
        prepare_jobs(FLAGS.data_dir, FLAGS.sc_vocab_size, FLAGS.sc_vocab_size)


def slot_filling_mapping_induction(FLAGS):
    """Induce the filler-slot alignments on train/dev/test dataset."""
    data_dir = FLAGS.data_dir
    nl_vocab_size = FLAGS.sc_vocab_size
    cm_vocab_size = FLAGS.tg_vocab_size

    for dataset in ['train', 'dev', 'test']:
        nl_path = os.path.join(data_dir, '{}.{}.nl'
                               .format(dataset, nl_vocab_size))
        cm_path = os.path.join(data_dir, '{}.{}.cm'
                               .format(dataset, cm_vocab_size))
        nl_list = [nl.strip() for nl in open(nl_path, 'r').readlines()]
        cm_list = [cm.strip() for cm in open(cm_path, 'r').readlines()]

        assert(len(nl_list) == len(cm_list))

        with open(os.path.join(data_dir,
                '{}.{}.mappings'.format(dataset, nl_vocab_size)), 'w') as o_f:
            for nl, cm in zip(nl_list, cm_list):
                mappings = \
                    slot_filling.slot_filler_alignment_induction(nl, cm)
                if mappings:
                    for i, j in sorted(mappings, key=lambda x:x[0]):
                        o_f.write('{}-{} '.format(i, j))
                o_f.write('\n')

def load_slot_filling_data(data_dir):
    with open(data_dir, 'rb') as f:
        if sys.version_info > (3, 0):
            train_X, train_Y = pickle.load(f, encoding='latin-1')
        else:
            train_X, train_Y = pickle.load(f)
        train_X = np.concatenate(train_X, axis=0)
        train_Y = np.concatenate([np.expand_dims(y, 0) for y in train_Y],
                                 axis=0)
        # print(train_X[0][:40])
        # normalize the rows of the feature matrices
        train_X = train_X / norm(train_X, axis=1)[:, None]
        # print(train_X[0][:40])
        assert(len(train_X) == len(train_Y))
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


def group_data_by_nl(dataset, use_bucket=False, use_temp=True):
    """
    Group dataset by the natural language sentence.

    :param dataset: a list of training quadruples (nl_str, cm_str, nl, cm)
    :param bucket_input: if the input is grouped in buckets
    :param use_temp: set to true if the dataset is to be grouped by the natural
        language template; false if the dataset is to be grouped by the natural
        language strings.

    :return: a dictionary with natural language sentence as the key and data
        list quadruples as the values.
    """
    if use_bucket:
        dataset = functools.reduce(lambda x,y: x + y, dataset)

    grouped_dataset = {}
    for i in xrange(len(dataset)):
        nl_str, cm_str, nl, cm = dataset[i]
        if use_temp:
            words, _ = tokenizer.ner_tokenizer(nl_str)
            nl_template = " ".join(words)
        else:
            nl_template = nl_str
        if nl_template in grouped_dataset:
            grouped_dataset[nl_template][0].append(nl_str)
            grouped_dataset[nl_template][1].append(cm_str)
            grouped_dataset[nl_template][2].append(nl)
            grouped_dataset[nl_template][3].append(cm)
        else:
            grouped_dataset[nl_template] = [[nl_str], [cm_str], [nl], [cm]]

    return grouped_dataset


def group_data_by_cm(dataset, use_bucket=False, use_temp=True):
    if use_bucket:
        dataset = functools.reduce(lambda x,y: x + y, dataset)
    grouped_dataset = {}
    for i in xrange(len(dataset)):
        nl_str, cm_str, nl, cm = dataset[i]
        if use_temp:
            cm_template = data_tools.cmd2template(cm_str)
        else:
            cm_template = cm_str
        if cm_template in grouped_dataset:
            grouped_dataset[cm_template][0].append(cm_str)
            grouped_dataset[cm_template][1].append(nl_str)
            grouped_dataset[cm_template][2].append(cm)
            grouped_dataset[cm_template][3].append(nl)
        else:
            grouped_dataset[cm_template] = [[nl_str], [cm_str], [cm], [nl]]

    return grouped_dataset


def load_vocab(FLAGS):
    if FLAGS.decoder_topology in ['rnn']:
        nl_vocab_path = os.path.join(
            FLAGS.data_dir, "vocab%d.nl" % FLAGS.sc_vocab_size)
        if FLAGS.canonical:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm.norm" % FLAGS.sc_vocab_size)
        elif FLAGS.normalized:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm.norm" % FLAGS.sc_vocab_size)
        else:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm" % FLAGS.sc_vocab_size)
    elif FLAGS.decoder_topology in ['basic_tree']:
        nl_vocab_path = os.path.join(
            FLAGS.data_dir, "vocab%d.nl" % FLAGS.sc_vocab_size)
        if FLAGS.canonical:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm.ast.norm" % FLAGS.sc_vocab_size)
        elif FLAGS.normalized:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm.ast.norm" % FLAGS.sc_vocab_size)
        else:
            cm_vocab_path = os.path.join(
                FLAGS.data_dir, "vocab%d.cm.ast" % FLAGS.sc_vocab_size)
    else:
        raise ValueError("Unrecognized decoder topology: {}."
                         .format(FLAGS.decoder_topology))

    nl_vocab, rev_nl_vocab = initialize_vocabulary(nl_vocab_path)
    cm_vocab, rev_cm_vocab = initialize_vocabulary(cm_vocab_path)

    if FLAGS.explain:
        return cm_vocab, rev_cm_vocab, nl_vocab, rev_nl_vocab
    else:
        return nl_vocab, rev_nl_vocab, cm_vocab, rev_cm_vocab


def load_data(FLAGS, buckets=None, load_mappings=False):
    print("Loading data from %s" % FLAGS.data_dir)

    data_dir = FLAGS.data_dir

    if FLAGS.char:
        nl_extension = ".ids%d.nl.char" % FLAGS.sc_vocab_size
        cm_extension = ".ids%d.cm.char" % FLAGS.sc_vocab_size
        append_head_token = True
        append_end_token = True
    elif FLAGS.decoder_topology in ["rnn"]:
        nl_extension = ".ids%d.nl" % FLAGS.sc_vocab_size
        if FLAGS.canonical:
            cm_extension = ".ids%d.cm.norm.order" % FLAGS.sc_vocab_size
        elif FLAGS.normalized:
            cm_extension = ".ids%d.cm.norm" % FLAGS.sc_vocab_size
        else:
            cm_extension = ".ids%d.cm" % FLAGS.sc_vocab_size
        append_head_token = True
        append_end_token = True
    elif FLAGS.decoder_topology in ["basic_tree"]:
        nl_extension = ".ids%d.nl" % FLAGS.sc_vocab_size
        if FLAGS.canonical:
            cm_extension = ".seq%d.cm.norm.order" % FLAGS.sc_vocab_size
        elif FLAGS.normalized:
            cm_extension = ".seq%d.cm.norm" % FLAGS.sc_vocab_size
        else:
            cm_extension = ".seq%d.cm" % FLAGS.sc_vocab_size
        append_head_token = False
        append_end_token = False
    
    train_path = os.path.join(data_dir, "train")
    dev_path = os.path.join(data_dir, "dev")
    test_path = os.path.join(data_dir, "test")

    nl_txt_train = train_path + ".%d.nl" % FLAGS.sc_vocab_size
    cm_txt_train = train_path + ".%d.cm" % FLAGS.sc_vocab_size
    nl_txt_dev = dev_path + ".%d.nl" % FLAGS.sc_vocab_size
    cm_txt_dev = dev_path + ".%d.cm" % FLAGS.sc_vocab_size
    nl_txt_test = test_path + ".%d.nl" % FLAGS.sc_vocab_size
    cm_txt_test = test_path + ".%d.cm" % FLAGS.sc_vocab_size

    nl_train = train_path + nl_extension
    cm_train = train_path + cm_extension
    nl_dev = dev_path + nl_extension
    cm_dev = dev_path + cm_extension
    nl_test = test_path + nl_extension
    cm_test = test_path + cm_extension

    if FLAGS.explain:
        train_set = read_data(cm_txt_train, nl_txt_train, cm_train, nl_train,
                            buckets, FLAGS.max_train_data_size,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
        dev_set = read_data(cm_txt_dev, nl_txt_dev, cm_dev, nl_dev, buckets,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
        test_set = read_data(cm_txt_test, nl_txt_test, cm_test, nl_test, buckets,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
    else:
        train_set = read_data(nl_txt_train, cm_txt_train, nl_train, cm_train,
                            buckets, FLAGS.max_train_data_size,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
        dev_set = read_data(nl_txt_dev, cm_txt_dev, nl_dev, cm_dev, buckets,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
        test_set = read_data(nl_txt_test, cm_txt_test, nl_test, cm_test, buckets,
                            append_head_token=append_head_token,
                            append_end_token=append_end_token,
                            load_mappings=load_mappings)
    
    return train_set, dev_set, test_set


def read_data(sc_path, tg_path, sc_id_path, tg_id_path,
              buckets=None, max_num_examples=None,
              append_head_token=False, append_end_token=False,
              load_mappings=False):
    """Read preprocessed data from source and target files and put into buckets.
    :param sc_path: path to the file containing the original source
    strings.
    :param tg_path: path to the file containing the original target
    strings.
    :param sc_id_path: path to the file with token-ids for the source language.
    :param tg_id_path: path to the file with token-ids for the target language.
    :param buckets: bucket sizes for training.
    :param max_num_examples: maximum number of lines to read. Read complete
           data files if this entry is 0 or None.
    :param load_mappings: load the slot-filler mappings
    """
    if buckets:
        data_set = [[] for _ in buckets]
    else:
        data_set = []

    sc_file = tf.gfile.GFile(sc_path, mode="r")
    tg_file = tf.gfile.GFile(tg_path, mode="r")
    sc_id_file = tf.gfile.GFile(sc_id_path, mode="r")
    tg_id_file = tf.gfile.GFile(tg_id_path, mode="r")
    if load_mappings:
        mapping_path = '.'.join(sc_path.rsplit('.')[:-1]) + '.mappings'
        mapping_file = tf.gfile.GFile(mapping_path, mode="r")
    
    counter = 0
    while True:
        sc_txt, tg_txt = sc_file.readline(), tg_file.readline()
        sc, tg = sc_id_file.readline(), tg_id_file.readline()
        if load_mappings:
            mapping = mapping_file.readline()
        if not sc or not tg:
            break
        if max_num_examples and counter < max_num_examples:
            break

        counter += 1
        if counter % 1000 == 0:
            print("  reading data line %d" % counter)
            sys.stdout.flush()

        sc_ids = [int(x) for x in sc.split()]
        tg_ids = [int(x) for x in tg.split()]
        if append_head_token:
            tg_ids.insert(0, ROOT_ID)
        if append_end_token:
            tg_ids.append(EOS_ID)
        if load_mappings:
            mappings = []
            if mapping.strip():
                for mp in mapping.strip().split():
                    mappings.append([int(x) for x in mp.split('-')])
            data_point = [sc_txt, tg_txt, sc_ids, tg_ids, mappings]
        else:
            data_point = [sc_txt, tg_txt, sc_ids, tg_ids]

        if buckets:
            for bucket_id, (sc_size, tg_size) in enumerate(buckets):
                if len(sc_ids) < sc_size and len(tg_ids) < tg_size:
                    data_set[bucket_id].append(data_point)
                    break
        else:
            data_set.append(data_point)

    print("  %d data points read." % counter)
    return data_set
