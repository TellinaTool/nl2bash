"""
Node Classes for the Normalized Bash AST.
"""

right_associate_unary_logic_operators \
    = set([
        '!',
        '-not'
    ])
left_associate_unary_logic_operators \
    = set([
        '-prune'
    ])

binary_logic_operators \
    = set([
        '-and',
        '-or',
        '||',
        '&&',
        '-o',
        '-a'
    ])

def make_parent_child(parent, child):
    parent.add_child(child)
    child.parent = parent

def make_sibling(lsb, rsb):
    if lsb:
        lsb.rsb = rsb
    if rsb:
        rsb.lsb = lsb

class Node(object):
    num_child = -1      # default value = -1, allow arbitrary number of children
    children_types = [] # list of children types

    def __init__(self, parent=None, lsb=None, kind="", value=""):
        """
        :member parent: pointer to parent node
        :member lsb: pointer to left sibling node
        :member rsb: pointer to right sibling node
        :member kind: ['pipe',
                      'headcommand',
                      'unarylogicop',
                      'binarylogicop'
                      'flag',
                      'argument',
                      'commandsubstitution',
                      'processsubstitution'
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

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

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

    def is_reserved(self):
        if self.kind != "argument":
            return True

    def is_command(self, value):
        return self.kind == "headcommand" and self.value == value

    def is_headcommand(self):
        return self.kind == "headcommand"

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
    def symbol(self):
        return self.kind.upper() + "_" + self.value

    @property
    def grandparent(self):
        return self.parent.parent

class ArgumentNode(Node):
    num_child = 0

    def __init__(self, value="", arg_type="", parent=None, lsb=None):
        super(ArgumentNode, self).__init__(parent, lsb, "argument", value)
        self.arg_type = arg_type

    def get_head_command(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

    def is_reserved(self):
        return self.arg_type == "ReservedWord"

class FlagNode(Node):
    def __init__(self, value="", parent=None, lsb=None):
        super(FlagNode, self).__init__(parent, lsb, "flag", value)

    def get_head_command(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

class HeadCommandNode(Node):
    def __init__(self, value="", parent=None, lsb=None):
        super(HeadCommandNode, self).__init__(parent, lsb, "headcommand", value)

    def get_head_command(self):
        return self

class UnaryLogicOpNode(Node):
    num_child = 1
    children_types = [set('flag')]
    LEFT = 0
    RIGHT = 1

    def __init__(self, value="", parent=None, lsb=None):
        super(UnaryLogicOpNode, self).__init__( parent, lsb, 'unarylogicop', value)
        if value in right_associate_unary_logic_operators:
            self.associate = UnaryLogicOpNode.RIGHT
        elif value in left_associate_unary_logic_operators:
            self.associate = UnaryLogicOpNode.LEFT
        else:
            raise ValueError("Unrecognized unary logic operator: {}".format(value))

    def get_head_command(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

class BinaryLogicOpNode(Node):
    num_child = 2
    children_types = [set('flag'), set('flag')]

    def __init__(self, value="", parent=None, lsb=None):
        super(BinaryLogicOpNode, self).__init__(parent, lsb, 'binarylogicop', value)

    def get_head_command(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

class RedirectNode(Node):
    num_child = 2

    def __init__(self, value="", parent=None, lsb=None):
        super(RedirectNode, self).__init__(parent, lsb, 'redirect', value)

class PipelineNode(Node):
    children_types = [set(['headcommand'])]

    def __init__(self, parent=None, lsb=None):
        super(PipelineNode, self).__init__(parent, lsb, 'pipeline')

class CommandSubstitutionNode(Node):
    num_child = 1
    children_types = [set(['pipe', 'headcommand'])]

    def __init__(self, parent=None, lsb=None):
        super(CommandSubstitutionNode, self).__init__(parent, lsb)
        self.kind = "commandsubstitution"

class ProcessSubstitutionNode(Node):
    num_child = 1
    children_types = [set(['pipe', 'headcommand'])]

    def __init__(self, value, parent=None, lsb=None):
        super(ProcessSubstitutionNode, self).__init__(parent, lsb)
        self.kind = "processsubstitution"
        if value in ["<", ">"]:
            self.value = value
        else:
            raise ValueError("Value of a processsubstitution has to be '<' or '>'.")

