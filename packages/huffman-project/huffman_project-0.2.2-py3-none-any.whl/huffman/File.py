import os


class File():
    """Class to read / write files
    """
    def __init__(self, path):
        self.path = path

    def read(self):
        """Read file

        Returns:
            str: return text from the film
        """
        with open(self.path) as file:
            return file.read()

    def export(self, frequency, compressedText):
        """Exports frequency and compressed text

        Args:
            frequency (dict): frequency of each characters in initial text
            compressedText (str): compressed text
        """
        dir = os.path.dirname(self.path)
        basename = os.path.splitext(os.path.basename(self.path))[0]

        with open(dir+"/"+basename+"_freq.txt", 'w') as file:
            file.write(str(len(frequency))+"\n")
            frequency = map(
                    lambda x: str(x[0])+" "+str(x[1])+'\n', frequency.items()
                )
            file.writelines(frequency)

        with open(dir+"/"+basename+"_comp.bin", 'wb') as file:
            file.write(compressedText)
