from collections import UserDict, UserList
import pickle


class Tags(UserList):
    pass


class Note:
    def __init__(self, content: str):
        self.title = content[:20]
        self.content = content


class NoteBook(UserDict):
    def add_note(self, note: Note):
        self.data[note.title] = note

    def save_before_close(self, fh='notebook.txt'):

        with open(fh, 'wb') as file:
            pickle.dump(self, file)

    def load_saved_notebook(self, fh='notebook.txt'):
        try:
            with open(fh, 'rb') as file:
                saved_book = pickle.load(file)
            return saved_book

        except FileNotFoundError:
            return self


NOTEBOOK = NoteBook()
NOTEBOOK = NOTEBOOK.load_saved_notebook()


def adding_note(text: str):
    note = Note(text)
    NOTEBOOK.add_note(note)
