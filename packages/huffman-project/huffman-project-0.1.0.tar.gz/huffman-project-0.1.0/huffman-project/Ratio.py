class Ratio():
    """Get informations (statistics) on compression
    """
    def __init__(self, frequency, encodage_table):
        self.frequency = frequency
        self.encodage_table = encodage_table

    def getRatio(self):
        """Determine the compression ratio

        Returns:
            float: compression ratio
        """
        nbChars = 0
        compressedBits = 0
        for char in self.frequency.items():
            nbChars += char[1]
            compressedBits += char[1]*len(self.encodage_table[char[0]])

        originalBits = nbChars * 8
        return 1 - compressedBits / originalBits

    def getAveragageBitsForChar(self) -> float:
        """Average number of storage bits of a character in the compressed text

        Returns:
            float: average bits for one char
        """
        bitsForChar = []

        for char in self.encodage_table.values():
            bitsForChar.append(len(char))

        return sum(bitsForChar)/len(bitsForChar)
