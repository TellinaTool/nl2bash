#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Algorithms for filling the argument slots in a command template with the
argument values extracted from the natural language.
"""

import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

import collections, copy, datetime, re
import numpy as np
from numpy.linalg import norm

from . import constants, tokenizer
from bashlint import data_tools

# --- Slot filling functions --- #

def stable_slot_filling(template_tokens, sc_fillers, tg_slots, pointer_targets,
                        encoder_outputs, decoder_outputs,
                        slot_filling_classifier, verbose=False):
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
        assert(f <= len(encoder_outputs))
        surface, filler_type = sc_fillers[f]
        matched = False
        for s in tg_slots:
            assert(s <= len(decoder_outputs))
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
            template_tokens[s] = get_fill_in_value(tg_slots[s], sc_fillers[f])
        cmd = ' '.join(template_tokens)
        tree = data_tools.bash_parser(cmd)
        if not tree is None:
            data_tools.fill_default_value(tree)
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
            node.value = get_fill_in_value((node.value, slot_type),
                                           (surface, filler_type))
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

# --- Heuristically induce slot-filling alignments from oracle translation pairs.

def slot_filler_alignment_induction(nl, cm, verbose=True):
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
        if cm_tokens_with_types[i] in constants._ENTITIES:
            if i > 0 and is_min_flag(cm_tokens_with_types[i-1]):
                cm_token_type = 'Timespan'
            else:
                cm_token_type = cm_tokens_with_types[i]
            cm_slots[i] = (cm_tokens[i], cm_token_type)
    
    # Step 2: construct one-to-one mappings for the token ids from both sides

    M = collections.defaultdict(dict)               # alignment score matrix
    for i in nl_fillers:
        surface, filler_type = nl_fillers[i]
        filler_value = extract_value(filler_type, filler_type, surface)
        for j in cm_slots:
            slot_value, slot_type = cm_slots[j]
            if (filler_value and is_parameter(filler_value)) or \
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
    if slot_type in constants._PATTERNS or \
            (filler_value and is_parameter(filler_value)):
        if slot_value == filler_value:
            return 1

        slot_value = constants.remove_quotation(slot_value).lower()
        filler_value = constants.remove_quotation(filler_value).lower()

        if filler_value and is_parameter(filler_value):
            if strip(strip_sign(slot_value)).lower() == \
                    strip(filler_value).lower():
                return 1
        else:
            sv = strip(slot_value).lower()
            fv = strip(filler_value).lower()
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
            if strip_sign(slot_value) == extract_number(filler_value):
                return 1
        if strip_sign(slot_value) == strip_sign(filler_value):
            return 1
        else:
            if slot_type.endswith('Timespan') or slot_type.endswith('Size'):
                if extract_number(slot_value) == extract_number(filler_value):
                    return 1
        return 0

def slot_filler_type_match(slot_type, filler_type):
    """Check if the category of a slot in the command matches that of the slot
    filler extracted from the natural language. Used for generating alignments
    from the training data.

    :param slot_type: slot category in the bash command
    :param filler_type: slot filler category extracted from the natural
        language.
    """
    category_matches = {
        '_NUMBER:::Number',
        '_NUMBER:::+Number',
        '_NUMBER:::-Number',
        '_NUMBER:::Regex',
        '_SIZE:::Size',
        '_SIZE:::+Size',
        '_SIZE:::-Size',
        '_TIMESPAN:::Timespan',
        '_TIMESPAN:::+Timespan',
        '_TIMESPAN:::-Timespan',
        # '_DATETIME:::Timespan',
        # '_DATETIME:::+Timespan',
        # '_DATETIME:::-Timespan',
        '_DATETIME:::DateTime',
        '_DATETIME:::+DateTime',
        '_DATETIME:::-DateTime',
        '_PERMISSION:::Permission',
        '_PERMISSION:::+Permission',
        '_PERMISSION:::-Permission',
        '_PATH:::Path',
        '_DIRECTORY:::Directory',
        '_DIRECTORY:::Path',
        '_FILE:::Path',
        '_FILE:::File',
        '_FILE:::Directory',
        '_FILE:::Regex',
        '_REGEX:::Username',
        '_REGEX:::Groupname',
        '_REGEX:::Directory',
        '_REGEX:::File',
        '_REGEX:::Path',
        '_REGEX:::Regex'
    }

    return '{}:::{}'.format(filler_type, slot_type) in category_matches

def strip(pattern):
    # special_start_1c_re = re.compile(r'^[\"\'\*\\\/\.-]]')
    # special_start_2c_re = re.compile(r'^\{\}')
    # special_end_1c_re = re.compile(r'[\"\'\\\/\$\*\.-]$')
    # special_end_2c_re = re.compile(r'(\\n|\{\})$')
    while len(pattern) > 1 and \
            pattern[0] in ['"', '\'', '*', '\\', '/', '.', '-', '{', '}']:
        pattern = pattern[1:]
    while len(pattern) > 1 and \
            pattern[-1] in ['"', '\'', '\\', '/', '$', '*', '.', '-',
                            '{', '}']:
        pattern = pattern[:-1]
    special_start_re = re.compile(r'^\{\}')
    special_end_re = re.compile(r'(\\n|\{\})$')
    while len(pattern) > 2 and re.search(special_end_re, pattern):
        pattern = pattern[:-2]
    while len(pattern) > 1 and \
            pattern[0] in ['"', '\'', '*', '\\', '/', '.', '-', '~']:
        pattern = pattern[1:]
    while len(pattern) > 1 and \
            pattern[-1] in ['"', '\'', '\\', '/', '$', '*', '.', '-', '~']:
        pattern = pattern[:-1]
    return pattern

def strip_sign(pattern):
    if pattern[0] in ['-', '+']:
        pattern = pattern[1:]
    return pattern

def is_parameter(value):
    return constants.remove_quotation(value).startswith('$')

# --- Filler value extractors --- #

def get_fill_in_value(cm_slot, nl_filler):
    """
    Compute a command argument given the argument slot specification and the
    entity being aligned to it (mostly dealing with file name formatting,
    adding signs to quantities, etc.).
    :param cm_slot: (slot_value, slot_type)
    :param nl_filler: (filler_value, filler_type)

    """
    slot_value, slot_type = cm_slot
    surface, filler_type = nl_filler
    filler_value = extract_value(filler_type, slot_type, surface)

    # In most cases the filler can be directly copied into the slot
    slot_filler_value = filler_value

    if slot_type in constants._QUANTITIES:
        if slot_value.startswith('+'):
            slot_filler_value = filler_value if filler_value.startswith('+') \
                else '+{}'.format(filler_value)
        elif slot_value.startswith('-'):
            slot_filler_value = filler_value if filler_value.startswith('-') \
                else '-{}'.format(filler_value)

    return slot_filler_value

def extract_value(filler_type, slot_type, surface):
    """
    Extract slot filling values from the natural language.
    """
    if filler_type in constants.type_conversion:
        filler_type = constants.type_conversion[filler_type]

    # remove quotations if there is any
    if constants.with_quotation(surface):
        value = constants.remove_quotation(surface)
    else:
        value = surface

    if filler_type in ['Directory']:
        value = value
    elif filler_type == 'Number':
        value = extract_number(value)
    elif filler_type == 'File':
        value = extract_filename(value, slot_type)
    elif filler_type == 'Permission':
        value = extract_permission(value)
    elif filler_type == 'DateTime':
        value = extract_datetime(value)
    elif filler_type == 'Timespan':
        value = extract_timespan(value)
    elif filler_type == 'Size':
        value = extract_size(value)
    elif filler_type == 'Regex':
        value = value
    elif filler_type in ['Username', 'Groupname']:
        value = value
    
    # add quotations for pattern slots
    if filler_type in constants._PATTERNS and \
            not constants.with_quotation(value):
        value = constants.add_quotations(value)
    
    return value

def extract_number(value):
    digit_re = re.compile(constants._DIGIT_RE)
    match = re.search(digit_re, value)
    if match:
        return match.group(0)
    else:
        raise AttributeError('Cannot find number representation in pattern {}'
                             .format(value))

def extract_filename(value, slot_type='File'):
    """Extract file names."""
    quoted_span_re = re.compile(constants._QUOTED_RE)
    special_symbol_re = re.compile(constants._SPECIAL_SYMBOL_RE)
    file_extension_re = re.compile('{}|{}'.format(constants._FILE_EXTENSION_RE,
        constants._FILE_EXTENSION_RE.upper()))
    path_re = re.compile(constants._PATH_RE)

    # path
    match = re.search(path_re, value)
    if match:
        return match.group(0)
    # file extension
    # if re.search(re.compile(r'[^ ]*\.[^ ]+'), value):
    #     # the pattern being matched represents a regular file
    #     match = re.match(file_extension_re, strip(value))
    #     if match:
    #         return '"*.' + match.group(0) + '"'
    match = re.search(file_extension_re, value)
    if match:
        if slot_type in ['Directory', 'Path']:
            return value
        else:
            if (len(match.group(0)) + 0.0) / len(strip(value)) > 0.5:
                # avoid cases in which a file name happen to contain a
                # substring which is the same as a file extension
                return '"*.' + match.group(0) + '"'
            else:
                return value
    # quotes
    if re.match(quoted_span_re, value):
        return value
    # special symbol
    if re.match(special_symbol_re, value):
        return value
    raise AttributeError('Unrecognized file name {}'.format(value))

def extract_permission(value):
    """Extract permission patterns."""
    numerical_permission_re = re.compile(constants._NUMERICAL_PERMISSION_RE)
    pattern_permission_re = re.compile(constants._PATTERN_PERMISSION_RE)
    if re.match(numerical_permission_re, value) or \
            re.match(pattern_permission_re, value):
        return value
    else:
        # TODO: write rules to synthesize permission pattern
        return value

def extract_datetime(value):
    """Extract date/time patterns."""
    standard_time = re.compile(constants.quotation_safe(
        r'\d+:\d+:\d+\.?\d*'))
    standard_datetime_dash_re = re.compile(constants.quotation_safe(
        r'\d{1,4}[-]\d{1,4}[-]\d{1,4}'))
    standard_datetime_slash_re = re.compile(constants.quotation_safe(
        r'\d{1,4}[\/]\d{1,4}[\/]\d{1,4}'))
    textual_datetime_re = re.compile(constants.quotation_safe(
        constants._MONTH_RE + r'(\s\d{0,2})?([,|\s]\d{2,4})?'))
    rel_day_re = re.compile(constants.quotation_safe(constants._REL_DAY_RE))
    month_re = re.compile(constants._MONTH_RE)
    digit_re = re.compile(constants._DIGIT_RE)
    if re.match(standard_time, value) or \
            re.match(standard_datetime_dash_re, value):
        return value
    elif re.match(standard_datetime_slash_re, value):
        return re.sub(re.compile(r'\/'), '-', value)
    elif re.match(textual_datetime_re, value):
        # TODO: refine rules for date formatting
        month = re.search(month_re, value).group(0)
        month = constants.digitize_month[month[:3]]
        date_year = re.findall(digit_re, value)
        if date_year:
            if len(date_year) == 2:
                date = date_year[0]
                year = date_year[1]
                formatted_datetime = '{}-{}-{:02}'.format(year, month, int(date))
            else:
                if ',' in value:
                    year = date_year[0]
                    formatted_datetime = '{}-{}'.format(year, month)
                else:
                    date = date_year[0]
                    formatted_datetime = '{}-{}-{:02}'.format(
                        datetime.datetime.now().year, month, int(date))
        return formatted_datetime
    elif re.match(rel_day_re, value):
        if value == 'today':
            date = datetime.date.today()
        elif value == 'yesterday':
            date = datetime.date.today() - datetime.timedelta(1)
        elif value == 'the day before yesterday':
            date = datetime.date.today() - datetime.timedelta(2)
        elif value == 'tomorrow':
            date = datetime.date.today() + datetime.timedelta(1)
        elif value == 'the day after tomorrow':
            date = datetime.date.today() + datetime.timedelta(2)
        else:
            raise AttributeError("Cannot parse relative date expression: {}"
                                 .format(value))
        return date.strftime('%y-%m-%d')
    else:
        raise AttributeError("Cannot parse date/time: {}".format(value))

def extract_timespan(value):
    """Extract timespans."""
    digit_re = re.compile(constants._DIGIT_RE)
    duration_unit_re = re.compile(constants._DURATION_UNIT)
    m = re.search(digit_re, value)
    number = m.group(0) if m else '1'
    duration_unit = sorted(re.findall(duration_unit_re, value),
                           key=lambda x:len(x), reverse=True)[0]
    # TODO: refine rules for time span formatting and calculation
    if value.startswith('+'):
        sign = '+'
    elif value.startswith('-'):
        sign = '-'
    else:
        sign = ''
    if duration_unit.startswith('y'):
        return sign + '{}'.format(int(float(number)*365))
    if duration_unit.startswith('mon'):
        return sign + '{}'.format(int(float(number)*30))
    if duration_unit.startswith('w'):
        return sign + '{}'.format(int(float(number)*7))
    if duration_unit.startswith('d'):
        if '.' in number:
            number = int(float(number) * 24)
            unit = 'h'
        else:
            unit = ''
        return sign + '{}{}'.format(number, unit)
    if duration_unit.startswith('h'):
        if '.' in number:
            number = int(float(number) * 60)
            unit = 'm'
        else:
            unit = 'h'
        return sign + '{}{}'.format(number, unit)
    if duration_unit.startswith('m'):
        if '.' in number:
            number = int(float(number) * 60)
            unit = 's'
        else:
            unit = 'm'
        return sign + '{}{}'.format(number, unit)
    if duration_unit.startswith('s'):
        return sign + '{}s'.format(int(number))

    raise AttributeError("Cannot parse timespan: {}".format(value))

def extract_size(value):
    """Extract sizes."""
    digit_re = re.compile(constants._DIGIT_RE)
    size_unit_re = re.compile(constants._SIZE_UNIT)
    m = re.search(digit_re, value)
    number = m.group(0) if m else '1'
    size_unit = sorted(re.findall(size_unit_re, value),
                       key=lambda x:len(x), reverse=True)[0]
    if value.startswith('+'):
        sign = '+'
    elif value.startswith('-'):
        sign = '-'
    else:
        sign = ''
    if size_unit.startswith('b'):
        number = int(float(number))
        unit = 'c'
        return sign + '{}{}'.format(number, unit)
    elif size_unit.startswith('k'):
        if '.' in number:
            number = int(float(number) * 1000)
            unit = 'c'
        else:
            unit = 'k'
        return sign + '{}{}'.format(number, unit)
    elif size_unit.startswith('m'):
        if '.' in number:
            number = int(float(number) * 1000)
            unit = 'k'
        else:
            unit = 'M'
        return sign + '{}{}'.format(number, unit)
    elif size_unit.startswith('g'):
        if '.' in number:
            number = int(float(number) * 1000)
            unit = 'M'
        else:
            unit = 'G'
        return sign + '{}{}'.format(number, unit)
    elif size_unit.startswith('t'):
        number = int(float(number) * 1000)
        unit = 'G'
        return sign + '{}{}'.format(number, unit)
    else:
        raise AttributeError('Unrecognized size unit: {}'.format(size_unit))

def is_min_flag(token):
    if len(token) == 5 and token.endswith('min') and token.startswith('-'):
        return True
    return False
