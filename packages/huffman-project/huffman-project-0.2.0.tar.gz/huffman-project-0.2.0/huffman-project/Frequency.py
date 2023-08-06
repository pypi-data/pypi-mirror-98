class Frequency():
    """Class to generate frequency of initial text
    """
    def __init__(self, text):
        self.text = text
        self.freq = {}

        for character in text:
            if character in self.freq:
                self.freq[character] += 1
            else:
                self.freq[character] = 1

        self.freq = dict(sorted(self.freq.items(), key=lambda x: x[1]))

    def get_text(self):
        """Get initial text

        Returns:
            str: initial text
        """
        return self.text

    def get_freq(self):
        """Get generate frequency

        Returns:
            dict: frequency of each characters in initial text
        """
        return self.freq
