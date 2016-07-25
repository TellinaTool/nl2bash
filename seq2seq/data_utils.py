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
# ==============================================================================

"""Utilities for tokenizing & generating vocabularies."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import bashlex

from tensorflow.python.platform import gfile

# Special vocabulary symbols - we always put them at the start.
_PAD = b"_PAD"
_GO = b"_GO"
_EOS = b"_EOS"
_UNK = b"_UNK"
_NUM = b"_NUM"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<|\'|\"|\`]|[\)|\]|\}|\>|\'|\"|\`]$")
# _WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_DIGIT_RE = re.compile(br"\d")


def basic_tokenizer(sentence, normalize_digits=True):
    """Very basic tokenizer: split the sentence into a list of tokens."""
    words = []
    for space_separated_fragment in sentence.replace('\n', ' ').strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    normalized_words = []
    for i in xrange(len(words)):
        w = words[i].lower() if i == 0 else words[i]
        word = re.sub(_DIGIT_RE, _NUM, w) if normalize_digits and not w.startswith('-') else w
        normalized_words.append(word)
    return normalized_words


def bash_tokenizer(cmd, normalize_digits=True):
    cmd = cmd.replace('\n', ' ').strip()
    tokens = []

    def parse(node, tokens):
        if node.kind == "word":
            w = node.word
            word = re.sub(_DIGIT_RE, _NUM, w) if normalize_digits and not w.startswith('-') else w
            tokens.append(word)
        else:
            if hasattr(node, 'parts'):
                for child in node.parts:
                    parse(child, tokens)
    try:
        parts = bashlex.parse(cmd)
    except bashlex.tokenizer.MatchedPairError, e:
        return basic_tokenizer(cmd, normalize_digits)
    except bashlex.errors.ParsingError, e:
        return basic_tokenizer(cmd, normalize_digits)
    except NotImplementedError, e:
        return basic_tokenizer(cmd, normalize_digits)

    for part in parts:
        parse(part, tokens)

    return tokens

def create_vocabulary(vocabulary_path, data, max_vocabulary_size,
                      tokenizer, normalize_digits=True):
    """Create vocabulary file (if it does not exist yet) from data file.

    Data file is assumed to contain one sentence per line. Each sentence is
    tokenized and digits are normalized (if normalize_digits is set).
    Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
    We write it to vocabulary_path in a one-token-per-line format, so that later
    token in the first line gets id=0, second line gets id=1, and so on.

    Args:
      vocabulary_path: path where the vocabulary will be created.
      data: list of lines each of which corresponds to a data point.
      max_vocabulary_size: limit on the size of the created vocabulary.
      tokenizer: a function to use to tokenize each data sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(vocabulary_path):
        print("Creating vocabulary %s from data (%d)" % (vocabulary_path, len(data)))
        vocab = {}
        counter = 0
        for line in data:
            counter += 1
            if counter % 1000 == 0:
                print("  processing line %d" % counter)
            tokens = tokenizer(line, normalize_digits)
            for word in tokens:
                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1
                str += w + ' '
            print(str)
        vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
        if len(vocab_list) > max_vocabulary_size:
            vocab_list = vocab_list[:max_vocabulary_size]
        with gfile.GFile(vocabulary_path, mode="wb") as vocab_file:
            for w in vocab_list:
                vocab_file.write(w.encode('utf-8') + b"\n")


def initialize_vocabulary(vocabulary_path):
    """Initialize vocabulary from file.

    We assume the vocabulary is stored one-item-per-line, so a file:
      dog
      cat
    will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
    also return the reversed-vocabulary ["dog", "cat"].

    Args:
      vocabulary_path: path to the file containing the vocabulary.

    Returns:
      a pair: the vocabulary (a dictionary mapping string to integers), and
      the reversed vocabulary (a list, which reverses the vocabulary mapping).

    Raises:
      ValueError: if the provided vocabulary_path does not exist.
    """
    if gfile.Exists(vocabulary_path):
        rev_vocab = []
        with gfile.GFile(vocabulary_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_path)


def sentence_to_token_ids(sentence, vocabulary,
                          tokenizer, normalize_digits=True):
    """Convert a string to list of integers representing token-ids.

    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].

    Args:
      sentence: the sentence in bytes format to convert to token-ids.
      vocabulary: a dictionary mapping tokens to integers.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.

    Returns:
      a list of integers, the token-ids for the sentence.
    """

    words = tokenizer(sentence, normalize_digits)

    if not normalize_digits:
        return [vocabulary.get(w, UNK_ID) for w in words]
    # Normalize digits by 0 before looking words up in the vocabulary.
    return [vocabulary.get(re.sub(_DIGIT_RE, b"0", w), UNK_ID) for w in words]


def data_to_token_ids(data, target_path, vocabulary_path,
                      tokenizer, normalize_digits=True):
    """Tokenize data file and turn into token-ids using given vocabulary file.

    This function loads data line-by-line from data_path, calls the above
    sentence_to_token_ids, and saves the result to target_path. See comment
    for sentence_to_token_ids on the details of token-ids format.

    Args:
      data: list of lines each of which corresponds to a data point.
      target_path: path where the file with token-ids will be created.
      vocabulary_path: path to the vocabulary file.
      tokenizer: a function to use to tokenize each sentence;
        if None, basic_tokenizer will be used.
      normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(target_path):
        print("Tokenizing data (%d)" % len(data))
        vocab, _ = initialize_vocabulary(vocabulary_path)
        with gfile.GFile(target_path, mode="w") as tokens_file:
            counter = 0
            for line in data:
                counter += 1
                if counter % 1000 == 0:
                    print("  tokenizing line %d" % counter)
                token_ids = sentence_to_token_ids(line, vocab, tokenizer,
                                                  normalize_digits)
                tokens_file.write(" ".join([str(tok) for tok in token_ids]) + "\n")


def prepare_data(data, data_dir, nl_vocabulary_size, cm_vocabulary_size,
                 tokenizers=(basic_tokenizer, bash_tokenizer)):
    """Get data into data_dir, create vocabularies and tokenize data.

    Args:
      data: { 'train': [cm_list, nl_list],
              'dev': [cm_list, nl_list],
              'test': [cm_list, nl_list] }.
      data_dir: directory in which the data sets will be stored.
      nl_vocabulary_size: size of the English vocabulary to create and use.
      cm_vocabulary_size: size of the Command vocabulary to create and use.
      tokenizers: two functions - one to tokenize each English sentence and one to tokenize each bash command;
        if None, basic_tokenizer and bash_tokenizer will be used.

    Returns:
      A tuple of 6 elements:
        (1) path to the token-ids for English training data-set,
        (2) path to the token-ids for Command training data-set,
        (3) path to the token-ids for English development data-set,
        (4) path to the token-ids for Command development data-set,
        (5) path to the English vocabulary file,
        (6) path to the Command vocabulary file.
    """

    train_cm_list = data['train'][0]
    train_nl_list = data['train'][1]
    dev_cm_list = data['dev'][0]
    dev_nl_list = data['dev'][1]
    test_cm_list = data['test'][0]
    test_nl_list = data['test'][1]

    # Get data to the specified directory.
    train_path = data_dir + "/train"
    dev_path = data_dir + "/dev"
    test_path = data_dir + "/test"

    # Create vocabularies of the appropriate sizes.
    cm_vocab_path = os.path.join(data_dir, "vocab%d.cm" % cm_vocabulary_size)
    nl_vocab_path = os.path.join(data_dir, "vocab%d.nl" % nl_vocabulary_size)
    create_vocabulary(cm_vocab_path, train_cm_list, cm_vocabulary_size, tokenizers[1], True)
    create_vocabulary(nl_vocab_path, train_nl_list, nl_vocabulary_size, tokenizers[0], True)

    # Create token ids for the training data.
    cm_train_ids_path = train_path + (".ids%d.cm" % cm_vocabulary_size)
    nl_train_ids_path = train_path + (".ids%d.nl" % nl_vocabulary_size)
    data_to_token_ids(train_cm_list, cm_train_ids_path, cm_vocab_path, tokenizers[1])
    data_to_token_ids(train_nl_list, nl_train_ids_path, nl_vocab_path, tokenizers[0])

    # Create token ids for the development data.
    cm_dev_ids_path = dev_path + (".ids%d.cm" % cm_vocabulary_size)
    nl_dev_ids_path = dev_path + (".ids%d.nl" % nl_vocabulary_size)
    data_to_token_ids(dev_cm_list, cm_dev_ids_path, cm_vocab_path, tokenizers[1])
    data_to_token_ids(dev_nl_list, nl_dev_ids_path, nl_vocab_path, tokenizers[0])

    # Create token ids for the test data
    cm_test_ids_path = test_path + (".ids%d.cm" % cm_vocabulary_size)
    nl_test_ids_path = test_path + (".ids%d.nl" % nl_vocabulary_size)
    data_to_token_ids(test_cm_list, cm_test_ids_path, cm_vocab_path, tokenizers[1])
    data_to_token_ids(test_nl_list, nl_test_ids_path, nl_vocab_path, tokenizers[0])

    return (nl_train_ids_path, cm_train_ids_path,
            nl_dev_ids_path, cm_dev_ids_path,
            nl_test_ids_path, cm_test_ids_path,
            nl_vocab_path, cm_vocab_path)
