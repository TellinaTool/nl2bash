"""
Collection of data loading functions.
"""
from bunch import bunchify
import json
import os

from src.data_processor.data_utils import *


def load_data(args):
    print("Loading data from %s" % args.data_dir)
    train_set = load_data_split(args, 'train')
    dev_set = load_data_split(args, 'dev')
    test_set = load_data_split(args, 'test')
    return train_set, dev_set, test_set


def load_data_split(args, split):
    data_dir = args.data_dir
    in_json = os.path.join(data_dir, '{}.filtered.json'.format(split))
    print("input data file: {}".format(in_json))
    with open(in_json) as f:
        content = json.load(f)
        return bunchify(content)


def load_vocabulary(args):
    data_dir = args.data_dir
    source, target = ('nl', 'cm') if not args.explain else ('cm', 'nl')
    token_ext = 'normalized.{}'.format(args.channel) if args.normalized else args.channel
    vocab_ext = 'vocab.{}'.format(token_ext)

    source_vocab_path = os.path.join(data_dir, '{}.{}'.format(source, vocab_ext))
    target_vocab_path = os.path.join(data_dir, '{}.{}'.format(target, vocab_ext))

    vocab = Vocab()
    min_vocab_frequency = 1 if args.channel == 'char' else args.min_vocab_frequency
    vocab.nl_vocab, vocab.rev_nl_vocab = initialize_vocabulary(source_vocab_path, min_vocab_frequency)
    vocab.cm_vocab, vocab.rev_cm_vocab = initialize_vocabulary(target_vocab_path, min_vocab_frequency)

    max_nl_token_size = 0
    for v in vocab.nl_vocab:
        if len(v) > max_nl_token_size:
            max_nl_token_size = len(v)
    max_cm_token_size = 0
    for v in vocab.cm_vocab:
        if len(v) > max_cm_token_size:
            max_cm_token_size = len(v)
    vocab.max_nl_token_size = max_nl_token_size
    vocab.max_cm_token_size = max_cm_token_size

    print('source vocabulary size = {}'.format(len(vocab.nl_vocab)))
    print('target vocabulary size = {}'.format(len(vocab.cm_vocab)))
    print('max source token size = {}'.format(vocab.max_nl_token_size))
    print('max target token size = {}'.format(vocab.max_cm_token_size))

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
      vocab_path: path to the file containing the vocabulary
      min_frequency: frequency threshold of vocabulary

    Returns:
      a pair: the vocabulary (a dictionary mapping string to integers), and
      the reversed vocabulary (a list, which reverses the vocabulary mapping).

    Raises:
      ValueError: if the provided vocab_path does not exist.
    """
    if os.path.exists(vocab_path):
        V = []
        with open(vocab_path) as f:
            while (True):
                line = f.readline()
                if line:
                    if line.startswith('\t'):
                        v = line[0]
                        freq = line.strip()
                    else:
                        v, freq = line[:-1].rsplit('\t', 1)
                    if int(freq) >= min_frequency or bashlint.flag_suffix in v:
                        V.append(v)
                else:
                    break
        vocab = dict([(x, y) for (y, x) in enumerate(V)])
        rev_vocab = dict([(y, x) for (y, x) in enumerate(V)])
        assert (len(vocab) == len(rev_vocab))
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocab_path)


def save_data_split(data_split, out_json):
    dataset = DataSet()
    for nl_temp in data_split:
        example_group = ExampleGroup(nl_temp)
        for nl, cm in data_split[nl_temp]:
            example = Example(nl, cm)
            example_group.add_example(example)
        dataset.add_example(example_group)
    with open(out_json, 'w') as o_f:
        json.dump(dataset, o_f, indent=4, default=lambda x: x.__dict__)