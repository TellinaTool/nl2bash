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
COMPOUND_FLAG_S = 1
FLAG_S = 2
COMMAND_S = 3
ARG_COMMAND_S = 4
EXEC_COMMAND_S = 5
ARG_S = 6
EOF_S = 7


class BashGrammarState(object):
    def __init__(self, type):
        self.type = type

    def get_utility(self):
        cur = self
        while (cur):
            if cur.is_utility():
                return cur
            cur = cur.parent
        raise ValueError('No utility state found')

    def is_argument(self):
        return self.type == ARG_S

    def is_command(self):
        return self.type == COMMAND_S \
               or self.type == ARG_COMMAND_S \
               or self.type == EXEC_COMMAND_S

    def is_compound_flag(self):
        return self.type == COMPOUND_FLAG_S

    def is_flag(self):
        return self.type == FLAG_S

    def is_utility(self):
        return self.type == UTIL_S

    def is_eof(self):
        return self.type == EOF_S


class UtilityState(BashGrammarState):
    def __init__(self, name):
        super(UtilityState, self).__init__(UTIL_S)
        self.name = name
        self.compound_flag = CompoundFlagState(self)
        self.positional_arguments = []
        self.eof = EOFState()

    def add_flag(self, flag):
        self.compound_flag.add_flag(flag)

    def add_positional_argument(self, arg):
        self.positional_arguments.append(arg)
        arg.parent = self

    def next_states(self):
        next_states = [self.compound_flag]
        for arg_state in self.positional_arguments:
            if not arg_state.filled or arg_state.is_list:
                next_states.append(arg_state)
        next_states.append(self.eof)
        return next_states

    def serialize(self):
        header = self.name
        header += ' ' + self.compound_flag.serialize()
        for arg in self.positional_arguments:
            header += ' ' + arg.serialize()
        return header


class CompoundFlagState(BashGrammarState):
    def __init__(self, parent):
        super(CompoundFlagState, self).__init__(COMPOUND_FLAG_S)
        self.parent = parent
        self.flag_index = {}

    def add_flag(self, flag):
        self.flag_index[flag.flag_name] = flag
        flag.parent = self

    def serialize(self):
        header = ''
        for flag in sorted(self.flag_index.keys()):
            header += ' ' + self.flag_index[flag].serialize()
        return header


class FlagState(BashGrammarState):
    def __init__(self, flag_name, optional):
        super(FlagState, self).__init__(FLAG_S)
        self.flag_name = flag_name
        self.optional = optional
        self.parent = None
        self.argument = None

    def add_argumet(self, argument):
        self.argument = argument
        argument.parent = self

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
        :member regex_format: Pattern which specifies the structure to parse
            the argument.
        :member filled: If set, at least
        """
        super(ArgumentState, self).__init__(ARG_S)
        self.arg_name = arg_name
        self.arg_type = arg_type
        self.optional = optional
        self.is_list = is_list
        self.list_separator = list_separator
        self.regex_format = regex_format
        self.filled = False
        self.parent = None

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


class EOFState(BashGrammarState):
    def __init__(self):
        super(EOFState, self).__init__(EOF_S)


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
            print(utility_state.serialize())
            self.next_states = utility_state.next_states()
            return True
        else:
            return False

    def push(self, token, state_type):
        state = self.get_next_state(state_type)
        if state_type == COMPOUND_FLAG_S:
            if token.startswith('--'):
                # long option
                if '=' in token:
                    flag_token, flag_arg = token.split('=', 1)
                else:
                    flag_token, flag_arg = token, ''
                if flag_token in state.flag_index:
                    flag_state = state.flag_index[flag_token]
                    if flag_state.argument:
                        arg_state = flag_state.argument
                        if not flag_arg:
                            self.next_states = [arg_state]
                            return [(flag_token, '__OPEN__')]
                        else:
                            return [(flag_token, (flag_arg, arg_state.arg_type))]
                    else:
                        if not flag_arg:
                            return [(flag_token, None)]
                        else:
                            raise ValueError('Unexpected flag argument "{}"'.format(token))
                else:
                    raise ValueError('Unrecognized long flag "{}"'.format(flag_token))
            elif token in state.flag_index:
                flag_token = token
                state = state.flag_index[flag_token]
                if state.argument:
                    self.next_states = [state.argument]
                    return [(flag_token, '__OPEN__')]
                else:
                    return [(flag_token, None)]
            else:
                flag_token = token[:2]
                if flag_token in state.flag_index:
                    if flag_token in state.flag_index:
                        # Case 1: argument follows flag
                        flag_state = state.flag_index[flag_token]
                        flag_arg = token[2:]
                        print(flag_arg)
                        if flag_state.argument:
                            arg_state = flag_state.argument
                            return [(flag_token, (flag_arg, arg_state.arg_type))]
                        else:
                            raise ValueError('Unexpected flag argument "{}"'.format(flag_arg))
                    elif len(flag_token) > 2 and flag_token.startswith('-'):
                        flag_list = [(flag_token, None)]
                        # Case 2: multiple flags specified at the same time
                        for j in xrange(2, len(token)):
                            flag_token = '-' + token[j]
                            if flag_token in state.flag_index:
                                flag_list.append((flag_token, None))
                            else:
                                raise ValueError('Unrecognized flag "{}"'.format(flag_token))
                        return flag_list
                else:
                    # Case 3: argument specified with just '-'
                    if flag_token.startswith('-') and '-' in state.flag_index \
                            and state.flag_index['-'].argument:
                        flag_arg = token[1:]
                        arg_state = state.flag_index['-'].argument
                        return [('-', (flag_arg, arg_state.arg_type))]
                    else:
                        # Case 4: the token does not match any flag state
                        return None
        elif state_type == COMMAND_S:
            self.next_states = state.get_utility().next_states()
        elif state_type == ARG_COMMAND_S:
            self.next_states = state.get_utility().next_states()
        elif state_type == EXEC_COMMAND_S:
            self.next_states = state.get_utility().next_states()
        elif state.type == ARG_S:
            state.filled = True
            self.next_states = state.get_utility().next_states()

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
                        # print(name, type)
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
        synopsis += ' '
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
        # print(u_state.serialize())

    def make_positional_argument(self, u_state, synopsis, optional=False):
        assert(u_state is not None)
        arg = self.make_argument(synopsis, optional=optional)
        u_state.add_positional_argument(arg)

    def make_flag_argument(self, f_state, synopsis, optional=False):
        assert(f_state is not None)
        f_state.add_argumet(self.make_argument(synopsis, optional=optional))

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
            u_state.add_flag(flag)
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
        flag = None
        if flag_name.endswith('::'):
            # split flags
            flag_prefix = flag_name[0]
            for i in xrange(1, len(flag_name)-2):
                new_flag_name = flag_prefix + flag_name[i]
                flag = FlagState(new_flag_name, optional=optional)
                u_state.add_flag(flag)
        else:
            flag = FlagState(flag_name, optional=optional)
            u_state.add_flag(flag)
        return flag


if __name__ == '__main__':
    bg = BashGrammar()
    bg.make_grammar(os.path.join(os.path.dirname(__file__), '..', 'grammar', 'grammar100.txt'))
    # bg.make_utility('chmod [-R [-H | -L | -P]] [ -c | --changes ] [ -f | --silent | --quiet ] [ -v | --verbose ] [ --no-preserve-root ] [ --preserve-root ] [ -R | --recursive ] [ --help ] [ --version ] MODE[,MODE]... FILE...')
    # bg.make_utility('less [-aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX::] [+aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX::] [-+] [--+] [-b space] [-h lines] [-j line] [-k keyfile] [-o logfile] [-O logfile] [-p pattern] [-P prompt] [-t tag] [-T tagsfile] [-x n,...] [--tabs=n,...] [-y lines] [--max-forw-scroll=n] [-[z] lines] [--window=n] [-TILDE] [--tilde] [-SHARP shift] [--shift shift] [-X] [--no-init] [--quotes=cc] [--no-keypad] [--follow-name] [+ cmd] [++ cmd] [DOUBLEDASH] [filename...]')
    # bg.make_utility('head  [- K] [ -c K<[-]K>] [--bytes=K<[-]K>] [ -n K<[-]K>] [ --lines=K<[-]K> ] [ -q | --quiet | --silent ] [ -v | --verbose ] [ --help ] [ --version ] [FILE...]')