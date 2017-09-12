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

# bashlex stuff
from bashlint import bast, errors, tokenizer, bparser
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


def safe_bashlex_parse(cmd, start_pos=0, verbose=False):
    """
    Call bashlex with all exceptions properly catched.
    """
    def increment_bashlex_tree_offset(tree, offset):
        if tree.kind == 'word':
            tree.pos = (tree.pos[0]+offset, tree.pos[1]+offset)
        if tree.parts:
            for child in tree.parts:
                increment_bashlex_tree_offset(child, offset)
    try:
        tree = bparser.parse(cmd)
        if start_pos > 0:
            increment_bashlex_tree_offset(tree[0], start_pos)
    except tokenizer.MatchedPairError:
        if verbose:
            print("Bashlex cannot parse: %s - MatchedPairError" % cmd)
        return None
    except errors.ParsingError:
        if verbose:
            print("Bashlex cannot parse: %s - ParsingError" % cmd)
        return None
    except NotImplementedError:
        if verbose:
            print("Bashlex cannot parse: %s - NotImplementedError" % cmd)
        return None
    except IndexError:
        if verbose:
            print("Bashlex cannot parse: %s - IndexError" % cmd)
        # empty command
        return None
    except AttributeError:
        if verbose:
            print("Bashlex cannot parse: %s - AttributeError" % cmd)
        # not a bash command
        return None
    except AssertionError:
        if verbose:
            print("Bashlex cannot parse: %s - AssertionError" % cmd)
        # not a bash command
        return None
    except NameError:
        if verbose:
            print("Bashlex cannot parse: %s - NameError" % cmd)
        # not a bash command
        return None
    except TypeError:
        if verbose:
            print("Bashlex cannot parse: %s - AssertionError" % cmd)
        return None
    if len(tree) > 1:
        if verbose:
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

    def is_unary_logic_op(node, parent):
        if node.word == "!":
            return parent and parent.is_command("find")
        return node.word in bash.right_associate_unary_logic_operators \
               or node.word in bash.left_associate_unary_logic_operators

    def is_binary_logic_op(node, parent):
        if node.word == '-o':
            if parent and parent.is_command("find"):
                node.word = "-or"
                return True
            else:
                return False
        if node.word == '-a':
            if parent and parent.is_command("find"):
                node.word = "-and"
                return True
            else:
                return False
        if node.word == ',':
            if parent and parent.is_command("find"):
                node.word = "-and"
                return True
            else:
                return False
        return node.word in bash.binary_logic_operators

    def is_parenthesis(node, parent):
        if node.word in ['(', ')', '\\(', '\\)']:
            if parent and parent.is_command('find'):
                return True
            else:
                return False

    def recover_node_quotes(node):
        return cmd[node.pos[0] : node.pos[1]]

    def normalize_word(node, recover_quotes=True):
        w = recover_node_quotes(node) if recover_quotes else node.word
        return w

    def normalize_argument(node, current, arg_type):
        value = normalize_word(node, recover_quotes)
        norm_node = ArgumentNode(value=value, arg_type=arg_type)
        attach_to_tree(norm_node, current)
        return norm_node

    def normalize_command(node, current=None):
        bash_grammar = BashGrammar()
        bash_grammar.name2type = bg.name2type

        if not node or not node.parts:
            return
        input = node.parts
        num_tokens = len(node.parts)

        bast_node = input[0]
        if bast_node.kind == 'assignment':
            normalize(bast_node, current, 'assignment')
        elif bast_node.kind == 'redirect':
            normalize(bast_node, current, 'redirect')
        elif bast_node.kind == 'commandsubstitution':
            normalize(bast_node, current, 'commandsubstitution')
        elif bast_node.kind == 'word' and not bast_node.parts:
            token = normalize_word(bast_node)
            head = UtilityNode(token, parent=current, lsb=current.get_right_child())
            if current:
                current.add_child(head)

            # If utility grammar is not known, parse into a simple two-level tree
            if not bg.consume(token):
                raise errors.LintParsingError(
                    "Warning: grammar not found - utility {}".format(token), num_tokens, 0)
                for bast_node in input[1:]:
                    if bast_node.kind == 'word' and (not bast_node.parts
                            or (bast_node.parts[0].kind == 'parameter' and
                                bast_node.word.startswith('-'))):
                        token = normalize_word(bast_node)
                        if token.startswith('-'):
                            child = FlagNode(token, parent=head, lsb=head.get_right_child())
                        else:
                            child = ArgumentNode(token, arg_type='Unknown', parent=head,
                                                 lsb=head.get_right_child())
                        head.add_child(child)
                    else:
                        normalize(bast_node, head)
                return

            current, i = head, 1
            bash_grammar.grammar = {head.value: copy.deepcopy(bg.grammar[head.value])}
            bash_grammar.consume(head.value)

            while i < len(input):
                bast_node = input[i]
                # '--': signal the end of options
                if bast_node.kind == 'word' and bast_node.word == '--':
                    op = OperatorNode('--', parent=current, lsb=current.get_right_child())
                    current.add_child(op)
                    bash_grammar.push('--', OPERATOR_S)
                    i += 1
                    continue
                # examine each possible next states in order
                matched = False
                for next_state in bash_grammar.next_states:
                    if next_state.is_compound_flag():
                        # Next state is a flag
                        if bast_node.kind != 'word' or (bast_node.parts and not (
                                bast_node.word.startswith('-') and
                                    bast_node.parts[0].kind == 'parameter')):
                            continue
                        if is_parenthesis(bast_node, current):
                            flag = FlagNode(bast_node.word, parent=current,
                                            lsb=current.get_right_child())
                            current.add_child(flag)
                            matched = True
                            i += 1
                            break
                        elif is_unary_logic_op(bast_node, current):
                            flag = UnaryLogicOpNode(bast_node.word, parent=current,
                                                    lsb=current.get_right_child())
                            current.add_child(flag)
                            matched = True
                            i += 1
                            break
                        elif is_binary_logic_op(bast_node, current):
                            flag = BinaryLogicOpNode(bast_node.word, parent=current,
                                                     lsb=current.get_right_child())
                            current.add_child(flag)
                            matched = True
                            i += 1
                            break
                        else:
                            token = normalize_word(bast_node)
                            try:
                                result = bash_grammar.push(token, COMPOUND_FLAG_S)
                            except ValueError as e:
                                raise errors.FlagError(e.args[0], num_tokens, i)
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
                                        argument = ArgumentNode(flag_arg[0], arg_type=flag_arg[1],
                                            parent=flag, lsb=flag.get_right_child())
                                        flag.add_child(argument)
                                matched = True
                                i += 1
                                break
                    elif next_state.is_command():
                        # Next state is a nested bash command
                        new_command_node = bast.node(
                            kind="command", word="", parts=[], pos=(-1,-1))
                        if next_state.type == ARG_COMMAND_S:
                            if bast_node.kind == 'word' and not bast_node.parts:
                                token = normalize_word(bast_node)
                                if constants.with_quotation(token):
                                    subcommand = token[1:-1]
                                    start_pos = bast_node.pos[0] + 1
                                    tree = safe_bashlex_parse(subcommand, start_pos=start_pos,
                                                              verbose=verbose)
                                    if tree is None:
                                        raise errors.SubCommandError(
                                            'Error in subcommand string: {}'.format(token),
                                            num_tokens, i)
                                    normalize(tree[0], current)
                                    bash_grammar.push(token, next_state.type)
                                    i += 1
                                else:
                                    continue 
                            else:
                                normalize(bast_node, current, 'command')
                                i += 1
                        elif next_state.type == EXEC_COMMAND_S:
                            new_input = []
                            j = i
                            while j < len(input):
                                if hasattr(input[j], 'word') and \
                                        input[j].word in next_state.stop_tokens:
                                    break
                                else:
                                    new_input.append(input[j])
                                    j += 1
                            new_command_node.parts = new_input
                            normalize_command(new_command_node, current)
                            if j < len(input):
                                current.value += ('::' + input[j].word)
                                bash_grammar.push(input[j], EXEC_COMMAND_S)
                            else:
                                if verbose:
                                    print("Warning: -exec missing stop token - ; added")
                                current.value += ('::' + ';')
                                bash_grammar.push(';', EXEC_COMMAND_S)
                            i = j + 1
                        else:
                            # Interpret all of the rest of the tokens as content of the nested command
                            new_command_node.parts = input[i:]
                            normalize_command(new_command_node, current)
                            bash_grammar.push('', next_state.type)
                            i = len(input)
                        current = current.utility
                        matched = True
                        break
                    elif next_state.is_argument():
                        # Next state is an argument
                        if bast_node.kind == 'word' and not bast_node.parts:
                            token = normalize_word(bast_node)
                            if next_state.is_list and next_state.list_separator != ' ':
                                list_separator = next_state.list_separator
                                argument = ArgumentNode(token, arg_type=next_state.arg_type,
                                    parent=current, lsb=current.get_right_child(),
                                    list_members=token.split(list_separator),
                                    list_separator=list_separator)
                            else:
                                argument = ArgumentNode(token, arg_type=next_state.arg_type,
                                    parent=current, lsb=current.get_right_child())
                            current.add_child(argument)
                            status = bash_grammar.push(token, ARG_S)
                        else:
                            normalize(bast_node, current, next_state.arg_type)
                            status = bash_grammar.push('', ARG_S)
                        if status != '__SAME_PARENT__':
                            current = current.utility
                        i += 1
                        matched = True
                        break

                if not matched:
                    if bast_node.kind == 'redirect' or bast_node.kind == 'operator':
                        i += 1
                        matched = True
                    else:
                        raise errors.LintParsingError('Unmatched token', num_tokens, i)

            if bash_grammar.allow_eof():
                post_process_command(head)
                return
            else:
                raise errors.LintParsingError('Incomplete command', num_tokens, i)
        else:
            if bast_node.parts:
                normalize(bast_node, current)
            else:
                raise errors.LintParsingError(
                    'Utility needs to be a BAST node of "Word" type" {}'.format(bast_node),
                    num_tokens, 0)

    def post_process_command(head):
        # process (embedded) parenthese -- treat as implicit "-and"
        def organize_buffer(lparenth, rparenth):
            node = lparenth
            while node != rparenth:
                node = node.rsb
            node = lparenth.rsb
            if node.rsb == rparenth:
                return lparenth.rsb
            else:
                norm_node = BracketNode()
                while node != rparenth:
                    attach_to_tree(node, norm_node)
                    node = node.rsb
                return norm_node

        stack = []
        depth = 0

        def pop_stack_content(depth, rparenth, stack_top=None):
            # popping pushed states off the stack
            popped = stack.pop()
            while (popped.value != "("):
                head.remove_child(popped)
                popped = stack.pop()
            lparenth = popped
            if not rparenth:
                # unbalanced brackets
                rparenth = ArgumentNode(value=")")
                make_parent_child(stack_top.parent, rparenth)
                make_sibling(stack_top, rparenth)
            new_child = organize_buffer(lparenth, rparenth)
            i = head.substitute_parentheses(
                lparenth, rparenth, new_child)
            depth -= 1
            if depth > 0:
                # embedded parenthese
                stack.append(new_child)
            return depth, i

        i = 0
        while i < head.get_num_of_children():
            child = head.children[i]
            if child.value == "(":
                stack.append(child)
                depth += 1
            elif child.value == ")":
                assert(depth >= 0)
                # fix imbalanced parentheses: missing '('
                if depth == 0:
                    # simply drop the single ')'
                    detach_from_tree(child, child.parent)
                else:
                    depth, i = pop_stack_content(depth, child)
            else:
                if depth > 0:
                    stack.append(child)

            i += 1

        # fix imbalanced parentheses: missing ')'
        while (depth > 0):
            depth, _ = pop_stack_content(depth, None, stack[-1])

        assert(len(stack) == 0)
        assert(depth == 0)

        # recover omitted arguments
        if head.value == "find":
            arguments = []
            for child in head.children:
                if child.is_argument():
                    arguments.append(child)
            if head.get_num_of_children() > 0 and len(arguments) < 1:
                norm_node = ArgumentNode(value=".", arg_type="Path")
                make_sibling(norm_node, head.children[0])
                norm_node.parent = head
                head.children.insert(0, norm_node)

        # "grep" normalization
        if head.value == "egrep":
            head.value = "grep"
            flag_present = False
            for child in head.children:
                if child.is_option() and child.value in ["-E", "--extended-regexp"]:
                    flag_present = True
            if not flag_present:
                norm_node = FlagNode(value="-E")
                if head.has_children():
                    make_sibling(norm_node, head.children[0])
                norm_node.parent = head
                head.children.insert(0, norm_node)

        if head.value == "fgrep":
            head.value = "grep"
            flag_present = False
            for child in head.children:
                if child.is_option() and child.value in ["-F", "--fixed-strings"]:
                    flag_present = True
            if not flag_present:
                norm_node = FlagNode(value="-F")
                if head.has_children():
                    make_sibling(norm_node, head.children[0])
                norm_node.parent = head
                head.children.insert(0, norm_node)

        # "xargs" normalization
        def normalize_replace_str(node, r_str, n_str):
            for child in node.children:
                if child.is_argument():
                    if r_str in child.value:
                        child.value = child.value.replace(r_str, n_str)
                        if child.value == n_str:
                            child.arg_type = "ReservedWord"
                else:
                    normalize_replace_str(child, r_str, n_str)

        has_repl_str = False
        if head.value == "xargs":
            for flag in head.get_flags():
                if flag.value == "-I":
                    has_repl_str = True
                    repl_str = flag.get_argument()
                    assert(repl_str is not None)
                    if repl_str.value != "{}":
                        utility = head.get_subcommand()
                        assert(utility is not None)
                        normalize_replace_str(utility, repl_str.value, '{}')
                        repl_str.value = "{}"
                        repl_str.arg_type = "ReservedWord"

            # add -I {} if not present
            utility = head.get_subcommand()
            if not has_repl_str and utility is not None:
                for i in xrange(head.get_num_of_children()):
                    if head.children[i].is_utility():
                        repl_str_flag_node = FlagNode("-I")
                        repl_str_node = ArgumentNode("{}", "ReservedWord")
                        repl_str_node2 = ArgumentNode("{}", "ReservedWord")

                        head.children.insert(i, repl_str_flag_node)
                        repl_str_flag_node.parent = head
                        repl_str_flag_node.lsb = head.children[i-1]
                        head.children[i-1].rsb = repl_str_flag_node

                        make_parent_child(repl_str_flag_node, repl_str_node)
                        sub_command = head.children[i+1]
                        repl_str_node2.parent = sub_command
                        repl_str_node2.lsb = sub_command.get_right_child()
                        sub_command.children.append(repl_str_node2)
                        break

    def normalize(node, current, arg_type=""):
        # recursively normalize each subtree
        if not type(node) is bast.node:
            raise ValueError('type(node) is not bast.node')
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
                elif (node.parts[0].kind == "parameter" or
                      node.parts[0].kind == "tilde"):
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
                raise ValueError("Error: pipeline node must have odd number of parts (%d)"
                      % len(node.parts))
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

    tree = safe_bashlex_parse(cmd, verbose=verbose)
    if tree is None:
        return tree

    normalized_tree = Node(kind="root")
    try:
        normalize(tree[0], normalized_tree)
    except ValueError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None
    except AttributeError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None
    except AssertionError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None
    except errors.SubCommandError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None
    except errors.LintParsingError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None
    except errors.FlagError as err:
        if verbose:
            print("%s - %s" % (err.args[0], cmd))
        return None

    if len(normalized_tree.children) == 0:
        # parsing not successful if the normalized tree consists of the root
        # node only
        return None

    return normalized_tree

def serialize_ast(node, loose_constraints=False, ignore_flag_order=False):
    if not node:
        return ''

    lc = loose_constraints
    ifo = ignore_flag_order

    def to_command_fun(node):
        str = ''
        if node.is_root():
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc:
                for child in node.children:
                    str += to_command_fun(child)
            else:
                str += to_command_fun(node.get_left_child())
        elif node.kind == 'pipeline':
            assert(loose_constraints or node.get_num_of_children() > 1)
            if lc and node.get_num_of_children() < 1:
                str += ''
            elif lc and node.get_num_of_children() == 1:
                str += to_command_fun(node.get_left_child())
            else:
                for child in node.children[:-1]:
                    str += to_command_fun(child)
                    str += ' | '
                str += to_command_fun(node.get_right_child())
        elif node.kind == "commandsubstitution":
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc and node.get_num_of_children() < 1:
                str += ''
            else:
                str += '$('
                str += to_command_fun(node.get_left_child())
                str += ')'
        elif node.kind == 'processsubstitution':
            assert(loose_constraints or node.get_num_of_children() == 1)
            if lc and node.get_num_of_children() < 1:
                str += ''
            else:
                str += '{}('.format(node.value)
                str += to_command_fun(node.get_left_child())
                str += ')'
        elif node.is_utility():
            str += node.value + ' '
            children = sorted(node.children, key=lambda x:x.value) \
                if ifo else node.children
            for child in children:
                str += to_command_fun(child) + ' '
            str = str.strip()
        elif node.is_option():
            assert(loose_constraints or node.parent)
            if '::' in node.value:
                value, op = node.value.split('::')
                str += value + ' '
            else:
                arg_connector = '=' if (node.is_long_option() and
                                        node.children) else ' '
                str += node.value + arg_connector
            for child in node.children:
                str += to_command_fun(child) + ' '
            if '::' in node.value:
                if op == ';':
                    op = "\\;"
                str += op + ' '
            str = str.strip()
        elif node.kind == 'operator':
            str += '--'
        elif node.kind == "binarylogicop":
            assert(loose_constraints or node.get_num_of_children() == 0)
            if lc and node.get_num_of_children() > 0:
                for child in node.children[:-1]:
                    str += to_command_fun(child) + ' '
                    str += node.value + ' '
                str += to_command_fun(node.children[-1])
                str = str.strip()
            else:
                str += node.value
        elif node.kind == "unarylogicop":
            assert(loose_constraints or node.get_num_of_children() == 0)
            if lc and node.get_num_of_children() > 0:
                if node.associate == UnaryLogicOpNode.RIGHT:
                    str += '{} {}'.format(
                        node.value, to_command_fun(node.get_left_child()))
                else:
                    str += '{} {}'.format(
                        to_command_fun(node.get_left_child()), node.value)
            else:
                str += node.value
        elif node.kind == "bracket":
            assert(loose_constraints or node.get_num_of_children() >= 1)
            if lc and node.get_num_of_children() < 2:
                for child in node.children:
                    str += to_command_fun(child)
            else:
                str += "\\( "
                for i in xrange(len(node.children)):
                    str += to_command_fun(node.children[i]) + ' '
                str += "\\)"
        elif node.is_argument():
            assert(loose_constraints or node.get_num_of_children() == 0)
            str += node.value
            if lc:
                for child in node.children:
                    str += to_command_fun(child)
        return str

    return to_command_fun(node)


def get_utility_statistics(utility):
    return len(bg.grammar[utility].compound_flag.flag_index)
