class Node():
    """A node is an element with up to 2 children, a leaf has one character.
    """
    def __init__(self, weight, char=None):
        self.left = None
        self.right = None
        self.char = char
        self.weight = weight

    def setChildren(self, left_node, right_node):
        """Define children of Node

        Args:
            left_node (Node): [description]
            right_node (Node): [description]
        """
        self.left = left_node
        self.right = right_node

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_char(self):
        return self.char

    def get_weight(self):
        return self.weight

    def __str__(self):
        return f"char : {self.char} - weight : {self.weight}"
