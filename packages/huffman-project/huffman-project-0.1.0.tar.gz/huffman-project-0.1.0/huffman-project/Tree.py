from .Node import Node


class Tree():
    def __init__(self, frequency):
        list_nodes = [
            Node(weight, character) for character, weight in frequency.items()]

        while len(list_nodes) > 1:
            list_nodes = sorted(list_nodes, key=lambda x: x.get_weight())
            left_node = list_nodes.pop(0)
            right_node = list_nodes.pop(0)
            parent_node = Node(
                left_node.get_weight() + right_node.get_weight())
            parent_node.setChildren(left_node, right_node)
            list_nodes.append(parent_node)

        self.root = list_nodes[0]

    """Get root Node of Tree

    Returns:
        Node: root node
    """
    def get_root(self):
        return self.root
