import bash

right_associate_unary_logic_operators = set(['!', '-not'])

left_associate_unary_logic_operators = set(['-prune'])

def make_parentchild(parent, child):
    parent.addChild(child)
    child.parent = parent

def make_sibling(lsb, rsb):
    if lsb:
        lsb.rsb = rsb
    if rsb:
        rsb.lsb = lsb

class Node(object):
    num_child = -1      # default value = -1, allow arbitrary number of children
    children_types = [] # list of children types
                        # a length-one list of representing the common types for each
                        # child if num_child = -1
                        # dummy field if num_child = 0

    def __init__(self, parent=None, lsb=None, kind="", value=""):
        """
        :member kind: ['pipe',
                      'headcommand',
                      'logicop',
                      'flag',
                      'file', 'pattern', 'numberexp',
                      'sizeexp', 'timeexp', 'permexp',
                      'username', 'groupname', 'unknown',
                      'number', 'unit', 'op',
                      'commandsubstitution',
                      'processsubstitution'
                     ]
        :member value: string value of the node
        :member parent: pointer to parent node
        :member lsb: pointer to left sibling node
        :member children: list of child nodes
        """
        self.parent = parent
        self.lsb = lsb
        self.rsb = None
        self.kind = kind
        self.value = value
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getNumChildren(self):
        return len(self.children)

    def getLeftChild(self):
        if len(self.children) >= 1:
            return self.children[0]
        else:
            return None

    def getRightChild(self):
        if len(self.children) >= 1:
            return self.children[-1]
        else:
            return None

    def getSecond2RightChild(self):
        if len(self.children) >= 2:
            return self.children[-2]
        else:
            return None

    def grandparent(self):
        return self.parent.parent

    def is_simple(self):
        """Check if subtree contains only high-frequency commands."""
        if self.kind == "headcommand" and not self.value in bash.head_commands:
            return False
        for child in self.children:
            if not child.is_simple():
                return False
        return True

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)

    def removeChildByIndex(self, index):
        self.children.pop(index)

    def replaceChild(self, child, new_child):
        new_child.parent = child.parent
        index = self.children.index(child)
        self.removeChild(child)
        self.children.insert(index, new_child)
        make_sibling(child.lsb, new_child)
        make_sibling(new_child, child.rsb)

    def substituteParentheses(self, lp, rp, new_child):
        # substitute parenthese expression with single node
        assert(lp.parent == rp.parent)
        new_child.parent = rp.parent
        make_sibling(lp.lsb, new_child)
        make_sibling(new_child, rp.rsb)
        index = self.children.index(lp)
        self.removeChild(lp)
        self.removeChild(rp)
        self.children.insert(index, new_child)
        return index

    @property
    def symbol(self):
        return self.kind.upper() + "_" + self.value

# syntax constraints for different kind of nodes
class ArgumentNode(Node):
    num_child = 0

    def __init__(self, value="", arg_type="", parent=None, lsb=None):
        super(ArgumentNode, self).__init__(parent, lsb, "argument", value)
        self.arg_type = arg_type

    def getHeadCommand(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

class FlagNode(Node):
    def __init__(self, value="", parent=None, lsb=None):
        super(FlagNode, self).__init__(parent, lsb, "flag", value)

    def getHeadCommand(self):
        ancester = self.parent
        while (ancester.parent and ancester.kind != "headcommand"):
            # if not head command is detect, return "root"
            ancester = ancester.parent
        return ancester

class HeadCommandNode(Node):
    def __init__(self, value="", parent=None, lsb=None):
        super(HeadCommandNode, self).__init__(parent, lsb, "headcommand", value)

    def getHeadCommand(self):
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

    def getHeadCommand(self):
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

    def getHeadCommand(self):
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
