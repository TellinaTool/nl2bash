#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Algorithms for filling the argument slots in a command template with the
   argument values extracted from the natural language"""

import collections, copy, datetime, re

from . import constants, tokenizer
from bashlex.data_tools import bash_tokenizer

def get_slot_alignment(nl, cm):
    """Extract training data for the statistical slot filling algorithm."""
    # Step 1: extract the token ids of the constants in nl and the slots in cm
    tokens, ner = tokenizer.ner_tokenizer(nl)
    nl_entities = []

    ast = bash_tokenizer(cm)
    cm_entities = []
    # Step 2: construct one-to-one mappings for the token ids from both sides


def heuristic_slot_filling(node, arguments):
    """
    Fills the argument slots with heuristic rules. This rule-based slot-filling
    algorithm does not achieve enough accuracy in practice.
    """
    if arguments is None:
        # no constants detected in the natural language query
        return True

    def copy_file_name(value):
        special_symbol_re = re.compile(constants._SPECIAL_SYMBOL_RE)
        file_extension_re = re.compile(constants._FILE_EXTENSION_RE)
        if re.match(special_symbol_re, value):
            return value
        else:
            match = re.search(file_extension_re, value)
            if match:
                return '"*.' + match.group(0) + '"'
            else:
                raise AttributeError('Unrecognized file name: {}'.format(value))

    def copy_permission(value):
        numerical_permission_re = re.compile(constants._NUMERICAL_PERMISSION_RE)
        pattern_permission_re = re.compile(constants._PATTERN_PERMISSION_RE)
        if re.match(numerical_permission_re, value) or \
                re.match(pattern_permission_re, value):
            return value
        else:
            # TODO: write rules to synthesize permission pattern
            return None

    def copy_datetime(value):
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
            print(value)
            print(date_year)
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

    def copy_timespan(value):
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

    def copy_size(value):
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

    def copy_value(arg_type, value):
        if constants.with_quotation(value):
            return value
        if arg_type in ['Number', 'Directory']:
            return value
        if arg_type == 'File':
            return copy_file_name(value)
        if arg_type == 'Permission':
            return copy_permission(value)
        if arg_type == 'DateTime':
            return copy_datetime(value)
        if arg_type == 'Timespan':
            return copy_timespan(value)
        if arg_type == 'Size':
            return copy_size(value)
        if arg_type in ['Username', 'Groupname']:
            return value
        if arg_type == 'Regex':
            return value

    def fill_arguments_fun(node, arguments):
        def fill_argument(arg_type):
            value = copy_value(arg_type, arguments[arg_type][0][0])
            if value is not None:
                if arg_type in constants._PATTERNS:
                    if not constants.with_quotation(value):
                        node.value = constants.add_quotations(value)
                    else:
                        node.value = value
                elif arg_type in constants._QUANTITIES:
                    if node.value.startswith('+'):
                        node.value = value if value.startswith('+') else \
                            '+{}'.format(value)
                    elif node.value.startswith('-'):
                        node.value = value if value.startswith('-') else \
                            '-{}'.format(value)
                    else:
                        node.value = value
            arguments[arg_type].pop(0)

        if node.is_argument():
            if node.arg_type != 'Regex' and arguments[node.arg_type]:
                fill_argument(node.arg_type)
            elif node.arg_type == 'Path':
                if arguments['Directory']:
                    fill_argument('Directory')
                    return
                if arguments['File']:
                    fill_argument('File')
                    return
                node.value = '.'
            elif node.arg_type == 'Directory':
                if arguments['File']:
                    fill_argument('File')
                    return
                if arguments['Regex']:
                    fill_argument('Regex')
            elif node.arg_type in ['Username', 'Groupname']:
                if arguments['Regex']:
                    fill_argument('Regex')
            elif node.arg_type == 'Regex':
                if arguments['File']:
                    fill_argument('File')
                    return
                if arguments['Regex']:
                    fill_argument('Regex')
                    return
        else:
            for child in node.children:
                fill_arguments_fun(child, arguments)

    renamed_arguments = collections.defaultdict(list)
    for key in constants.ner_to_ast_arg_type:
        arg_type = constants.ner_to_ast_arg_type[key]
        renamed_arguments[arg_type] = copy.deepcopy(arguments[key])
    arguments = renamed_arguments
    fill_arguments_fun(node, arguments)

    # The template should fit in all arguments
    for key in arguments:
        if arguments[key]:
            return False
    return True