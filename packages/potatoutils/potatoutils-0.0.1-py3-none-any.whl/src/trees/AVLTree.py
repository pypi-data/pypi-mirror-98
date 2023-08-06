from .BinaryTree import *


class AVLNode(BinaryTreeNode):
    def __init__(self, value):
        super(AVLNode, self).__init__(value)
        self.depth = 0


class AVLTree(BinaryTree):
    def __init__(self):
        super(AVLTree, self).__init__(AVLNode)
        return

    def insert(self, value, log: list = None):
        super(AVLTree, self).insert(value, log)
        return