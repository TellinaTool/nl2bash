#!/usr/bin/env python

from __future__ import print_function
from collections import namedtuple
import collections
import os
import json
import sys

def indent_count_to_string(num):
    s = ""
    for i in range(0, num):
        s = s + "  "
    return s

# the AST for the command line structure
class Program(object):
    def __init__(self, commands, parent):
        self.commands = commands
        self.parent = parent
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Program]"
        for c in self.commands:
            result = result + "\n" + c.pretty_print(indent_count + 1)
        return result

class Cmd(object):
    def __init__(self, name, option, parent):
        self.name = name
        self.option = option
        self.parent = parent
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Cmd] " + self.name
        if (not self.option == None):
            result = result + "\n" + self.option.pretty_print(indent_count + 1)
        return result

class FlagOp(object):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[FlagOp]"
        result = result + "\n" + indent + self.name + "  " + self.arg
        return result

class ArgOp(object):
    def __init__(self, name, is_list):
        self.name = name
        self.is_list = is_list
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[ArgOp]"
        result = result + "\n" + indent + self.name
        return result

class OptionalOp(object):
    def __init__(self, option):
        self.option = option
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[OptionalOp]"
        result = result + "\n" + option.pretty_print(indent_count + 1)
        return result

class SeqOp(object):
    def __init__(self, options):
        self.options = options
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[SeqOp]"
        for c in options:
            result = result + "\n" + c.pretty_print(indent_count + 1)
        return result

class CaseOp(object):
    def __init__(self, options):
        self.options = options
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[CaseOp]"
        for c in options:
            result = result + "\n" + c.pretty_print(indent_count + 1)
        return result

'''
def load_syntax(json_files):
    simple_cmds = []
    counts = collections.defaultdict(int)
    for jsonfile in json_files:
        print("loading from {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        for cmd in syntax:
            simple_cmds.append(make_grammar_from_json_syntax(cmd))
            counts[cmd["name"]] += 1
            print(" --> loaded {} ({})".format(cmd["name"], counts[cmd["name"]]))
    return Grammar(Grammar.CASES, *simple_cmds)

def make_full_grammar(simple_grammar, max_pipeline_depth):
    pipe = Grammar(Grammar.EXACT, "|")
    def make_pipeline(g, n):
        return Grammar(Grammar.SEQ, g, *([Grammar(Grammar.SEQ, pipe, g)] * n))

    grammar = simple_grammar
    for n in range(max_pipeline_depth + 1):
        grammar = Grammar(Grammar.CASES, grammar, make_pipeline(simple_grammar, n))
    return grammar
'''

def load_syntax(json_files):
    simple_cmds = []
    counts = collections.defaultdict(int)
    for jsonfile in json_files:
        print("loading from {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        for cmd in syntax:
            simple_cmds.append(make_grammar_from_json_syntax(cmd))
            counts[cmd["name"]] += 1
            print(" > loaded {} ({})".format(cmd["name"], counts[cmd["name"]]))
    return Program(simple_cmds, parent=None)

def make_grammar_from_json_syntax(syntax):
    g = Cmd(name=syntax["name"], option=None, parent=None)
    g.options = make_grammar_from_options(syntax["option"])
    return g

def make_grammar_from_options(x):
    if x["type"] == "compound_options":
        return SeqOp([make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "optional_option":
        return OptionalOp(Grammar.CASES, Grammar(Grammar.EMPTY), make_grammar_from_options(x["cmd"]))
    elif x["type"] == "exclusive_options": # sic
        return Grammar(Grammar.CASES, *[make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "flag_option":
        g = Grammar(Grammar.EXACT, "-" + x["flag_name"])
    elif x["type"] == "long_flag_option":
        g = Grammar(Grammar.EXACT, "--" + x["flag_name"])
    elif x["type"] == "argument_option":
        return Grammar(Grammar.HOLE) # TODO: record type, description, etc...
    else:
        raise Exception("unknown type: {}".format(x["type"]))

    # has arg?
    if "arg_exists" in x and x["arg_exists"]:
        g = Grammar(Grammar.SEQ, g, make_grammar_from_options(x["argument"]))
    return g



if __name__ == "__main__":
    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__), "..", "data", "primitive_cmds_grammar.json")])
    print (simple_grammar.pretty_print(0))
    '''
    grammar = make_full_grammar(simple_grammar, max_pipeline_depth=3)

    e = Enumerator(grammar)
    while True:
        choices = list(e.legal_tokens())
        if Enumerator.HOLE in choices:
            choices.remove(Enumerator.HOLE)
            choices.append("*")
        if Enumerator.EOF in choices:
            choices.remove(Enumerator.EOF)
            choices.append("<EOF>")
        print("choices: {}".format(", ".join(choices)))
        try:
            inp = raw_input("> ")
            if inp == "*":
                inp = Enumerator.HOLE
            e.push(inp)
        except EOFError as ex:
            break
    e.push(Enumerator.EOF)
    '''
