"""
Collection of data loading functions.
"""
import os
import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import bashlint
from data_processor.data_utils import *


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
        token_ext = 'normalized.{}'.format(FLAGS.channel) if FLAGS.normalized else FLAGS.channel
        sc_token_path = get_data_file_path(data_dir, split, source, token_ext)
        tg_token_path = get_data_file_path(data_dir, split, target, token_ext)
        print("source tokenized sequence file: {}".format(sc_token_path))
        print("target tokenized sequence file: {}".format(tg_token_path))
        sc_token_file = open(sc_token_path, encoding='utf-8')
        tg_token_file = open(tg_token_path, encoding='utf-8')
        align_file = os.path.join(data_dir, '{}.{}.align'.format(split, FLAGS.channel))
        alignments = load_pair_alignment(align_file)

    dataset = []
    num_data = 0
    max_sc_length = 0
    max_tg_length = 0

    for i, source in enumerate(sc_file.readlines()):
        example = Example()
        example.source = source.strip()
        example.target = tg_file.readline().strip()
        if load_features:
            example.sc_ids = get_source_ids(sc_token_file.readline().strip())
            if len(example.sc_ids) > max_sc_length:
                max_sc_length = len(example.sc_ids)
            example.tg_ids = get_target_input_ids(tg_token_file.readline().strip())
            example.alignments = alignments[i]
            if len(example.tg_ids) > max_tg_length:
                max_tg_length = len(example.tg_ids)
        dataset.append(example)
        num_data += 1
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
            sc_copy_token_path = get_data_file_path(data_dir, split, source, copy_token_ext)
            tg_copy_token_path = get_data_file_path(data_dir, split, target, copy_token_ext)
            sc_token_file = open(sc_token_path, encoding='utf-8')
            tg_token_file = open(tg_token_path, encoding='utf-8')
            sc_copy_token_file = open(sc_copy_token_path, encoding='utf-8')
            tg_copy_token_file = open(tg_copy_token_path, encoding='utf-8')
            for i, example in enumerate(dataset):
                sc_tokens = sc_token_file.readline().strip().split(TOKEN_SEPARATOR)
                tg_tokens = tg_token_file.readline().strip().split(TOKEN_SEPARATOR)
                sc_copy_tokens = sc_copy_token_file.readline().strip().split(TOKEN_SEPARATOR)
                tg_copy_tokens = tg_copy_token_file.readline().strip().split(TOKEN_SEPARATOR)
                example.csc_ids, example.ctg_ids = compute_copy_indices(
                    sc_tokens, tg_tokens, sc_copy_tokens, tg_copy_tokens, vocab.tg_vocab, token_ext)
            sc_token_file.close()
            tg_token_file.close()
            sc_copy_token_file.close()
            tg_copy_token_file.close()

    if load_features and use_buckets and split == 'train':
        print('Group data points into buckets...')
        # Determine bucket sizes based on the characteristics of the dataset
        num_buckets = FLAGS.num_buckets
        bucket_capacity = int(len(dataset) / num_buckets)
        assert (bucket_capacity > 0)
        # Excluding outliers (very long sequences)
        length_cutoff = 0.01
        # A. Determine maximum source length
        sorted_dataset = sorted(dataset, key=lambda x: len(x.sc_ids), reverse=True)
        max_sc_length = len(sorted_dataset[int(len(sorted_dataset) * length_cutoff)].sc_ids)
        # B. Determine maximum target length
        sorted_dataset = sorted(dataset, key=lambda x: len(x.tg_ids), reverse=True)
        max_tg_length = len(sorted_dataset[int(len(sorted_dataset) * length_cutoff)].tg_ids)
        print('max_source_length after filtering = {}'.format(max_sc_length))
        print('max_target_length after filtering = {}'.format(max_tg_length))
        # Determine thresholds for buckets of equal capacity
        buckets = []
        sorted_dataset = sorted(dataset, key=lambda x: len(x.sc_ids), reverse=False)
        max_tg_len_so_far = 0
        for i, dp in enumerate(sorted_dataset):
            if len(dp.sc_ids) > max_sc_length:
                break
            if len(dp.tg_ids) > max_tg_len_so_far:
                max_tg_len_so_far = len(dp.tg_ids)
            if i > 0 and i % bucket_capacity == 0:
                buckets.append((len(dp.sc_ids) + 1, min(max_tg_len_so_far, max_tg_length) + 1))
        if len(buckets) == 0 or buckets[-1][0] < max(max_sc_length, max_tg_length):
            buckets.append((max_sc_length + 1, min(max_tg_len_so_far, max_tg_length) + 1))

        dataset2 = [[] for _ in buckets]
        for i, example in enumerate(dataset):
            example = dataset[i]
            # Compute bucket id
            bucket_ids = [b for b in xrange(len(buckets))
                          if buckets[b][0] > len(example.sc_ids) and buckets[b][1] > len(example.tg_ids)]
            if bucket_ids:
                bucket_id = min(bucket_ids)
                dataset2[bucket_id].append(example)
            else:
                if split != 'train':
                    bucket_id = len(buckets) - 1
                    dataset2[bucket_id].append(example)
        dataset = dataset2

    D = DataSet(dataset)
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