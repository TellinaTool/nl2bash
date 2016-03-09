#!/usr/bin/env python

from __future__ import print_function
from collections import namedtuple
import collections
import os
import json
import sys

# given a number num, generate space of size length
def indent_count_to_string(num):
    s = ""
    for i in range(0, num):
        s = s + "  "
    return s

# the AST for the command line structure
class Program(object):
    def __init__(self, commands):
        self.commands = commands
        for cmd in self.commands:
            setattr(cmd, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Program]" + "\n"
        for c in self.commands:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

class Cmd(object):
    def __init__(self, name, option):
        self.name = name
        self.option = option
        setattr(self.option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Cmd] " + self.name + "\n"
        result = result +  self.option.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

class FlagOp(object):
    def __init__(self, name):
        self.name = name
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[FlagOp] " + self.name
        return result

class LongFlagOp(object):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
        if (not self.arg == None):
            setattr(self.arg, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[LongFlagOp] " + self.name + "\n"
        if (not self.arg == None):
            result = result + self.arg.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

class ArgOp(object):
    def __init__(self, name, ty, is_list):
        self.name = name
        self.ty = ty
        self.is_list = is_list
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[ArgOp] " + self.name 
        return result.rstrip()

class OptionalOp(object):
    def __init__(self, option):
        self.option = option
        setattr(self.option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[OptionalOp]" + "\n"
        result = result + self.option.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

class SeqOp(object):
    def __init__(self, options):
        self.options = options
        for option in self.options:
            setattr(option, "parent", self.options)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[SeqOp]" + "\n" 
        for c in self.options:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

class CaseOp(object):
    def __init__(self, options):
        self.options = options
        for option in self.options:
            setattr(option, "parent", self.options)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[CaseOp]" + "\n"
        for c in self.options:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()

def load_syntax(json_files):
    simple_cmds = []
    counts = collections.defaultdict(int)
    for jsonfile in json_files:
        print("loading from {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        for cmd in syntax:
            c = make_grammar_from_json_syntax(cmd)
            simple_cmds.append(c)
            counts[cmd["name"]] += 1
            print(" > loaded {} ({})".format(cmd["name"], counts[cmd["name"]]))
    return Program(simple_cmds)

def make_grammar_from_json_syntax(syntax):
    g = Cmd(name=syntax["name"], option=make_grammar_from_options(syntax["option"]))
    return g

def make_grammar_from_options(x):
    if x["type"] == "compound_options":
        return SeqOp([make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "optional_option":
        return OptionalOp(make_grammar_from_options(x["cmd"]))
    elif x["type"] == "exclusive_options":
        return CaseOp([make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "flag_option":
        return FlagOp(x["flag_name"])
    elif x["type"] == "long_flag_option":
        g = LongFlagOp(x["flag_name"], None)
        if x["arg_exists"]:
            if x["arg_optional"]:
                setattr(g, "arg", OptionalOp(make_grammar_from_options(x["argument"])))
            else:
                setattr(g, "arg", make_grammar_from_options(x["argument"]))
        return g
    elif x["type"] == "argument_option":
        return ArgOp(x["arg_name"], x["arg_type"], x["isList"])
    else:
        raise Exception("unknown type: {}".format(x["type"]))
    return g

if __name__ == "__main__":
    simple_grammar = load_syntax([os.path.join(os.path.dirname(__file__), "..", "data", "primitive_cmds_grammar.json")])
    #print (simple_grammar.pretty_print(0))
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
