#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Consume tokens in a bash command and tract the next possible states.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import os, sys
if sys.version_info > (3, 0):
    from six.moves import xrange

UTIL_S = 0
FLAG_S = 1
COMMAND_S = 2
ARG_COMMAND_S = 3
EXEC_COMMAND_S = 4
ARG_S = 5
EOS_S = 6


class BashGrammarState(object):
    def __init__(self, type):
        self.type = type

    def is_argument(self):
        return self.type == ARG_S

    def is_command(self):
        return self.type == COMMAND_S \
               or self.type == ARG_COMMAND_S \
               or self.type == EXEC_COMMAND_S

    def is_flag(self):
        return self.type == FLAG_S

    def is_utility(self):
        return self.type == UTIL_S

    def is_eof(self):
        return self.type == EOS_S


class UtilityState(BashGrammarState):
    def __init__(self, name):
        super(UtilityState, self).__init__(UTIL_S)
        self.name = name
        self.flag_index = {}
        self.positional_arguments = []

    def serialize(self):
        header = self.name
        for flag in sorted(self.flag_index.keys()):
            header += ' ' + self.flag_index[flag].serialize()
        for arg in self.positional_arguments:
            header += ' ' + arg.serialize()
        return header

class FlagState(BashGrammarState):
    def __init__(self, flag_name, optional):
        super(FlagState, self).__init__(FLAG_S)
        self.flag_name = flag_name
        self.optional = optional
        self.argument = None

    def serialize(self):
        header = '{}'.format(self.flag_name)
        if self.argument:
            header += ' ' + self.argument.serialize()
        if self.optional:
            header = '[ {} ]'.format(header)
        return header


class ArgumentState(BashGrammarState):
    def __init__(self, arg_name, arg_type, optional=False, is_list=False,
                 list_separator=' ', regex_format=None):
        """
        :member arg_name: Name of argument as appeared in the man page.
        :member arg_type: Semantic type of argument as assigned in the synopsis.
        :member optional: If set, argument is optional.
        :member is_list: If set, argument can be a list.
        :member list_separator: Argument list separator.
        :member regex_format: Pattern which specifies the structure to parse the argument.
        """
        super(ArgumentState, self).__init__(ARG_S)
        self.arg_name = arg_name
        self.arg_type = arg_type
        self.optional = optional
        self.is_list = is_list
        self.list_separator = list_separator
        self.regex_format = regex_format

    def serialize(self):
        header = '{} ({})'.format(self.arg_type, self.arg_name)
        if self.optional:
            header = '[ {} ]'.format(header)
        if self.is_list:
            header += '{}...'.format(self.list_separator)
        if self.regex_format:
            header += '<{}>'.format(self.regex_format)
        return header


class ArgCommandState(BashGrammarState):
    def __init__(self):
        super(ArgCommandState, self).__init__(ARG_COMMAND_S)

    def serialize(self):
        return 'COMMAND'


class ExecCommandState(BashGrammarState):
    def __init__(self, stop_tokens):
        super(ExecCommandState, self).__init__(EXEC_COMMAND_S)
        self.stop_tokens = stop_tokens

    def serialize(self):
        return '{}$${}'.format('COMMAND', ','.join(self.stop_tokens))


class CommandState(BashGrammarState):
    def __init__(self):
        super(CommandState, self).__init__(COMMAND_S)


class BashGrammar(object):
    def __init__(self):
        self.name2type = {}
        self.grammar = {}
        self.next_states = None     # pointer on the current position in the grammar tree

    def allow_eof(self):
        for state in self.next_states:
            if state.is_eof():
                return True
        return False

    def get_next_state(self, state_type):
        for state in self.next_states:
            if state.type == state_type:
                return state

    def consume(self, token):
        if token in self.grammar:
            utility_state = self.grammar[token]
            self.next_states = utility_state
        else:
            return None

    def push(self, token, state_type):
        state = self.get_next_state(state_type)
        if state_type == FLAG_S:
            if token.startswith('--'):
                # long option
                if '=' in token:
                    flag_token, flag_arg = token.split('=', 1)
                else:
                    flag_token, flag_arg = token, ''
                if flag_token in state.token_candidates:
                    arg_info = state.token_candidates[flag_token]
                    if arg_info:
                        if not flag_arg:
                            self.next_states = [arg_info]
                            return [(flag_token, '__OPEN__')]
                        else:
                            return [(flag_token, flag_arg)]
                    else:
                        if not flag_arg:
                            return [(flag_token, None)]
                        else:
                            raise ValueError('Unexpected flag argument "{}"'.format(token))
                else:
                    raise ValueError('Unrecognized long flag "{}"'.format(token))
            elif token in state.token_candidates:
                flag_token = token
                arg_info = state.token_candidates[flag_token]
                if arg_info is not None:
                    self.next_states = state.children
                    return [(flag_token, '__OPEN__')]
                else:
                    return [(flag_token, None)]
            else:
                flag_token = token[:2]
                if flag_token in state.token_candidates:
                    if state.token_candidates[flag_token]:
                        # Case 1: argument follows flag
                        flag_arg = token[2:]
                        return [(flag_token, flag_arg)]
                    elif len(flag_token) > 2 and flag_token.startswith('-'):
                        flag_list = [(flag_token, None)]
                        # Case 2: multiple flags specified at the same time
                        for j in xrange(2, len(token)):
                            flag_token = '-' + token[j]
                            if flag_token in state.token_candidates:
                                flag_list.append((flag_token, None))
                            else:
                                raise ValueError('Unrecognized flag "{}"'.format(flag_token))
                        return flag_list
                else:
                    # Case 3: argument specified with '-'
                    if flag_token.startswith('-') and '-' in state.token_candidates \
                            and state.token_candidates['-']:
                        flag_arg = token[1:]
                        return [('-', flag_arg)]
                    else:
                        # Case 4: the token does not match any flag state
                        return None
        elif state_type == COMMAND_S:
            self.next_states = state.get_utility().children
        elif state_type == ARG_COMMAND_S:
            self.next_states = state.get_utility().children
        elif state_type == EXEC_COMMAND_S:
            self.next_states = state.get_utility().children
        elif state.type == ARG_S:
            self.next_states = state.get_utility().children
        elif state.type == UTIL_S:
            self.next_states = self.grammar['token']

    def make_grammar(self, input_file):
        """
        Build utility grammar from man-page synopsis.
        """
        with open(input_file) as f:
            content = f.readlines()

        reading_type = False
        reading_constants = False
        reading_synopsis = False

        for line in content:
            l = line.strip()
            if not l:
                continue
            if l == 'type':
                reading_type = True
                reading_constants = False
                reading_synopsis = False
            elif l == 'constants':
                reading_constants = True
                reading_type = False
                reading_synopsis = False
            elif l == 'PrimitiveCmd ::=':
                reading_synopsis = True
                reading_type = False
                reading_constants = False
            elif reading_type:
                type, names = line.strip().split(' ', 1)
                for name in names.strip()[1:-1].split(','):
                    name = name.strip()
                    if not name in self.name2type:
                        self.name2type[name] = type
                        print(name, type)
                    else:
                        raise ValueError('Ambiguity in name type: "{}" ({} vs. {})'.format(
                            name, self.name2type[name], type))
            elif reading_synopsis:
                self.make_utility(line)

    def make_utility(self, line):
        line = line.strip()
        if line.startswith('* '):
            line = line[2:]

        if len(line.strip().split()) == 1:
            utility = line.strip()
            u_state = UtilityState(utility)
            self.grammar[utility] = u_state
            return

        utility, synopsis = line.strip().split(' ', 1)
        # print(utility, synopsis)
        if not utility in self.grammar:
            u_state = UtilityState(utility)
            self.grammar[utility] = u_state
        else:
            u_state = self.grammar[utility]

        # parse the synopsis of a utility into flag portion and argument
        # portion
        stack = []
        status = 'IDLE'
        flag_synopsis = ''
        arg_synopsis = ''
        for i in xrange(len(synopsis)):
            c = synopsis[i]
            if status == 'IDLE':
                if c == '-' or c == '+':
                    status = 'READING_FLAG'
                    flag_synopsis += c
                elif c == '[':
                    # reading either an optional flag or an optional argument
                    status = 'READING_OPTIONAL'
                    stack.append('[')
                elif c.strip():
                    status = 'READING_ARGUMENT'
                    arg_synopsis += c
            elif status == 'READING_FLAG':
                if c == ' ' or c == '\n':
                    self.make_flag(u_state, flag_synopsis)
                    flag_synopsis = ''
                    status = 'IDLE'
                else:
                    flag_synopsis += c
            elif status == 'READING_ARGUMENT':
                if c == ' ' or c == '\n':
                    self.make_positional_argument(u_state, arg_synopsis)
                    arg_synopsis = ''
                    status = 'IDLE'
                else:
                    arg_synopsis += c
            elif status == 'READING_OPTIONAL':
                if c == '-' or c == '+':
                    status = 'READING_OPTIONAL_FLAG'
                    flag_synopsis += c
                elif c.strip():
                    status = 'READING_OPTIONAL_ARGUMENT'
                    arg_synopsis += c
            elif status == 'READING_OPTIONAL_FLAG':
                if c == ']':
                    stack.pop()
                    if not stack:
                        self.make_flag(u_state, flag_synopsis.strip(), optional=True)
                        flag_synopsis = ''
                        status = 'IDLE'
                    else:
                        flag_synopsis += c
                else:
                    flag_synopsis += c
                    if c == '[':
                        stack.append('[')
            elif status == 'READING_OPTIONAL_ARGUMENT':
                if c == ']':
                    stack.pop()
                    if not stack:
                        self.make_positional_argument(u_state, arg_synopsis.strip(), optional=True)
                        arg_synopsis = ''
                        status = 'IDLE'
                    else:
                        arg_synopsis += c
                else:
                    arg_synopsis += c
                    if c == '[':
                        stack.append('[')
        print(u_state.serialize())

    def make_positional_argument(self, u_state, synopsis, optional=False):
        assert(u_state is not None)
        arg = self.make_argument(synopsis, optional=optional)
        u_state.positional_arguments.append(arg)

    def make_flag_argument(self, f_state, synopsis, optional=False):
        assert(f_state is not None)
        f_state.argument  = self.make_argument(synopsis, optional=optional)

    def make_argument(self, synopsis, optional=False):
        if '$$' in synopsis:
            _, stop_token_synopsis = synopsis.split('$$', 1)
            stop_token_list = stop_token_synopsis.split(',')
            arg = ExecCommandState(stop_token_list)
        else:
            if synopsis.endswith('...'):
                is_list = True
                synopsis = synopsis[:-3]
                if synopsis[-1] in [',', '|']:
                    list_separator = synopsis[-1]
                    synopsis = synopsis[:-1]
                else:
                    list_separator = ' '
            else:
                is_list = False
                list_separator = ' '
            if '<' in synopsis:
                assert(synopsis.endswith('>'))
                arg_name, format = synopsis[:-1].split('<', 1)
                arg_name = arg_name.lower()
                arg_type = self.name2type[arg_name]
                arg = ArgumentState(arg_name, arg_type, optional=optional, is_list=is_list,
                                    list_separator=list_separator, regex_format=format)
            else:
                arg_name = synopsis.lower()
                arg_type = self.name2type[arg_name]
                if arg_type == 'Command':
                    arg = ArgCommandState()
                else:
                    arg = ArgumentState(arg_name, arg_type, optional=optional,
                        is_list=is_list, list_separator=list_separator)
        return arg

    def make_flag(self, u_state, synopsis, optional=False):
        assert(u_state is not None)
        synopsis += ' '
        if synopsis.startswith('--'):
            # long flag option
            if '=' in synopsis:
                status = 'READING_FLAG'
                stack = []
                flag = None
                flag_name = ''
                arg_synopsis = ''
                for i in xrange(len(synopsis)):
                    c = synopsis[i]
                    if status == 'READING_FLAG':
                        if c == '=' or c == '[':
                            flag = FlagState(flag_name, optional=optional)
                            if c == '[':
                                stack.append(c)
                                status = 'READING_OPTIONAL_FLAG_ARGUMENT'
                            else:
                                status = 'READING_FLAG_ARGUMENT'
                        elif c.strip():
                            flag_name += c
                    elif status == 'READING_FLAG_ARGUMENT':
                        if c == ' ':
                            self.make_flag_argument(flag, arg_synopsis, optional=False)
                        elif c.strip():
                            arg_synopsis += c
                    elif status == 'READING_OPTIONAL_FLAG_ARGUMENT':
                        if c == ']':
                            stack.pop()
                            if not stack:
                                self.make_flag_argument(flag, arg_synopsis, optional=False)
                            else:
                                arg_synopsis += c
                        elif c.strip() and c != '=':
                            arg_synopsis += c
            else:
                flag = FlagState(synopsis, optional=optional)
            u_state.flag_index[flag.flag_name] = flag
        else:
            status = 'IDLE'
            stack = []
            flag = None
            flag_name = ''
            arg_synopsis = ''
            optional_synopsis = ''
            for i in xrange(len(synopsis)):
                c = synopsis[i]
                if status == 'IDLE':
                    if c == '-' or c == '+':
                        flag_name += c
                        status = 'READING_FLAG_NAME'
                    elif c == '[':
                        stack.append(c)
                        status = 'READING_OPTIONAL'
                    elif c == ']':
                        stack.pop()
                    elif c.strip() and c != '|':
                        arg_synopsis += c
                        status = 'READING_FLAG_ARGUMENT'
                elif status == 'READING_OPTIONAL':
                    if c == '-' or c == '+':
                        optional_synopsis += c
                        status = 'READING_OPTIONAL_SECONDARY_FLAG'
                    elif c.strip():
                        if c == '[':
                            stack.append(c)
                        arg_synopsis += c
                        status = 'READING_OPTIONAL_FLAG_ARGUMENT'
                elif status == 'READING_FLAG_NAME':
                    if c == ' ' or c == '|':
                        flag = self.split_flags(u_state, flag_name, optional=optional)
                        flag_name = ''
                        status = 'IDLE'
                    elif c == ']':
                        mark = stack.pop()
                        if not mark.endswith('FLAG_NAME'):
                            flag = self.split_flags(u_state, flag_name, optional=optional)
                            flag_name = ''
                            status = 'IDLE'
                        else:
                            flag_name += c
                    elif c.strip():
                        if c == '[':
                            stack.append(c + 'FLAG_NAME')
                        flag_name += c
                elif status == 'READING_FLAG_ARGUMENT':
                    if c == ' ':
                        self.make_flag_argument(flag, arg_synopsis, optional=False)
                        arg_synopsis = ''
                        status = 'IDLE'
                    elif c == ']':
                        mark = stack.pop()
                        if not mark.endswith('FLAG_ARGUMENT'):
                            self.make_flag_argument(flag, arg_synopsis, optional=False)
                            arg_synopsis = ''
                            status = 'IDLE'
                        else:
                            arg_synopsis += c
                    elif c.strip():
                        if c == '[':
                            stack.append(c + 'FLAG_ARGUMENT')
                        arg_synopsis += c
                elif status == 'READING_OPTIONAL_FLAG_ARGUMENT':
                    if c == ' ':
                        self.make_flag_argument(flag, arg_synopsis, optional=True)
                        arg_synopsis = ''
                        status = 'IDLE'
                    elif c == ']':
                        mark = stack.pop()
                        if not mark.endswith('OPTIONAL_FLAG_ARGUMENT'):
                            self.make_flag_argument(flag, arg_synopsis, optional=True)
                            arg_synopsis = ''
                            status = 'IDLE'
                        else:
                            arg_synopsis += c
                    elif c.strip():
                        if c == '[':
                            stack.append(c + 'OPTIONAL_FLAG_ARGUMENT')
                        arg_synopsis += c
                elif status == 'READING_OPTIONAL_SECONDARY_FLAG':
                    if c == ']':
                        mark = stack.pop()
                        if mark.endswith('OPTIONAL_SECONDARY_FLAG'):
                            self.make_flag(u_state, optional_synopsis, optional=True)
                            optional_synopsis = ''
                        else:
                            optional_synopsis += c
                    elif c.strip():
                        if c == '[':
                            stack.append(c + 'OPTIONAL_SECONDARY_FLAG')
                        optional_synopsis += c

    def split_flags(self, u_state, flag_name, optional=False):
        """
        If multiple flags were specified in the same synopsis, split them.
        """
        if flag_name.endswith('::'):
            # split flags
            flag_prefix = flag_name[0]
            for i in xrange(1, len(flag_name)-2):
                new_flag_name = flag_prefix + flag_name[i]
                flag = FlagState(new_flag_name, optional=optional)
                u_state.flag_index[new_flag_name] = flag
        else:
            flag = FlagState(flag_name, optional=optional)
            u_state.flag_index[flag_name] = flag
        return flag


if __name__ == '__main__':
    bg = BashGrammar()
    bg.make_grammar(os.path.join(os.path.dirname(__file__), '..', 'grammar', 'grammar100.txt'))
    # bg.make_utility('chmod [-R [-H | -L | -P]] [ -c | --changes ] [ -f | --silent | --quiet ] [ -v | --verbose ] [ --no-preserve-root ] [ --preserve-root ] [ -R | --recursive ] [ --help ] [ --version ] MODE[,MODE]... FILE...')
    # bg.make_utility('less [-aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX::] [+aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX::] [-+] [--+] [-b space] [-h lines] [-j line] [-k keyfile] [-o logfile] [-O logfile] [-p pattern] [-P prompt] [-t tag] [-T tagsfile] [-x n,...] [--tabs=n,...] [-y lines] [--max-forw-scroll=n] [-[z] lines] [--window=n] [-TILDE] [--tilde] [-SHARP shift] [--shift shift] [-X] [--no-init] [--quotes=cc] [--no-keypad] [--follow-name] [+ cmd] [++ cmd] [DOUBLEDASH] [filename...]')
    # bg.make_utility('head  [- K] [ -c K<[-]K>] [--bytes=K<[-]K>] [ -n K<[-]K>] [ --lines=K<[-]K> ] [ -q | --quiet | --silent ] [ -v | --verbose ] [ --help ] [ --version ] [FILE...]')