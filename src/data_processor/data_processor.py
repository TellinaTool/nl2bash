"""
Collection of data processing functions.
"""
import collections
import os

import src.data_processor.data_utils as data_utils
from src.data_processor.data_loader import initialize_vocabulary, load_data_split, save_data_split
from src.data_processor.tokenizers import parallel_data_to_chars
from src.data_processor.tokenizers import parallel_data_to_partial_tokens
from src.data_processor.tokenizers import parallel_data_to_tokens
from src.data_processor.tokenizers import parallel_data_to_normalized_tokens
from src.data_processor.vectorizers import vectorize_data
from src.data_processor.vectorizers import vectorize_data_copy


def process_data(FLAGS):
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
    process_dataset_split(data_dir, 'train', channel=channel)
    process_dataset_split(data_dir, 'dev', channel=channel)
    process_dataset_split(data_dir, 'test', channel=channel)


def process_dataset_split(data_dir, split, channel=''):
    """
    Process a specific dataset split.
    """
    print("Split - {}".format(split))
    in_json = os.path.join(data_dir, '{}.filtered.json'.format(split))
    dataset = load_data_split(in_json)
    # character based processing
    if not channel or channel == 'char':
        prepare_channel(data_dir, dataset, split, channel='char',
                        tokenize_data=parallel_data_to_chars)
    # partial-token based processing
    if not channel or channel == 'partial.token':
        prepare_channel(data_dir, dataset, split, channel='partial.token',
                        tokenize_data=parallel_data_to_partial_tokens)
    # token based processing
    if not channel or channel == 'token':
        prepare_channel(data_dir, dataset, split, channel='token',
                        tokenize_data=parallel_data_to_tokens)
    # normalized token based processing
    if not channel or channel == 'normalized.token':
        prepare_channel(data_dir, dataset, split, channel='normalized.token',
                        tokenize_data=parallel_data_to_normalized_tokens)
    out_json = os.path.join(data_dir, '{}.filtered.features.json')
    save_data_split(dataset, out_json)


def prepare_channel(data_dir, dataset, split, channel, tokenize_data):
    print("    channel - {}".format(channel))
    # Tokenize data
    nl_tokens, cm_tokens = tokenize_data(dataset)

    # Create or load vocabulary
    nl_vocab_path = os.path.join(data_dir, 'nl.vocab.{}'.format(channel))
    cm_vocab_path = os.path.join(data_dir, 'cm.vocab.{}'.format(channel))
    nl_vocab = create_vocabulary(nl_vocab_path, nl_tokens) \
        if split == 'train' else initialize_vocabulary(nl_vocab_path)[0]
    cm_vocab = create_vocabulary(cm_vocab_path, cm_tokens) \
        if split == 'train' else initialize_vocabulary(cm_vocab_path)[0]

    # Vectorize data
    vectorize_data(dataset, channel, nl_vocab, cm_vocab)

    # For copying
    if channel in ['token', 'char', 'partial.token']:
        vectorize_data_copy(dataset, channel, cm_vocab)


def create_vocabulary(vocab_path, dataset, min_word_frequency=1,
                      is_character_model=False, parallel_dataset=None):
    """
    Compute the vocabulary of a tokenized dataset and save to file.
    """
    vocab = collections.defaultdict(int)
    num_copy = collections.defaultdict(int)
    if parallel_dataset:
        for i, example in enumerate(dataset):
            parallel_example = parallel_dataset[i]
            for token in example:
                vocab[token] += 1
                if token in parallel_example:
                    num_copy[token] += 1
        for v in vocab:
            if vocab[v] == num_copy[v]:
                vocab[v] = 0
    else:
        for example in dataset:
            for token in example:
                vocab[token] += 1
    sorted_vocab = [(x, y) for x, y in sorted(
        vocab.items(), key=lambda x: (x[1], x[0]), reverse=True)
                    if y >= min_word_frequency]

    init_vocab = data_utils.CHAR_INIT_VOCAB if is_character_model \
        else data_utils.TOKEN_INIT_VOCAB
    vocab = [(v, 1000000) for v in init_vocab]
    for v, f in sorted_vocab:
        if not v in init_vocab:
            vocab.append((v, f))

    with open(vocab_path, 'w') as vocab_file:
        for v, f in vocab:
            vocab_file.write('{}\t{}\n'.format(v.encode('utf-8'), f))

    return dict([(x[0], y) for y, x in enumerate(vocab)])
