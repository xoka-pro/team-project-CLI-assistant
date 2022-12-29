import pickle
from collections import UserDict


class MainBook(UserDict):
    """Parent class for notebook and contact book"""

    def saver(self, fh):
        """Saving data to file"""
        with open(fh, 'wb') as file:
            pickle.dump(self.data, file)

    def loader(self, fh):
        """Load data from file"""
        try:
            with open(fh, 'rb') as file:
                self.data = pickle.load(file)

        except FileNotFoundError:
            pass

