#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Functions for matching entity mentions in the natural language with the
corresponding program slots.
"""

import os, sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import collections, copy, re
import numpy as np
from numpy.linalg import norm

from bashlint import bash, data_tools
from nlp_tools import constants, format_args, tokenizer


# --- Classifiers for estimating likelihood of local matches --- #

class KNearestNeighborModel():
    def __init__(self, k, train_X, train_Y):
        """
        :member k: number of neighboring examples to use
        :member train_X: [size, dim] training feature matrix
        :member train_Y: [size, label_dim] training label matrix
        """
        self.k = k
        self.train_X = train_X
        self.train_Y = train_Y

    def predict(self, X):
        """
        :param X: [size, dim]
        """
        # [size, size]
        sim_scores = np.matmul(X, self.train_X.T)
        # [size, self.k]
        nn = np.argpartition(sim_scores, -self.k, axis=1)[:, -self.k:]
        # [size, self.k]
        nn_weights = np.partition(sim_scores, -self.k, axis=1)[:, -self.k:]

        nn_prediction = np.sum(
            np.expand_dims(nn_weights, 2) * self.train_Y[nn], axis=1)[:, 0]
        return nn_prediction

    def eval(self, X, Y, verbose=True):
        nn_prediction = self.predict(X)
        # compute accuracy
        threshold = 0.5
        num_total = 0.0
        num_correct = 0.0
        for i in xrange(len(nn_prediction)):
            if Y[i][0] == 1 and nn_prediction[i][0] >= threshold:
                num_correct += 1
            if Y[i][0] == 0 and nn_prediction[i][0] < threshold:
                num_correct += 1
            if verbose:
                print(nn_prediction[i][0], Y[i][0])
            num_total += 1
        print("Accuracy: ", num_correct / num_total)


def gen_slot_filling_training_data(sess, FLAGS, model, dataset, output_file):
    print("saving slot filling mappings to {}".format(output_file))

    X, Y = [], []
    for bucket_id in xrange(len(model.buckets)):
        for i in xrange(len(dataset.data_points[bucket_id])):
            dp = dataset.data_points[bucket_id][i]
            if dp.alignments is not None:
                source_inds, target_inds = dp.alignments.nonzero()
                mappings = list(zip(list(source_inds), list(target_inds)))
                encoder_channel_inputs = [[dp.sc_ids]]
                decoder_channel_inputs = [[dp.tg_ids]]
                # print(bucket_id)
                # print(encoder_channel_inputs)
                # print(decoder_channel_inputs)
                if FLAGS.use_copy:
                    encoder_channel_inputs.append([dp.csc_ids])
                    decoder_channel_inputs.append([dp.ctg_ids])
                formatted_example = model.format_batch(
                    encoder_channel_inputs, decoder_channel_inputs,
                    bucket_id=bucket_id)
                model_outputs = model.step(
                    sess, formatted_example, bucket_id, forward_only=True)
                encoder_outputs = model_outputs.encoder_hidden_states
                decoder_outputs = model_outputs.decoder_hidden_states
                # add positive examples
                for f, s in mappings:
                    # use reversed index for the encoder embedding matrix
                    ff = model.buckets[bucket_id][0] - f - 1
                    if f >= encoder_outputs.shape[1] or s >= decoder_outputs.shape[1]:
                        continue
                    X.append(np.concatenate([encoder_outputs[:, ff, :],
                                             decoder_outputs[:, s, :]], axis=1))
                    Y.append(np.array([[1, 0]]))
                    # add negative examples
                    # sample unmatched filler-slot pairs as negative examples
                    if len(mappings) > 1:
                        for n_s in [ss for _, ss in mappings if ss != s]:
                            if n_s >= decoder_outputs.shape[1]:
                                continue
                            X.append(np.concatenate(
                                [encoder_outputs[:, ff, :],
                                 decoder_outputs[:, n_s, :]], axis=1))
                            Y.append(np.array([[0, 1]]))
                    # Debugging
                    # if i == 0:
                    #     print(ff)
                    #     print(encoder_outputs[0])
                    #     print(decoder_outputs[0])
                    if len(X) > 0 and len(X) % 1000 == 0:
                        print('{} examples gathered for generating slot filling '
                              'features...'.format(len(X)))

    assert(len(X) == len(Y))
    X = np.concatenate(X, axis=0)
    X = X / np.linalg.norm(X, axis=1)[:, None]
    Y = np.concatenate(Y, axis=0)

    np.savez(output_file, X, Y)

# --- Global slot filling functions --- #

def stable_slot_filling(template_tokens, sc_fillers, tg_slots, pointer_targets,
        encoder_outputs, decoder_outputs, slot_filling_classifier, verbose=False):
    """
    Fills the argument slots using learnt local alignment scores and a greedy 
    global alignment algorithm (stable marriage).

    :param template_tokens: list of tokens in the command template
    :param sc_fillers: the slot fillers extracted from the source sequence,
        indexed by token id
    :param tg_slots: the argument slots in the command template, indexed by
        token id
    :param pointer_targets: [encoder_length, decoder_length], local alignment
        scores between source and target tokens
    :param encoder_outputs: [encoder_length, dim] sequence of encoder hidden states
    :param decoder_outputs: [decoder_length, dim] sequence of decoder hidden states
    :param slot_filling_classifier: the classifier that produces the local
        alignment scores
    :param verbose: print all local alignment scores if set to true
    """

    # Step a): prepare (binary) type alignment matrix based on type info
    M = np.zeros([len(encoder_outputs), len(decoder_outputs)], dtype=np.int32)
    for f in sc_fillers:
        if f >= len(encoder_outputs):
            print(template_tokens, f, len(encoder_outputs))
            continue
        surface, filler_type = sc_fillers[f]
        matched = False
        for s in tg_slots:
            if s >= len(decoder_outputs):
                print(tg_slots, s, len(decoder_outputs))
                continue
            slot_value, slot_type = tg_slots[s]
            if slot_filler_type_match(slot_type, filler_type):
                M[f, s] = 1
                matched = True
        if not matched:
            # If no target slot can hold a source filler, skip the alignment
            # step and return None
            return None, None, None

    # Step b): compute local alignment scores if they are not provided already
    if pointer_targets is None:
        assert(encoder_outputs is not None)
        assert(decoder_outputs is not None)
        assert(slot_filling_classifier is not None)
        pointer_targets = np.zeros([len(encoder_outputs), len(decoder_outputs)])
        for f in xrange(M.shape[0]):
            if np.sum(M[f]) > 1:
                X = []
                # use reversed index for the encoder embeddings matrix
                ff = len(encoder_outputs) - f - 1
                cm_slots_keys = list(tg_slots.keys())
                for s in cm_slots_keys:
                    X.append(np.concatenate([encoder_outputs[ff:ff+1],
                                             decoder_outputs[s:s+1]], axis=1))
                X = np.concatenate(X, axis=0)
                X = X / norm(X, axis=1)[:, None]
                raw_scores = slot_filling_classifier.predict(X)
                for ii in xrange(len(raw_scores)):
                    s = cm_slots_keys[ii]
                    pointer_targets[f, s] = raw_scores[ii]
                    if verbose:
                        print('• alignment ({}, {}): {}\t{}\t{}'.format(
                            f, s, sc_fillers[f], tg_slots[s], raw_scores[ii]))

    M = M + M * pointer_targets
    # convert M into a dictinary representation of a sparse matrix
    M_dict = collections.defaultdict(dict)
    for i in xrange(M.shape[0]):
        if np.sum(M[i]) > 0:
            for j in xrange(M.shape[1]):
                if M[i, j] > 0:
                    M_dict[i][j] = M[i, j]
    
    mappings, remained_fillers = stable_marriage_alignment(M_dict)

    if not remained_fillers:
        for f, s in mappings:
            template_tokens[s] = format_args.get_fill_in_value(
                tg_slots[s], sc_fillers[f])
        cmd = ' '.join(template_tokens)
        tree = data_tools.bash_parser(cmd)
        if not tree is None:
            fill_default_value(tree)
        temp = data_tools.ast2command(
            tree, loose_constraints=True, ignore_flag_order=False)
    else:
        tree, temp = None, None

    return tree, temp, mappings

def heuristic_slot_filling(node, ner_by_category):
    """
    Fills the argument slots with heuristic rules.
    This rule-based slot-filling algorithm has high error-rate in practice.

    :param node: the ast of a command template whose slots are to be filled
    :param entities: the slot fillers extracted from the natural language
        sentence, indexed by token id, character position and category,
        respectively.
    """
    if ner_by_category is None:
        # no constants detected in the natural language query
        return True

    def slot_filling_fun(node, arguments):
        def fill_argument(filler_type, slot_type=None):
            surface = arguments[filler_type][0][0]
            node.value = format_args.get_fill_in_value(
                (node.value, slot_type), (surface, filler_type))
            arguments[filler_type].pop(0)

        if node.is_argument():
            if node.arg_type != 'Regex' and arguments[node.arg_type]:
                fill_argument(node.arg_type)
            elif node.arg_type == 'Number':
                if arguments['Timespan']:
                    fill_argument(filler_type='Timespan', slot_type='Number')
                    return
            elif node.arg_type == 'Path':
                if arguments['Directory']:
                    fill_argument(filler_type='Directory', slot_type='Path')
                    return
                if arguments['File']:
                    fill_argument(filler_type='File', slot_type='Path')
                    return
                node.value = '.'
            elif node.arg_type == 'Directory':
                if arguments['File']:
                    fill_argument(filler_type='File', slot_type='Directory')
                    return
                if arguments['Regex']:
                    fill_argument(filler_type='Regex', slot_type='Directory')
            elif node.arg_type in ['Username', 'Groupname']:
                if arguments['Regex']:
                    fill_argument(filler_type='Regex', slot_type='Username')
            elif node.arg_type == 'Regex':
                if arguments['File']:
                    fill_argument(filler_type='File', slot_type='Regex')
                    return
                if arguments['Number']:
                    fill_argument(filler_type='Number', slot_type='Regex')
                    return
        else:
            for child in node.children:
                slot_filling_fun(child, arguments)

    arguments = collections.defaultdict(list)
    for filler_type in constants.type_conversion:
        slot_type = constants.type_conversion[filler_type]
        arguments[slot_type] = copy.deepcopy(ner_by_category[filler_type]) \
            if filler_type in ner_by_category else []

    slot_filling_fun(node, arguments)

    # The template should fit in all arguments
    for key in arguments:
        if arguments[key]:
            return False

    return True

def stable_marriage_alignment(M):
    """
    Return the stable marriage alignment between two sets of entities (fillers
    and slots).

    :param M: stores the raw match score between the two sets of entities
        represented by the rows and columns of M.

        M(i, j) = -inf implies that i and j are incompatible.
    :param include_partial_mappings: if set to True, consider partial word
        mapping between the source and target.

    """
    preferred_list_by_row = {}
    for i in M:
        preferred_list_by_row[i] = sorted(
            [(j, M[i][j]) for j in M[i] if M[i][j] > -np.inf],
            key=lambda x:x[1], reverse=True)

    remained_rows = list(M.keys())
    matched_cols = {}

    while (remained_rows):
        # In our application, it is possible to have both unmatched rows and
        # unmatched columns in the end, therefore need to detect this situation.
        preferred_list_changed = False
        for i in remained_rows:
            if len(preferred_list_by_row[i]) > 0:
                j, match_score = preferred_list_by_row[i].pop(0)
                preferred_list_changed = True
                if not j in matched_cols:
                    matched_cols[j] = (i, match_score)
                    remained_rows.remove(i)
                else:
                    if match_score > matched_cols[j][1]:
                        k, _ = matched_cols[j]
                        matched_cols[j] = (i, match_score)
                        remained_rows.remove(i)
                        remained_rows.append(k)
        if not preferred_list_changed:
            break

    return [(y, x) for (x, (y, score)) in sorted(matched_cols.items(),
            key=lambda x:x[1][1], reverse=True)], remained_rows


def fill_default_value(node):
    """
    Fill empty slot in the bash ast with default value.
    """
    if node.is_argument():
        if node.value in bash.argument_types:
            if node.arg_type == 'Path' and node.parent.is_utility() \
                    and node.parent.value == 'find':
                node.value = '.'
            elif node.arg_type == 'Regex':
                if node.parent.is_utility() and node.parent.value == 'grep':
                    node.value = '\'.*\''
                elif node.parent.is_option() and node.parent.value == '-name' \
                        and node.value == 'Regex':
                    node.value = '"*"'
                else:
                    node.value = '[' + node.arg_type.lower() + ']'
            elif node.arg_type == 'Number' and node.utility.value in ['head', 'tail']:
                node.value = '10'
            else:
                if node.is_open_vocab():
                    node.value = '[' + node.arg_type.lower() + ']'
    else:
        for child in node.children:
            fill_default_value(child)


# --- Slot-filling alignment induction from parallel data

def slot_filler_alignment_induction(nl, cm, verbose=False):
    """Give an oracle translation pair of (nl, cm), align the slot fillers
       extracted from the natural language with the slots in the command.
    """

    # Step 1: extract the token ids of the constants in the English sentence
    # and the slots in the command
    tokens, entities = tokenizer.ner_tokenizer(nl)
    nl_fillers, _, _ = entities
    cm_tokens = data_tools.bash_tokenizer(cm)
    cm_tokens_with_types = data_tools.bash_tokenizer(cm, arg_type_only=True)
    assert(len(cm_tokens) == len(cm_tokens_with_types))
    cm_slots = {}
    for i in xrange(len(cm_tokens_with_types)):
        if cm_tokens_with_types[i] in bash.argument_types:
            if i > 0 and format_args.is_min_flag(cm_tokens_with_types[i-1]):
                cm_token_type = 'Timespan'
            else:
                cm_token_type = cm_tokens_with_types[i]
            cm_slots[i] = (cm_tokens[i], cm_token_type)
    
    # Step 2: construct one-to-one mappings for the token ids from both sides
    M = collections.defaultdict(dict)               # alignment score matrix
    for i in nl_fillers:
        surface, filler_type = nl_fillers[i]
        filler_value = format_args.extract_value(filler_type, filler_type, surface)
        for j in cm_slots:
            slot_value, slot_type = cm_slots[j]
            if (filler_value and format_args.is_parameter(filler_value)) or \
                    slot_filler_type_match(slot_type, filler_type):
                M[i][j] = slot_filler_value_match(
                    slot_value, filler_value, slot_type)
            else:
                M[i][j] = -np.inf

    mappings, remained_fillers = stable_marriage_alignment(M)

    if verbose:
        print('nl: {}'.format(nl))
        print('cm: {}'.format(cm))
        for (i, j) in mappings:
            print('[{}] {} <-> [{}] {}'.format(
                i, nl_fillers[i][0], j, cm_slots[j][0]))
        for i in remained_fillers:
            print('filler {} is not matched to any slot\n'
                    .format(nl_fillers[i][0].encode('utf-8')))
    
    return mappings


def slot_filler_value_match(slot_value, filler_value, slot_type):
    """(Fuzzily) compute the matching score between a slot filler extracted
        from the natural language and a the slot in the command. Used for
        generating alignments from the training data.

       :param slot_value: slot value as shown in the bash command
       :param filler_value: slot filler value extracted from the natural language
       :param slot_type: category of the slot in the command
    """
    if slot_type in bash.pattern_argument_types or \
            (filler_value and format_args.is_parameter(filler_value)):
        if slot_value == filler_value:
            return 1

        slot_value = constants.remove_quotation(slot_value).lower()
        filler_value = constants.remove_quotation(filler_value).lower()

        if filler_value and format_args.is_parameter(filler_value):
            if format_args.strip(slot_value).lower() == \
                    format_args.strip(filler_value).lower():
                return 1
        else:
            sv = format_args.strip(slot_value).lower()
            fv = format_args.strip(filler_value).lower()
            if sv == fv:
                return 1
            elif fv in sv:
                # include partial match
                if len(sv) - len(fv) > 10:
                    return -np.inf
                else:
                    return (len(fv) + 0.0) / len(sv)
        return -np.inf
    else:
        if filler_value is None:
            if slot_type == 'Permission':
                return 1
            else:
                return 0
        if slot_type.endswith('Number'):
            if format_args.strip_sign(slot_value) == \
                    format_args.extract_number(filler_value):
                return 1
        if format_args.strip_sign(slot_value) == \
                format_args.strip_sign(filler_value):
            return 1
        else:
            if slot_type.endswith('Timespan') or slot_type.endswith('Size'):
                if format_args.extract_number(slot_value) == \
                        format_args.extract_number(filler_value):
                    return 1
        return 0

def slot_filler_type_match(slot_type, filler_type):
    """'
    Check if the category of a slot in the command matches that of the slot
    filler extracted from the natural language. Used for generating alignments
    from the training data.

    :param slot_type: slot category in the bash command
    :param filler_type: slot filler category extracted from the natural language.
    """
    c_matches = {
        '_NUMBER, Number',
        '_NUMBER, +Number',
        '_NUMBER, -Number',
        '_NUMBER, Regex',
        '_NUMBER, Quantity',
        '_NUMBER, +Quantity',
        '_NUMBER, -Quantity',
        '_SIZE, Size',
        '_SIZE, +Size',
        '_SIZE, -Size',
        '_TIMESPAN, Timespan',
        '_TIMESPAN, +Timespan',
        '_TIMESPAN, -Timespan',
        '_DATETIME, DateTime',
        '_DATETIME, +DateTime',
        '_DATETIME, -DateTime',
        '_NUMBER, Permission',
        '_NUMBER, +Permission',
        '_NUMBER, -Permission',
        '_PERMISSION, Permission',
        '_PERMISSION, +Permission',
        '_PERMISSION, -Permission',
        '_PATH, Path',
        '_DIRECTORY, Directory',
        '_DIRECTORY, Path',
        '_FILE, Path',
        '_FILE, File',
        '_FILE, Directory',
        '_FILE, Regex',
        '_REGEX, Username',
        '_REGEX, Groupname',
        '_REGEX, Directory',
        '_REGEX, File',
        '_REGEX, Path',
        '_REGEX, Regex'
    }
    return '{}, {}'.format(filler_type, slot_type) in c_matches
