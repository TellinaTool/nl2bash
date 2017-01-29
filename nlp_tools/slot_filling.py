#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Algorithms for filling the argument slots in a command template with the
   argument values extracted from the natural language"""

import collections, copy, datetime, re

from . import constants, tokenizer
from bashlex.data_tools import bash_tokenizer

# --- Slot-Filler Alignment --- #

def slot_filler_value_match(slot_value, filler_value, slot_type):
    """(Loosely) check if a slot filler extracted from the natural language
        matches a the slot in the command. Used for generating alignments from
        the training data.

       :param slot_value: slot value as shown in the bash command
       :param filler_value: slot filler value extracted from the natural language
       :param slot_type: category of the slot in the command
    """
    def strip(pattern):
        while pattern[0] in ['"', '\'', '*', '\\', '/', '.', '-']:
            if len(pattern) > 1:
                pattern = pattern[1:]
            else:
                break
        while pattern[-1] in ['"', '\'', '\\', '/', '$', '*', '.', '-']:
            if len(pattern) > 1:
                pattern = pattern[:-1]
            else:
                break
        return pattern
    print(strip(slot_value), strip(filler_value))
    def strip_sign(pattern):
        if pattern[0] in ['-', '+']:
            pattern = pattern[1:]
        return pattern

    if slot_type in constants._PATTERNS:
        print(strip(slot_value), strip(filler_value))
        return strip(slot_value).lower() == strip(filler_value).lower()
    else:
        if filler_value is None:
            if slot_type == 'Permission':
                return True
            else:
                return False
        if slot_type.endswith('Number'):
            return strip_sign(slot_value) == extract_number(filler_value)
        if strip_sign(slot_value) == strip_sign(filler_value):
            return True
        else:
            if slot_type.endswith('Timespan') or slot_type.endswith('Size'):
                return extract_number(slot_value) == extract_number(filler_value)

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
        '_TIMESPAN:::Number',
        '_TIMESPAN:::+Number',
        '_TIMESPAN:::-Number',
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
        '_FILE:::Regex',
        '_REGEX:::Username',
        '_REGEX:::Groupname',
        '_REGEX:::Directory',
        '_REGEX:::File',
        '_REGEX:::Path',
        '_REGEX:::Regex'
    }

    return '{}:::{}'.format(filler_type, slot_type) in category_matches

def get_slot_alignment(nl, cm):
    """Align the slot fillers extracted from the natural language with the
       slots in the command."""

    # Step 1: extract the token ids of the constants in the English sentence
    # and the slots in the command
    tokens, entities = tokenizer.ner_tokenizer(nl)
    nl_fillers, _, _ = entities

    cm_tokens = bash_tokenizer(cm)
    cm_tokens_with_types = bash_tokenizer(cm, arg_type_only=True)
    assert(len(cm_tokens) == len(cm_tokens_with_types))
    cm_slots = {}
    for i in xrange(len(cm_tokens_with_types)):
        if cm_tokens_with_types[i] in constants._ENTITIES:
            cm_slots[i] = (cm_tokens[i], cm_tokens_with_types[i])
    
    # Step 2: construct one-to-one mappings for the token ids from both sides
    mappings = collections.defaultdict()
    matched_slots = set()
    for i in nl_fillers:
        surface, filler_type = nl_fillers[i]
        filler_value = extract_value(filler_type, surface)
        matched = False
        type_matched_slot = -1
        num_type_matched = 0
        for j in cm_slots:
            if j in matched_slots:
                continue
            slot_value, slot_type = cm_slots[j]
            if slot_filler_type_match(slot_type, filler_type):
                type_matched_slot = j
                num_type_matched += 1
                if slot_filler_value_match(slot_value, filler_value, slot_type):
                    # print(slot_value, slot_type, filler_value, filler_type)
                    mappings[i] = j
                    matched_slots.add(j)
                    matched = True
            if matched:
                break
        if not matched:
            if num_type_matched == 1:
                mappings[i] = type_matched_slot
                matched_slots.add(type_matched_slot)
            else:
                print('nl: {}'.format(nl))
                print('cm: {}'.format(cm))
                print(nl_fillers)
                print(cm_slots)
                print('filler {} is not matched to any slot\n'
                      .format(surface.encode('utf-8')))
    return mappings

# --- Slot filler extractors --- #

def extract_value(arg_type, value):
    """Extract slot filling values from the natural language."""
    if arg_type in constants.category_conversion:
        arg_type = constants.category_conversion[arg_type]

    # remove quotations if there is any
    if constants.with_quotation(value):
        if value[0] in ['"', '\'']:
            value = value[1:]
        if value[-1] in ['"', '\'']:
            value = value[:-1]

    if arg_type in ['Directory']:
        value = value
    elif arg_type == 'Number':
        value = extract_number(value)
    elif arg_type == 'File':
        value = extract_filename(value)
    elif arg_type == 'Permission':
        value = extract_permission(value)
    elif arg_type == 'DateTime':
        value = extract_datetime(value)
    elif arg_type == 'Timespan':
        value = extract_timespan(value)
    elif arg_type == 'Size':
        value = extract_size(value)
    elif arg_type == 'Regex':
        value = value
    elif arg_type in ['Username', 'Groupname']:
        value = value

    # add quotations for pattern slots
    if arg_type in constants._PATTERNS and \
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

def extract_filename(value):
    """Extract file names."""
    special_symbol_re = re.compile(constants._SPECIAL_SYMBOL_RE)
    file_extension_re = re.compile(constants._FILE_EXTENSION_RE)
    path_re = re.compile(constants._PATH_RE)
    if re.match(special_symbol_re, value):
        return value
    else:
        match = re.search(file_extension_re, value)
        if match:
            return '"*.' + match.group(0) + '"'
        else:
            match = re.search(path_re, value)
            if match:
                return match.group(0)
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
        return None

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
        return sign + '{}d'.format(int(float(number)*365))
    if duration_unit.startswith('mon'):
        return sign + '{}d'.format(int(float(number)*30))
    if duration_unit.startswith('w'):
        if '.' in number:
            number = int(float(number) * 7)
            unit = 'd'
        else:
            unit = 'w'
        return sign + '{}{}'.format(number, unit)
    if duration_unit.startswith('d'):
        if '.' in number:
            number = int(float(number) * 24)
            unit = 'h'
        else:
            unit = 'd'
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

def heuristic_slot_filling(node, entities):
    """
    Fills the argument slots with heuristic rules. This rule-based slot-filling
    algorithm does not achieve enough accuracy in practice.
    """
    _, _, ner_by_category = entities

    if ner_by_category is None:
        # no constants detected in the natural language query
        return True

    def slot_filling_fun(node, arguments):
        arguments = collections.defaultdict(list)
        for filler_type in constants.category_conversion:
            slot_type = constants.category_conversion[filler_type]
            arguments[slot_type] = \
                copy.deepcopy(constants.category_conversion[filler_type])

        def fill_argument(filler_type, slot_type=None):
            if slot_type is None:
                slot_type = filler_type
            surface = arguments[filler_type][0][0]
            value = extract_value(filler_type, surface)
            if filler_type == 'Timespan' and slot_type == 'Number':
                value = extract_value(slot_type, value)
            if value is not None:
                if slot_type in constants._PATTERNS:
                    node.value = value
                elif slot_type in constants._QUANTITIES:
                    if node.value.startswith('+'):
                        node.value = value if value.startswith('+') else \
                            '+{}'.format(value)
                    elif node.value.startswith('-'):
                        node.value = value if value.startswith('-') else \
                            '-{}'.format(value)
                    else:
                        node.value = value
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

    slot_filling_fun(node, ner_by_category)

    # The template should fit in all arguments
    for key in ner_by_category:
        if ner_by_category[key]:
            return False
    return True
