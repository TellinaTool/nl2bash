"""
Node Classes for the Normalized Bash AST.
"""

import collections

from bashlint import bash

_H_NO_EXPAND = '__SP__H_NO_EXPAND'
_V_NO_EXPAND = '__SP__V_NO_EXPAND'

KIND_PREFIX = '<KIND_PREFIX>'


def make_parent_child(parent, child):
    parent.add_child(child)
    child.parent = parent

def make_sibling(lsb, rsb):
    if lsb:
        lsb.rsb = rsb
    if rsb:
        rsb.lsb = lsb

class Node(object):
    num_child = -1          # number of children taken by node
                            # -1 indicates "any number of"
    children_types = []     # list of compatible types of children

    def __init__(self, parent=None, lsb=None, kind="", value=""):
        """
        :member parent: pointer to parent node
        :member lsb: pointer to left sibling node
        :member rsb: pointer to right sibling node
        :member kind: ['pipeline',
                      'utility',
                      'unarylogicop',
                      'binarylogicop'
                      'flag',
                      'root',
                      'argument',
                      'commandsubstitution',
                      'processsubstitution',
                      'bracket'
                     ]
        :member value: string value of the node
        :member children: list of child nodes
        """
        self.parent = parent
        self.lsb = lsb
        self.rsb = None
        self.kind = kind
        self.value = value
        self.children = []

    def add_child(self, child, index=None):
        lsb = self.get_right_child()
        self.children.append(child)
        if lsb:
            lsb.rsb = child

    def get_children(self):
        return self.children

    # node label used for evaluation ONLY
    def get_label(self):
        return self.kind.upper() + "_" + self.value

    def get_left_child(self):
        if len(self.children) >= 1:
            return self.children[0]
        return None

    def get_right_child(self):
        if len(self.children) >= 1:
            return self.children[-1]
        return None

    def get_2nd_right_child(self):
        if len(self.children) >= 2:
            return self.children[-2]
        return None

    def get_num_of_children(self):
        return len(self.children)

    def has_children(self):
        return len(self.children) > 0

    def is_reserved(self):
        if self.kind != "argument":
            return True

    def is_command(self, value):
        return self.kind == "utility" and self.value == value

    def is_utility(self):
        return self.kind == "utility"

    def is_open_vocab(self):
        return False

    def is_option(self):
        return self.kind == "flag"

    def is_argument(self):
        return self.kind == "argument"

    def is_root(self):
        return self.kind == "root"

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def remove_child_by_index(self, index):
        self.children.pop(index)

    def replace_child(self, child, new_child):
        new_child.parent = child.parent
        index = self.children.index(child)
        self.remove_child(child)
        self.children.insert(index, new_child)
        make_sibling(child.lsb, new_child)
        make_sibling(new_child, child.rsb)

    def substitute_parentheses(self, lp, rp, new_child):
        # substitute parenthese expression with single node
        assert(lp.parent == rp.parent)
        new_child.parent = rp.parent
        make_sibling(lp.lsb, new_child)
        make_sibling(new_child, rp.rsb)
        index = self.children.index(lp)
        self.remove_child(lp)
        self.remove_child(rp)
        self.children.insert(index, new_child)
        return index

    @property
    def prefix(self):
        return self.kind.upper() + KIND_PREFIX

    @property
    def symbol(self):
        return self.prefix + self.value

    @property
    def utility(self):
        ancester = self
        while ancester is not None:
            if ancester.kind == "utility":
                return ancester
            # if no parent utility is detect, return "root"
            ancester = ancester.parent
        raise ValueError('No head utility found!')

    @property
    def grandparent(self):
        return self.parent.parent

class UtilityNode(Node):
    def __init__(self, value='', parent=None, lsb=None):
        super(UtilityNode, self).__init__(parent, lsb, "utility", value)
        self.arg_dict = {'': collections.defaultdict(int)}

    def add_child(self, child, index=None):
        super(UtilityNode, self).add_child(child)
        if child.is_argument() and not child.is_bracket():
            # command argument
            self.arg_dict[''][child.arg_type] += 1
            child.set_index(self.arg_dict[''][child.arg_type])

    def get_flags(self):
        flags = []
        for child in self.children:
            if child.is_option():
                flags.append(child)
        return flags

    def get_subcommand(self):
        for child in self.children:
            if child.is_utility():
                return child

class FlagNode(Node):
    def __init__(self, value='', parent=None, lsb=None):
        super(FlagNode, self).__init__(parent, lsb, "flag", value)

    def add_child(self, child, index=None):
        super(FlagNode, self).add_child(child)
        if child.is_argument():
            if not self.value in self.utility.arg_dict:
                self.utility.arg_dict[self.value] \
                    = collections.defaultdict(int)
            self.utility.arg_dict[self.value][child.arg_type] += 1
            child.set_index(
                self.utility.arg_dict[self.value][child.arg_type])

    def get_argument(self):
        for child in self.children:
            if child.kind == "argument":
                return child

    def is_long_option(self):
        return self.value.startswith('--')

class ArgumentNode(Node):
    num_child = 0

    def __init__(self, value='', arg_type='', parent=None, lsb=None,
                 list_members=None, list_separator=None):
        super(ArgumentNode, self).__init__(parent, lsb, "argument", value)
        self.arg_type = arg_type
        self.index = 1
        self.list_separator = list_separator
        self.list_members = list_members

    def is_bracket(self):
        return self.value == "(" or self.value == ")"
    
    def is_reserved(self):
        return self.value in bash.reserved_tokens

    def is_open_vocab(self):
        if self.is_reserved():
            return False
        if self.arg_type == 'Type':
            return False
        if self.arg_type == 'Option':
            return False
        if self.arg_type == 'Format':
            return False
        # if self.arg_type == "Size":
        #     return False
        # if self.arg_type == "Time":
        #     return False
        # if self.arg_type == "Number":
        #     return False
        # if self.arg_type == "Permission":
        #     return False
        return True

    def to_index(self):
        if self.parent.kind == "utility":
            return self.utility.arg_dict[''][self.arg_type] > 1
        else:
            return self.utility.arg_dict[self.parent.value][self.arg_type] > 1

    def set_index(self, ind):
        self.index = ind

class OperatorNode(Node):
    num_child = 0

    def __init__(self, value='', parent=None, lsb=None):
        super(OperatorNode, self).__init__(
            parent, lsb, kind='operator', value=value)

class UnaryLogicOpNode(Node):
    num_child = 1
    children_types = [set(['flag', 'bracket', 'unarylogicop', 'binarylogicop'])]
    LEFT = 0
    RIGHT = 1

    def __init__(self, value='', parent=None, lsb=None):
        super(UnaryLogicOpNode, self).__init__(parent, lsb, 'unarylogicop', value)
        if value in bash.right_associate_unary_logic_operators:
            self.associate = UnaryLogicOpNode.RIGHT
        elif value in bash.left_associate_unary_logic_operators:
            self.associate = UnaryLogicOpNode.LEFT
        else:
            raise ValueError("Unrecognized unary logic operator: {}".format(value))

class BinaryLogicOpNode(Node):
    num_child = -1
    children_types = [set(['flag', 'bracket', 'unarylogicop', 'binarylogicop'])]

    def __init__(self, value='', parent=None, lsb=None):
        super(BinaryLogicOpNode, self).__init__(parent, lsb, 'binarylogicop', value)

class BracketNode(Node):
    num_child = -1
    children_types = [set(['flag', 'bracket', 'unarylogicop', 'binarylogicop'])]

    def __init__(self, parent=None, lsb=None):
        super(BracketNode, self).__init__(parent, lsb, 'bracket', '')

class RedirectNode(Node):
    num_child = 2

    def __init__(self, value='', parent=None, lsb=None):
        super(RedirectNode, self).__init__(parent, lsb, 'redirect', value)

class PipelineNode(Node):
    children_types = [set(['utility'])]

    def __init__(self, parent=None, lsb=None):
        super(PipelineNode, self).__init__(parent, lsb, 'pipeline')

class CommandSubstitutionNode(Node):
    num_child = 1
    children_types = [set(['pipe', 'utility'])]

    def __init__(self, parent=None, lsb=None):
        super(CommandSubstitutionNode, self).__init__(parent, lsb)
        self.kind = "commandsubstitution"

class ProcessSubstitutionNode(Node):
    num_child = 1
    children_types = [set(['pipe', 'utility'])]

    def __init__(self, value, parent=None, lsb=None):
        super(ProcessSubstitutionNode, self).__init__(parent, lsb)
        self.kind = "processsubstitution"
        if value in ["<", ">"]:
            self.value = value
        else:
            raise ValueError("Value of a processsubstitution has to be '<' or '>'.")
