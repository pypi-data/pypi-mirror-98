from ..abstractions.Comparable import *


class BinaryTreeNode(Comparable):
    '''
    Basic node of a basic binary tree.
    '''

    def diff(self, other):
        return signum(self.value, other.value)

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        return

    def compare(self, value, getDirection=False):
        X = self.left if value > self.value else self.right
        return (X, value > self.value) if getDirection else X


class BinaryTree:
    """
    Basic binary tree.
    """

    def __init__(self, nodeType=BinaryTreeNode):
        self.nodeType = nodeType
        self.root: (BinaryTreeNode, None) = None
        self.size = 0
        return

    # -------------------------------------------------------------------------
    # The following functions do not change the data structure.
    def make_node(self, value):
        return self.nodeType(value)

    def __sizeof__(self):
        return self.size

    def __contains__(self, item):
        current = self.root
        while current is not None:
            current: BinaryTreeNode
            if current.value == item:
                return True
            current = current.compare(item)
        return False

    def get(self, item):
        current = self.root
        while current is not None:
            current: BinaryTreeNode
            if current.value == item:
                return current
            current = current.compare(item)
        return False

    # -------------------------------------------------------------------------
    # The following functions DO change the data structure.
    def insert(self, value, log: list = None):
        if self.root is None:
            self.root = self.make_node(value)
            self.size = 1
            return
        current: BinaryTreeNode = self.root
        last: BinaryTreeNode = self.root
        lastJump: bool = False
        while current is not None:
            last = current
            X = last.compare(value, True)
            last = X[0]
            lastJump = X[1]
            if log is not None:
                log.append((last, X[1]))
        new: BinaryTreeNode = self.make_node(value)
        if lastJump:
            last.right = new
        else:
            last.left = new
        return

    def remove(self, value):
        return
