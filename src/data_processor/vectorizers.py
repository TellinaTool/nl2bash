"""
Format data to NN model inputs.
"""
import numpy as np
import os
import scipy.sparse as ssp

import src.data_processor.data_utils as data_utils


def vectorize_data_copy(dataset, channel):
    assert(channel in ['token', 'char', 'partial.token'])
    for exp in dataset.example_list:
        if channel == 'token':
            nl_tokens, cm_tokens = exp.nl_tokens_orig, exp.cm_tokens
        elif channel == 'char':
            nl_tokens, cm_tokens = exp.nl_chars_orig, exp.cm_chars
        elif channel == 'partial.token':
            nl_tokens, cm_tokens = exp.nl_partial_tokens_orig, exp.cm_partial_tokens
        else:
            raise NotImplementedError
        exp.alignments = compute_pair_alignment(nl_tokens, cm_tokens)


def compute_pair_alignment(nl_tokens, cm_tokens):
    """
    Compute the alignments between two parallel sequences.
    """
    m = len(nl_tokens)
    n = len(cm_tokens)

    A = np.zeros([m, n], dtype=np.int32)

    for i, x in enumerate(nl_tokens):
        for j, y in enumerate(cm_tokens):
            if x not in data_utils.TOKEN_INIT_VOCAB and x not in data_utils.CHAR_INIT_VOCAB and x == y:
                A[i, j] = 1

    return ssp.lil_matrix(A)


def vectorize_data(dataset, channel, nl_vocab, cm_vocab):
    for exp in dataset.example_list:
        if channel == 'token':
            nl_tokens, cm_tokens = exp.nl_tokens, exp.cm_tokens
        elif channel == 'char':
            nl_tokens, cm_tokens = exp.nl_chars, exp.cm_chars
        elif channel == 'partial.token':
            nl_tokens, cm_tokens = exp.nl_partial_tokens, exp.cm_partial_tokens
        elif channel == 'normalized.token':
            nl_tokens, cm_tokens = exp.nl_normalized_tokens, exp.cm_normalized_tokens
        else:
            raise NotImplementedError
        exp.nl_ids = tokens_to_ids(nl_tokens, nl_vocab)
        exp.cm_ids = tokens_to_ids(cm_tokens, cm_vocab)


def tokens_to_ids(tokens, vocabulary):
    """
    Map tokens into their indices in the vocabulary.
    """
    token_ids = []
    for t in tokens:
        if t in vocabulary:
            token_ids.append(vocabulary[t])
        else:
            token_ids.append(data_utils.UNK_ID)
    return token_ids