#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Functions for reformatting entities mentioned in the natural language following
bash syntax.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime, re

from bashlint import bash
from nlp_tools import constants


# --- Slot filling value extractors --- #

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

    if slot_type in bash.quantity_argument_types:
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
    if filler_type in bash.pattern_argument_types and \
            not constants.with_quotation(value):
        value = constants.add_quotations(value)

    return value

def extract_number(value):
    digit_re = re.compile(constants._DIGIT_RE)
    match = re.search(digit_re, value)
    if match:
        return match.group(0)
    else:
        return 'unrecognized_numerical_expression'
        # raise AttributeError('Cannot find number representation in
        # pattern {}'.format(value))

def extract_filename(value, slot_type='File'):
    """Extract file names"""
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
    return 'unrecognized_file_name'

def extract_permission(value):
    """Extract permission patterns"""
    numerical_permission_re = re.compile(constants._NUMERICAL_PERMISSION_RE)
    pattern_permission_re = re.compile(constants._PATTERN_PERMISSION_RE)
    if re.match(numerical_permission_re, value) or \
            re.match(pattern_permission_re, value):
        return value
    else:
        # TODO: write rules to synthesize permission pattern
        return value

def extract_datetime(value):
    """Extract date/time patterns"""
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
        else:
            current_year = datetime.date.today().year
            formatted_datetime = '{}-{}'.format(current_year, month)
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
    """Extract timespans"""
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
        return sign + '{}s'.format(float(number))

    raise AttributeError("Cannot parse timespan: {}".format(value))

def extract_size(value):
    """Extract sizes"""
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

# --- Utils --- #

def strip(pattern):
    while len(pattern) > 1 and \
            pattern[0] in ['"', '\'', '*', '\\', '/', '.', '-', '+', '{', '}']:
        pattern = pattern[1:]
    while len(pattern) > 1 and \
            pattern[-1] in ['"', '\'', '\\', '/', '$', '*', '.', '-', '+', '{', '}']:
        pattern = pattern[:-1]
    special_end_re = re.compile(r'(\\n|\{\})$')
    while len(pattern) > 2 and re.search(special_end_re, pattern):
        pattern = pattern[:-2]
    while len(pattern) > 1 and \
            pattern[0] in ['"', '\'', '*', '\\', '/', '.', '-', '+', '~']:
        pattern = pattern[1:]
    while len(pattern) > 1 and \
            pattern[-1] in ['"', '\'', '\\', '/', '$', '*', '.', '-', '+', '~']:
        pattern = pattern[:-1]
    return pattern

def strip_sign(pattern):
    if pattern[0] in ['-', '+']:
        pattern = pattern[1:]
    return pattern

def is_parameter(value):
    return constants.remove_quotation(value).startswith('$')

def is_min_flag(token):
    if len(token) == 5 and token.endswith('min') and token.startswith('-'):
        return True
    return False