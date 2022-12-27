import pickle
from collections import UserDict


class MainBook(UserDict):

    def saver(self, fh):
        """Збереження словника книги до файлу"""
        with open(fh, 'wb') as file:
            pickle.dump(self.data, file)

    def loader(self, fh):
        """Завантаження словника книги з файлу"""
        try:
            with open(fh, 'rb') as file:
                self.data = pickle.load(file)

        except FileNotFoundError:
            pass

