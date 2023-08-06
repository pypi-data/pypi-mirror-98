class Encodage():
    """Class to generate encodage table and use it.
    """
    def __init__(self, node):
        self.table = {}
        self.make_table(node)

    def make_table(self, node, code=""):
        """Using recursivity to generate table for encoding text

        Args:
            node (Node): The node is the root node in the first iteration,
                and after that it is a child node until it reaches a leaf.
            code (str, optional): Defaults to "" in first iteration,
                and is completed by 0 or 1 at each iteration.

        Returns:
            Dict: Binary table for code each characters
        """
        if node.get_char():
            if not code:
                self.table[node.get_char()] = "0"
            else:
                self.table[node.get_char()] = code
            return self.table
        else:
            self.table.update(self.make_table(node.get_left(), code+"0"))
            self.table.update(self.make_table(node.get_right(), code+"1"))
            return self.table

    def get_table(self):
        """Return binary table for code each characters

        Returns:
            Dict: Binary table for code each characters
        """
        return self.table

    def encode(self, text):
        """Encodes the text passed in parameter

        Args:
            text (str): Text to compress

        Returns:
            String: Encoded text
        """
        return "".join([self.get_table()[char] for char in text]).encode()
