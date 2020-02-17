"""
Format data to NN model inputs.
"""
import numpy as np
import os
import scipy.sparse as ssp

from src.data_processor.data_utils import *


def vectorize_data_copy(dataset, channel, tg_vocab):
    assert(channel in ['token', 'char', 'partial.token'])
    for exp in dataset.all_examples:
        if channel == 'token':
            exp.copy_sc_token_ids, exp.copy_tg_token_ids = compute_copy_indices(
                exp.nl_tokens, exp.cm_tokens, exp.nl_tokens_orig, exp.cm_tokens, tg_vocab, channel)
            exp.token_alignments = compute_pair_alignment(exp.nl_tokens, exp.cm_tokens)
        elif channel == 'char':
            exp.copy_sc_char_ids, exp.copy_tg_char_ids = compute_copy_indices(
                exp.nl_chars, exp.cm_chars, exp.nl_chars_orig, exp.cm_chars, tg_vocab, channel)
            exp.char_alignments = compute_pair_alignment(exp.nl_chars, exp.cm_chars)
        elif channel == 'partial.token':
            exp.copy_sc_partial_token_ids, exp.copy_tg_partial_token_ids = compute_copy_indices(
                exp.nl_partial_tokens, exp.cm_partial_tokens, exp.nl_partial_tokens_orig, exp.cm_partial_tokens,
                tg_vocab, channel)
            exp.partial_token_alignments = compute_pair_alignment(exp.nl_partial_tokens, exp.cm_partial_tokens)
        else:
            raise NotImplementedError


def compute_copy_indices(sc_tokens, tg_tokens, sc_copy_tokens, tg_copy_tokens, tg_vocab, channel):
    if len(sc_tokens) != len(sc_copy_tokens):
        print(sc_tokens)
        print(sc_copy_tokens)
    assert (len(sc_tokens) == len(sc_copy_tokens))
    assert (len(tg_tokens) == len(tg_copy_tokens))
    copy_sc_ids, copy_tg_ids = [], []
    init_vocab = CHAR_INIT_VOCAB if channel == 'char' else TOKEN_INIT_VOCAB
    for i, sc_token in enumerate(sc_tokens):
        if sc_token not in init_vocab and sc_token in tg_vocab:
            copy_sc_ids.append(tg_vocab[sc_token])
        else:
            copy_sc_ids.append(len(tg_vocab) + sc_tokens.index(sc_token))
    for j, tg_token in enumerate(tg_tokens):
        tg_copy_token = tg_copy_tokens[j]
        if tg_token in tg_vocab:
            copy_tg_ids.append(tg_vocab[tg_token])
        else:
            if tg_copy_token in sc_copy_tokens:
                copy_tg_ids.append(
                    len(tg_vocab) + sc_copy_tokens.index(tg_copy_token))
            else:
                if channel == 'char':
                    copy_tg_ids.append(CUNK_ID)
                else:
                    copy_tg_ids.append(UNK_ID)
    # Append EOS symbol
    if channel == 'char':
        copy_tg_ids.append(CEOS_ID)
    else:
        copy_tg_ids.append(EOS_ID)
    return copy_sc_ids, copy_tg_ids


def compute_pair_alignment(nl_tokens, cm_tokens):
    """
    Compute the alignments between two parallel sequences.
    """
    m = len(nl_tokens)
    n = len(cm_tokens)

    A = np.zeros([m, n], dtype=np.int32)

    for i, x in enumerate(nl_tokens):
        for j, y in enumerate(cm_tokens):
            if x not in TOKEN_INIT_VOCAB and x not in CHAR_INIT_VOCAB and x == y:
                A[i, j] = 1

    return ssp.lil_matrix(A)


def vectorize_data(dataset, channel, nl_vocab, cm_vocab):
    for exp in dataset.all_examples:
        if channel == 'token':
            exp.nl_token_ids = tokens_to_ids(exp.nl_tokens, nl_vocab)
            exp.cm_token_ids = tokens_to_ids(exp.cm_tokens, cm_vocab)
        elif channel == 'char':
            exp.nl_char_ids = tokens_to_ids(exp.nl_chars, nl_vocab)
            exp.cm_char_ids = tokens_to_ids(exp.cm_chars, cm_vocab)
        elif channel == 'partial.token':
            exp.nl_partial_token_ids = tokens_to_ids(exp.nl_partial_tokens, nl_vocab)
            exp.cm_partial_token_ids = tokens_to_ids(exp.cm_partial_tokens, cm_vocab)
        elif channel == 'normalized.token':
            exp.nl_norm_token_ids = tokens_to_ids(exp.nl_norm_tokens, nl_vocab)
            exp.cm_norm_token_ids = tokens_to_ids(exp.cm_norm_tokens, cm_vocab)
        else:
            raise NotImplementedError


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