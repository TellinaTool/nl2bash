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
        self.arg_index = {}


class FlagState(BashGrammarState):
    def __init__(self, flag_name, optional):
        super(FlagState, self).__init__(FLAG_S)
        self.flag_name = flag_name
        self.optional = optional
        self.argument = None


class ArgumentState(BashGrammarState):
    def __init__(self, arg_name, arg_type, optional=False, is_list=False,
                 list_separator=None):
        super(ArgumentState, self).__init__(ARG_S)
        self.arg_name = arg_name
        self.arg_type = arg_type
        self.optional = optional
        self.is_list = is_list
        self.list_separator = list_separator


class ArgCommandState(BashGrammarState):
    def __init__(self):
        super(ArgCommandState, self).__init__(ARG_COMMAND_S)


class ExecCommandState(BashGrammarState):
    def __init__(self):
        super(ExecCommandState, self).__init__(EXEC_COMMAND_S)


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

    def add_long_flag(self, utility_state, part):
        if '=' in part:
            flag, arg_name = part.split('=', 1)
            flag = flag.strip()
            arg_name = arg_name.strip()
            if flag.endswith('['):
                flag = flag[:-1]
            if arg_name.endswith(']'):
                arg_name = arg_name[:-1]
                arg_type = self.name2type[arg_name]
                arg = ArgumentState(arg_name, arg_type, optional=True)
            else:
                arg_type = self.name2type[arg_name]
                arg = ArgumentState(arg_name, arg_type)
            utility_state.flag_index[flag] = FlagState()
        else:
            flag = part
            utility_state.flag_index[flag] = None

    def make_grammar(self, input_file):
        """
        Build utility grammar from man-page synopsis.
        """

        with open(input_file) as f:
            content = f.readlines()

        reading_type = False
        reading_synopsis = False

        for line in content:
            if line.strip() == 'type':
                reading_type = True
            elif line.strip() == 'PrimitiveCmd ::=':
                reading_synopsis = True
            elif reading_type:
                type, names = line.strip().split()
                for name in names.split(','):
                    name = name.strip()
                    if not name in self.name2type:
                        self.name2type[name] = type
                    else:
                        raise ValueError('Ambiguity in name type: {} ({} vs. {})'
                                         .format(name, self.name2type[name], type))
            elif reading_synopsis:
                self.make_utility(line)

    def make_utility(self, line):
        line = line.strip()
        if line.startswith('* '):
            line = line[2:]
        utility, synopsis = line.strip().split(' ', 1)
        if not utility in self.grammar:
            u_state = UtilityState(utility)

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
                        self.make_argument(u_state, arg_synopsis)
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
                            self.make_argument(u_state, arg_synopsis.strip(), optional=True)
                            arg_synopsis = ''
                            status = 'IDLE'
                        else:
                            arg_synopsis += c
                    else:
                        arg_synopsis += c
                        if c == '[':
                            stack.append('[')

    def make_argument(self, u_state, synopsis, optional=False):
        if optional:
            print('make_optional_argument: ' + synopsis)
        else:
            print('make_argument: ' + synopsis)

    def make_flag(self, u_state, synopsis, optional=False):
        if optional:
            print('make_optional_flag ' + synopsis)
        else:
            print('make_flag ' + synopsis)

    def make_flag_argument(self, f_state, synopsis, optional=False):
        if optional:
            print('make_optional_flag_argument ' + synopsis)
        else:
            print('make_flag_argument ' + synopsis)


if __name__ == '__main__':
    bg = BashGrammar()
    bg.make_utility('chmod [-R [-H | -L | -P]] [ -c | --changes ] [ -f | --silent | --quiet ] [ -v | --verbose ] [ --no-preserve-root ] [ --preserve-root ] [ -R | --recursive ] [ --help ] [ --version ] MODE[,MODE]... FILE...')
    bg.make_utility('less [-[+]aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX] [-b space] [-h lines] [-j line] [-k keyfile] [-o logfile] [-O logfile] [-p pattern] [-P prompt] [-t tag] [-T tagsfile] [-x n,...] [--tabs=n,...] [-y lines] [--max-forw-scroll=n] [-[z] lines] [--window=n] [-TILDE] [--tilde] [-SHARP shift] [--shift shift] [-X] [--no-init] [--quotes=cc] [--no-keypad] [--follow-name] [+ cmd] [++ cmd] [DOUBLEDASH] [filename...]')
    bg.make_utility('head  [- K] [ -c K<[-]K>] [--bytes=K<[-]K>] [ -n K<[-]K>] [ --lines=K<[-]K> ] [ -q | --quiet | --silent ] [ -v | --verbose ] [ --help ] [ --version ] [FILE...]')