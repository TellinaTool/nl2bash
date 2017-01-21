#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Domain-specific natural Language and bash command tokenizer.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections, copy, datetime, re

from bashlex import bash, nast, normalizer
from nlp_tools import constants


def is_simple(ast):
    # Check if tree contains only high-frequency commands
    if ast.kind == "headcommand" and not ast.value in bash.head_commands:
        return False
    for child in ast.children:
        if not is_simple(child):
            return False
    return True


def char_tokenizer(sentence, base_tokenizer=None):
    if base_tokenizer:
        # normalization is not needed for character model
        tokens = base_tokenizer(sentence)
    else:
        tokens = [sentence]
    chars = []
    for token in tokens:
        for c in token:
            chars.append(c)
        chars.append(constants._SPACE)
    return chars[:-1]


def bash_tokenizer(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True):
    tree = normalizer.normalize_ast(cmd, normalize_digits,
                                    normalize_long_pattern, recover_quotation)
    return normalizer.to_tokens(tree)


def bash_parser(cmd, normalize_digits=True, normalize_long_pattern=True,
                recover_quotation=True):
    """Parse bash command into AST."""
    return normalizer.normalize_ast(cmd, normalize_digits,
                                    normalize_long_pattern, recover_quotation)


def fill_arguments(node, arguments):
    """
    Fill the argument slot in a command template with the argument values
    extracted from the natural language.
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
            match = re.match(file_extension_re, value)
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
            print(date_year)
            if len(date_year) == 2:
                date = date_year[0]
                year = date_year[1]
            else:
                if ',' in value:
                    year = date_year[0]
                else:
                    date = date_year[0]
            return '{}-{}-{}'.format(year, month, date)
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
            if '.' in number:
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
            value = copy_value(arg_type, arguments[arg_type][0])
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
                if arguments['Regex']:
                    fill_argument('Regex')
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


def pretty_print(node, depth=0):
    """Pretty print the AST."""
    try:
        print("    " * depth + node.kind.upper() + '(' + node.value + ')')
        for child in node.children:
            pretty_print(child, depth+1)
    except AttributeError:
        print("    " * depth)


def ast2list(node, order='dfs', list=None, ignore_flag_order=False, arg_type_only=False,
             with_parent=False):
    """Linearize the AST."""
    if order == 'dfs':
        if arg_type_only and node.is_argument() and node.is_open_vocab():
            print(node.headcommand.value)
            print(node.parent.value)
            print(node.value)
            print(node.arg_type)
            list.append(node.prefix + node.arg_type)
        else:
            if node.is_option() and with_parent and node.headcommand:
                list.append(node.prefix + node.headcommand.value + "@@" + node.value)
            else:
                list.append(node.symbol)
        if node.get_num_of_children() > 0:
            if node.kind == "headcommand" and ignore_flag_order:
                children = sorted(node.children, key=lambda x:x.value)
            else:
                children = node.children
            for child in children:
                ast2list(child, order, list, ignore_flag_order, arg_type_only,
                         with_parent)
            list.append(normalizer._H_NO_EXPAND)
        else:
            list.append(normalizer._V_NO_EXPAND)
    return list


def list2ast(list, order='dfs'):
    """Convert the linearized parse tree back to the AST data structure."""
    return normalizer.list_to_ast(list, order)


def ast2tokens(node, loose_constraints=False, ignore_flag_order=False,
               arg_type_only=False, with_parent=False):
    return normalizer.to_tokens(node, loose_constraints, ignore_flag_order, arg_type_only,
                                with_parent=with_parent)


def ast2command(node, loose_constraints=False, ignore_flag_order=False):
    return normalizer.to_command(node, loose_constraints, ignore_flag_order)


def ast2template(node, loose_constraints=False, ignore_flag_order=True, arg_type_only=True):
    # convert a bash AST to a template that contains only reserved words and argument types
    # flags are alphabetically ordered
    tokens = normalizer.to_tokens(node, loose_constraints, ignore_flag_order,
                                  arg_type_only=arg_type_only, index_arg=True)
    return ' '.join(tokens) 


def cmd2template(cmd, normalize_digits=True, normalize_long_pattern=True,
                recover_quotation=True, arg_type_only=True,
                loose_constraints=False):
    # convert a bash command to a template that contains only reserved words and argument types
    # flags are alphabetically ordered
    tree = normalizer.normalize_ast(cmd, normalize_digits, normalize_long_pattern,
                         recover_quotation)
    return ast2template(tree, loose_constraints, arg_type_only)


def paren_parser(line):
    def order_child_fun(node):
        for child in node.children:
            order_child_fun(child)
        if len(node.children) > 1 and node.children[0].value in ["and", "or"]:
            node.children = node.children[:1] + sorted(node.children[1:],
                    key=lambda x:(x.value if x.kind == "t" else (
                        x.children[0].value if x.children else x.value)))

    """A very simple algorithm for parsing data with parentheses."""
    if not line.startswith("("):
        line = "( " + line
    if not line.endswith(")"):
        line = line + " )"
    words = line.strip().split()

    root = nast.Node(kind="root", value="root")
    stack = []

    i = 0
    while i < len(words):
        word = words[i]
        if word == "(":
            if stack:
                # creates non-terminal
                node = nast.Node(kind="nt", value="<n>")
                stack[-1].add_child(node)
                node.parent = stack[-1]
                stack.append(node)
            else:
                stack.append(root)
        elif word == ")":
            if stack:
                stack.pop()
        else:
            node = nast.Node(kind="t", value=word)
            stack[-1].add_child(node)
            node.parent = stack[-1]
        i += 1
        if len(stack) == 0:
            break

    # order nodes
    order_child_fun(root)

    return root


def test_bash_parser():
    while True:
        try:
            cmd = raw_input("> ")
            norm_tree = bash_parser(cmd)
            pruned_tree = normalizer.prune_ast(norm_tree)
            print()
            print("AST:")
            pretty_print(norm_tree, 0)
            # print("Pruned AST:")
            # pretty_print(pruned_tree, 0)
            # search_history = ast2list(norm_tree, 'dfs', list=[])
            # for state in search_history:
            #     print(state)
            print("Command Template:")
            print(ast2template(norm_tree, ignore_flag_order=False))
            print("Command: ")
            print(ast2command(norm_tree, ignore_flag_order=False))
            # print("Pruned Command Template:")
            # print(ast2template(pruned_tree, ignore_flag_order=False))
            print()
        except EOFError as ex:
            break


if __name__ == "__main__":
    test_bash_parser()
