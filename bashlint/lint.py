#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Parse the option list of a bash command and assign each argument a type.

Output a Bashlex (https://github.com/idank/bashlex) AST augmented with the
following syntactic sugars:
    1. every token is linked to its corresponding attach point:
        flag -> utility,
        argument -> utility,
        argument -> flag;
    2. the arguments are decorated with semantic types.

Report syntactic errors and wrong flag usages if there is any.

Related repository:
    - Bashlex (https://github.com/idank/bashlex)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import os
import re
import sys
if sys.version_info > (3, 0):
    from six.moves import xrange

# bash grammar
from bashlint.grammar import *
bash_grammar = BashGrammar()

# bashlex stuff
from bashlint import bash, bast, errors, tokenizer, bparser
from bashlint.nast import *

from nlp_tools import constants


def correct_errors_and_normalize_surface(cmd):
    # special normalization for certain commands
    ## remove all "sudo"'s
    cmd = cmd.replace("sudo", "")

    ## normalize utilities called with full path
    cmd = cmd.replace("/usr/bin/find", "find")
    cmd = cmd.replace("/bin/find", "find")
    cmd = cmd.replace("/usr/bin/grep", "grep")
    cmd = cmd.replace("/bin/rm", "rm")
    cmd = cmd.replace("/bin/mv", "mv")
    
    ## correct common typos
    cmd = cmd.replace("'{}'", "{}")
    cmd = cmd.replace("\"{}\"", "{}")
    cmd = cmd.replace("-i{}", "-I {}")
    cmd = cmd.replace("-i%", "-I %")
    cmd = cmd.replace("-I{}", "-I {}")
    cmd = cmd.replace(" [] ", " {} ")
    cmd = cmd.replace("-L.", "-L")
    cmd = cmd.replace("-mitime", "-mtime")
    cmd = cmd.replace("-dev", "-xdev")
    cmd = cmd.replace("-regex-type", "-regextype")
    cmd = cmd.replace(" ( ", " \\( ")
    cmd = cmd.replace(" ) ", " \\) ")
    cmd = cmd.replace("-\\(", "\\(")
    cmd = cmd.replace("-\\)", "\\)")
    cmd = cmd.replace("\"\\)", " \\)")
    cmd = cmd.replace("\\(-", "\\( -")
    cmd = cmd.replace("e\\)", "e \\)")
    cmd = cmd.replace("-\\!", "!")
    try:
        cmd = cmd.replace("— ", "-")
        cmd = cmd.replace("–", "-")
        cmd = cmd.replace("—", "-")
        cmd = cmd.replace("“", '"')
        cmd = cmd.replace("”", '"')
        cmd = cmd.replace("-\xd0\xbe", "-o")
        cmd = cmd.replace("\xe2\x80\x93 ", "-")
        cmd = cmd.replace('‘', '\'')
        cmd = cmd.replace('’', '\'')
    except UnicodeDecodeError:
        cmd = cmd.replace("— ".decode('utf-8'), "-")
        cmd = cmd.replace("–".decode('utf-8'), "-")
        cmd = cmd.replace("—".decode('utf-8'), "-")
        cmd = cmd.replace("“".decode('utf-8'), '"')
        cmd = cmd.replace("”".decode('utf-8'), '"')
        cmd = cmd.replace("\xd0\xbe".decode('utf-8'), "o")
        cmd = cmd.replace("\xe2\x80\x93 ".decode('utf-8') , "-")
        cmd = cmd.replace('‘'.decode('utf-8'), '\'')
        cmd = cmd.replace('’'.decode('utf-8'), '\'')

    # more typo fixes
    cmd = re.sub("-prin($| )", '-print', cmd)
    cmd = cmd.replace("/bin/echo", "echo")
    cmd = cmd.replace(" exec sed ", " -exec sed ")
    cmd = cmd.replace(" xargs -iname ", " xargs ")
    cmd = cmd.replace(" -chour +1 ", " -cmin 60 ")
    cmd = cmd.replace(" -target-directory ", " --target-directory=")
    cmd = cmd.replace("- perm", "-perm")
    cmd = cmd.replace(" perm", " -perm")
    cmd = cmd.replace("'-rd\\n' ", '')

    ## remove shell character
    if cmd.startswith("$ "):
        cmd = re.sub("^\$ ", '', cmd)
    if cmd.startswith("# "):
        cmd = re.sub("^\# ", '', cmd)
    if cmd.startswith("$find "):
        cmd = re.sub("^\$find ", "find ", cmd)
    if cmd.startswith("#find "):
        cmd = re.sub("^\#find ", "find ", cmd)

    ## the first argument of "tar" is always interpreted as an option
    tar_fix = re.compile(' tar \w')
    if cmd.startswith('tar'):
        cmd = ' ' + cmd
    for w in re.findall(tar_fix, cmd):
        cmd = cmd.replace(w, w.replace(' tar ', ' tar -'))
    cmd = cmd.strip()
    return cmd

def attach_to_tree(node, parent):
    node.parent = parent
    node.lsb = parent.get_right_child()
    parent.add_child(node)
    if node.lsb:
        node.lsb.rsb = node

def detach_from_tree(node, parent):
    if not parent:
        return
    parent.remove_child(node)
    node.parent = None
    if node.lsb:
        node.lsb.rsb = node.rsb
    if node.rsb:
        node.rsb.lsb = node.lsb
    node.rsb = None
    node.lsb = None

def safe_bashlex_parse(cmd):
    try:
        tree = bparser.parse(cmd)
    except tokenizer.MatchedPairError:
        print("Cannot parse: %s - MatchedPairError" % cmd)
        return None
    except errors.ParsingError:
        print("Cannot parse: %s - ParsingError" % cmd)
        return None
    except NotImplementedError:
        print("Cannot parse: %s - NotImplementedError" % cmd)
        return None
    except IndexError:
        print("Cannot parse: %s - IndexError" % cmd)
        # empty command
        return None
    except AttributeError:
        print("Cannot parse: %s - AttributeError" % cmd)
        # not a bash command
        return None
    except AssertionError:
        print("Cannot parse: %s - AssertionError" % cmd)
        # not a bash command
        return None
    except TypeError:
        print("Cannot parse: %s - AssertionError" % cmd)
        return None
    if len(tree) > 1:
        print("Doesn't support command with multiple root nodes: %s" % cmd)
        return None
    return tree

def normalize_ast(cmd, recover_quotes=True, verbose=False):
    """
    Convert the bashlex parse tree of a command into the normalized form.

    :param cmd: bash command to parse
    :param recover_quotes: if set, retain quotation marks in the command
    :param verbose: if set, print error message.
    :return normalized_tree
    """
    cmd = cmd.replace('\n', ' ').strip()
    cmd = correct_errors_and_normalize_surface(cmd)
    if not cmd:
        return None

    def node_with_quotes(node):
        return cmd[node.pos[0]] in ['"', '\''] \
            or cmd[node.pos[1]-1] in ['"', '\'']

    def recover_node_quotes(node):
        if node_with_quotes(node):
            return cmd[node.pos[0] : node.pos[1]]
        else:
            return node.word

    def normalize_word(node, recover_quotes):
        w = recover_node_quotes(node) if recover_quotes else node.word
        return w

    def normalize_argument(node, current, arg_type):
        value = normalize_word(node, recover_quotes)
        norm_node = ArgumentNode(value=value, arg_type=arg_type)
        attach_to_tree(norm_node, current)
        return norm_node

    def match(state, token):
        """
        Match a token with a grammar state and output the most likely match result.

        :param state: A grammar state as defined in BashGrammar.
        :param token: A token from the input sequence.
        :return: A dictionary specifying the most likely match result; None if the
            state and token do not match.
        """

    def normalize_command(node, current=None):
        if not node or not node.parts:
            return
        input = node.parts
        num_tokens = len(node.parts)

        token = input[0]
        head = UtilityNode(token, parent=current, lsb=current.get_right_child())
        if current:
            current.add_child(head)

        if not bash_grammar.consume(token):
            print("Warning: grammar not found - utility {}".format())
            for token in input[1:]:
                if token.startswith('-'):
                    child = FlagNode(token, parent=head, lsb=head.get_right_child())
                else:
                    child = ArgumentNode(token, arg_type='Unknown', parent=head,
                                         lsb=head.get_right_child())
                head.add_child(child)
        else:
            current = head
            i = 1
            while i < len(input):
                token = input[i]

                command_quote_missing_flag = False
                error_in_subcommand_flag = False

                # examine possible next states in order
                for next_state in bash_grammar.next_states:
                    matched = False
                    if next_state.is_flag():
                        try:
                            result = bash_grammar.push(token, next_state.type)
                            #                                 FLAG_S
                        except ValueError as e:
                            raise errors.FlagError(e, num_tokens, i)
                        if result:
                            for flag_token, flag_arg in result:
                                flag = FlagNode(flag_token, parent=current,
                                                lsb=current.get_right_child())
                                current.add_child(flag)
                                if flag_arg == '__OPEN__':
                                    # Incomplete AST, expecting flag argument
                                    current = flag
                                elif flag_arg is not None:
                                    # Argument is specified with flag
                                    argument = ArgumentNode(flag_arg, parent=flag,
                                                            lsb=flag.get_right_child())
                                    flag.add_child(argument)
                            matched = True
                            break
                    elif next_state.is_command():
                        # Nested bash command
                        new_command_node = bast.node(
                            kind="command", word="", parts=[], pos=(-1,-1))
                        if next_state.type == COMMAND_S:
                            # Interpret all of the rest of the tokens as content of the nested command
                            new_command_node.parts = input[i:]
                            normalize_command(new_command_node, current)
                            bash_grammar.push('', next_state.type)
                            i = len(input)
                        elif next_state.type == ARG_COMMAND_S:
                            if not constants.with_quotes(token):
                                command_quote_missing_flag = True
                            tree = safe_bashlex_parse(token[1:-1])
                            if tree is None:
                                error_in_subcommand_flag = True
                            normalize(tree[0], current)
                            bash_grammar.push(token, next_state.type)
                            i += 1
                        else:
                            new_input = []
                            j = i
                            while j < len(input) and not (input[j] in next_state.stop_tokens):
                                new_input.append(input[j])
                            new_command_node.parts = new_input
                            normalize_command(new_input, current)
                            if j < len(input):
                                current.value += ('::' + input[j])
                            else:
                                print("Warning: -exec missing stop token - ; added")
                            bash_grammar.push(input[j], next_state.type)
                            #                           EXEC_COMMAND_S
                            i = j + 1
                        matched = True
                        break
                    elif next_state.is_argument():
                        command_quote_missing_flag = False
                        error_in_subcommand_flag = False
                        argument = ArgumentNode(token, arg_type=next_state.arg_type,
                                                parent=current, lsb=current.get_right_child())
                        current.add_child(argument)
                        bash_grammar.push(token, next_state.type)
                        #                        ARG_S
                        matched = True
                        break

                if not matched:
                    if command_quote_missing_flag:
                        raise errors.SubCommandError('Missing quotes around command string: {}'.format(token),
                                                     num_tokens, i)
                    if error_in_subcommand_flag:
                        raise errors.SubCommandError('Error in subcommand string: {}'.format(token),
                                                     num_tokens, i)
                    raise errors.LintParsingError('Unmatched token', num_tokens, i)

            if bash_grammar.allow_eof():
                return
            else:
                raise errors.LintParsingError('Incomplete command', num_tokens, i)

    def normalize(node, current, node_kind="", arg_type=""):
        # recursively normalize each subtree
        if not type(node) is bast.node:
            raise ValueError('type(node) is not ast.node')
        if node.kind == 'word':
            # assign fine-grained types
            if node.parts:
                # Compound arguments
                # commandsubstitution, processsubstitution, parameter
                if node.parts[0].kind == "processsubstitution":
                    if '>' in node.word:
                        norm_node = ProcessSubstitutionNode('>')
                        attach_to_tree(norm_node, current)
                        for child in node.parts:
                            normalize(child, norm_node)
                    elif '<' in node.word:
                        norm_node = ProcessSubstitutionNode('<')
                        attach_to_tree(norm_node, current)
                        for child in node.parts:
                            normalize(child, norm_node)
                elif node.parts[0].kind == "commandsubstitution":
                    norm_node = CommandSubstitutionNode()
                    attach_to_tree(norm_node, current)
                    for child in node.parts:
                        normalize(child, norm_node)
                elif node.parts[0].kind == "parameter" or \
                    node.parts[0].kind == "tilde":
                    normalize_argument(node, current, arg_type)
                else:
                    for child in node.parts:
                        normalize(child, current)
            else:
                normalize_argument(node, current, arg_type)
        elif node.kind == "pipeline":
            norm_node = PipelineNode()
            attach_to_tree(norm_node, current)
            if len(node.parts) % 2 == 0:
                print("Error: pipeline node must have odd number of parts (%d)"
                      % len(node.parts))
                print(node)
                sys.exit()
            for child in node.parts:
                if child.kind == "command":
                    normalize(child, norm_node)
                elif not child.kind == "pipe":
                    raise ValueError(
                        "Error: unrecognized type of child of pipeline node")
        elif node.kind == "list":
            if len(node.parts) > 2:
                # multiple commands, not supported
                raise ValueError("Unsupported: list of length >= 2")
            else:
                normalize(node.parts[0], current)
        elif node.kind == "commandsubstitution" or \
             node.kind == "processsubstitution":
            normalize(node.command, current)
        elif node.kind == "command":
            try:
                normalize_command(node, current)
            except AssertionError:
                raise AssertionError("normalized_command AssertionError")
        elif hasattr(node, 'parts'):
            for child in node.parts:
                # skip current node
                normalize(child, current)
        elif node.kind == "redirect":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "operator":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "parameter":
            # not supported
            raise ValueError("Unsupported: parameters")
        elif node.kind == "compound":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "list":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "for":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "if":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "while":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "until":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "assignment":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "function":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "tilde":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)
        elif node.kind == "heredoc":
            # not supported
            raise ValueError("Unsupported: %s" % node.kind)

    try:
        cmd2 = cmd.encode('utf-8')
    except UnicodeDecodeError:
        cmd2 = cmd

    tree = safe_bashlex_parse(cmd2)
    if tree is None:
        return tree

    normalized_tree = Node(kind="root")
    try:
        normalize(tree[0], normalized_tree)
    except ValueError as err:
        print("%s - %s" % (err.args[0], cmd2))
        return None
    except AttributeError as err:
        print("%s - %s" % (err.args[0], cmd2))
        return None
    except AssertionError as err:
        print("%s - %s" % (err.args[0], cmd2))
        return None

    if len(normalized_tree.children) == 0:
        # parsing not successful if the normalized tree consists of the root
        # node only
        return None

    return normalized_tree