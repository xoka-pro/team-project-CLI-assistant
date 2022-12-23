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


def editing_note(title: str, new_text: str):
    if len(title) < 20:
        print("Input min the first 20 chars of the note, please")

    title = title[:20]

    NOTEBOOK.edit_note(title, new_text)


def delete_note(title: str):
    if len(title) < 20:
        print("Input min the first 20 chars of the note, please")

    title = title[:20]

    NOTEBOOK.del_note(title)
