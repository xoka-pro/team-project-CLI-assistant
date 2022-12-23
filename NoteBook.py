from collections import UserDict
import pickle
from datetime import datetime



class Note:
    def __init__(self, content: str):
        self.title = content[:20]
        self.content = content
        self.data = datetime.now()


class NoteBook(UserDict):

    FILENAME = 'notebook.dat'

    def add_note(self, note: Note):
        self.data[note.title] = note

    def edit_note(self, title: str, new_content: str):
        try:
            note = self.data[title]
            note.content = new_content
        except KeyError:
            f'There is no note with title "{title}".'

    def del_note(self, title: str):

        try:
            del self.data[title]

        except KeyError:
            f'There is no note with title "{title}".'

    def save_before_close(self, fh=FILENAME):

        with open(fh, 'wb') as file:
            pickle.dump(self, file)

    def load_saved_notebook(self, fh=FILENAME):

        try:
            with open(fh, 'rb') as file:
                saved_book = pickle.load(file)
            return saved_book

        except FileNotFoundError:
            return self



