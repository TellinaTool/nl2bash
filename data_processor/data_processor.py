"""
Collection of data processing functions.
"""
import collections
import os

import bashlint
from bashlint import bash
from data_processor.data_utils import *
from data_processor.data_loader import initialize_vocabulary
from nlp_tools import tokenizer


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

    def read_parallel_data(nl_path, cm_path):
        with open(nl_path) as f:
            nl_list = [nl.strip() for nl in f.readlines()]
        with open(cm_path) as f:
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
    nl_ids = [tokens_to_ids(example, nl_vocab) for example in nl_tokens]
    cm_ids = [tokens_to_ids(example, cm_vocab) for example in cm_tokens]
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
    out_align = os.path.join(data_dir, '{}.{}.align'.format(split, channel))
    save_pair_alignment(alignments, out_align)


def save_channel_features_to_file(data_dir, split, channel, nl_features,
                                  cm_features, feature_separator):
    convert_to_str = channel.startswith('ids')
    nl_feature_path = os.path.join(data_dir, '{}.nl.{}'.format(split, channel))
    cm_feature_path = os.path.join(data_dir, '{}.cm.{}'.format(split, channel))
    with open(nl_feature_path, 'w') as o_f:
        for example in nl_features:
            if convert_to_str:
                o_f.write('{}\n'.format(feature_separator.join(
                    [str(x) for x in example])))
            else:
                o_f.write('{}\n'.format(feature_separator.join(example)))
    with open(cm_feature_path, 'w') as o_f:
        for example in cm_features:
            if convert_to_str:
                o_f.write('{}\n'.format(feature_separator.join(
                    [str(x) for x in example])))
            else:
                o_f.write('{}\n'.format(feature_separator.join(example)))


def parallel_data_to_characters(nl_list, cm_list):
    nl_data = [nl_to_characters(nl) for nl in nl_list]
    cm_data = [cm_to_characters(cm) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_partial_tokens(nl_list, cm_list):
    nl_data = [nl_to_partial_tokens(nl, tokenizer.basic_tokenizer) for nl in nl_list]
    cm_data = [cm_to_partial_tokens(cm, bashlint.bash_tokenizer) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_tokens(nl_list, cm_list):
    nl_data = [nl_to_tokens(nl, tokenizer.basic_tokenizer) for nl in nl_list]
    cm_data = [cm_to_tokens(cm, bashlint.bash_tokenizer) for cm in cm_list]
    return nl_data, cm_data


def parallel_data_to_normalized_tokens(nl_list, cm_list):
    nl_data = [nl_to_tokens(nl, tokenizer.ner_tokenizer) for nl in nl_list]
    cm_data = [cm_to_tokens(cm, bashlint.bash_tokenizer, arg_type_only=True)
               for cm in cm_list]
    return nl_data, cm_data


def string_to_characters(s):
    assert (isinstance(s, str))
    chars = []
    for c in s:
        if c == ' ':
            chars.append(constants._SPACE)
        else:
            chars.append(c)
    return chars


def nl_to_characters(nl, use_preprocessing=False):
    nl_example = []
    if use_preprocessing:
        nl_tokens = nl_to_tokens(nl, tokenizer.basic_tokenizer, lemmatization=False)
        for c in ' '.join(nl_tokens):
            if c == ' ':
                nl_example.append(constants._SPACE)
            else:
                nl_example.append(c)
    else:
        nl_example = string_to_characters(nl)
    return nl_example


def cm_to_characters(cm, use_preprocessing=False):
    cm_example = []
    if use_preprocessing:
        cm_tokens = cm_to_tokens(
            cm, bashlint.bash_tokenizer, with_prefix=True,
            with_flag_argtype=True)
        for i, t in enumerate(cm_tokens):
            if not nast.KIND_PREFIX in t:
                cm_example.append(t)
            else:
                kind, token = t.split(nast.KIND_PREFIX, 1)
                if kind.lower() == 'utility':
                    cm_example.append(token)
                elif kind.lower() == 'flag':
                    cm_example.append(token)
                else:
                    for c in token:
                        cm_example.append(c)
            if i < len(cm_tokens) - 1:
                cm_example.append(constants._SPACE)
    else:
        cm = bashlint.clean_and_normalize(cm)
        cm_example = string_to_characters(cm)
    return cm_example


def nl_to_partial_tokens(s, tokenizer, to_lower_case=True, lemmatization=True):
    return string_to_partial_tokens(
        nl_to_tokens(s, tokenizer, to_lower_case=to_lower_case,
                     lemmatization=lemmatization), use_arg_start_end=False)


def cm_to_partial_tokens(s, tokenizer):
    s = bashlint.clean_and_normalize(s)
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
                or bashlint.flag_suffix in token \
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


def compute_alignments(nl_list, cm_list):
    alignments = []
    for nl_tokens, cm_tokens in zip(nl_list, cm_list):
        alignments.append(compute_pair_alignment(nl_tokens, cm_tokens))
    return alignments


def compute_pair_alignment(nl_tokens, cm_tokens):
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

    return ssp.lil_matrix(A)


def create_vocabulary(vocab_path, dataset, min_word_frequency=1, is_character_model=False,
                      parallel_dataset=None):
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

    if is_character_model:
        # Character model
        init_vocab = CHAR_INIT_VOCAB
    else:
        init_vocab = TOKEN_INIT_VOCAB
    vocab = [(v, 1000000) for v in init_vocab]
    for v, f in sorted_vocab:
        if not v in init_vocab:
            vocab.append((v, f))

    with open(vocab_path, 'w') as vocab_file:
        for v, f in vocab:
            vocab_file.write('{}\t{}\n'.format(v, f))

    return dict([(x[0], y) for y, x in enumerate(vocab)])


if __name__ == '__main__':
    print(nl_to_partial_tokens('Execute md5sum command on files found by the find command',
                               tokenizer=tokenizer.basic_tokenizer))
    print(cm_to_partial_tokens("find . -perm -600 -print",
                               tokenizer=bashlint.bash_tokenizer))
