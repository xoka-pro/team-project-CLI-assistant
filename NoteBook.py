from collections import UserDict
import pickle
from datetime import datetime


class Note:
    """Клас для нотатків
    title (str) - коротка назва
    content (str) - все тіло нотатки
    data (datetime) - дата створення
    tags (str) - теги
    """

    def __init__(self, content: str, tags):
        self.title = content[:20]
        self.content = content
        self.data = datetime.now()
        self.tags = tags

    def __str__(self) -> str:
        """Модифікація виводу нотатки"""
        return 'note: \n'+self.content+'\n insert '+self.data + '\n'

    def find_text(self, text: str):
        """Пошук тексту в нотатці"""
        if -1 != self.content.find(text):
            return True
        else:
            return False


class NoteBook(UserDict):
    """Клас для зберігання нотатків"""

    FILENAME = 'notebook.dat'

    def add_note(self, note: Note):
        """Внесення нової нотатки"""
        self.data[note.title] = note

    def edit_note(self, title: str, new_content: str):
        """Редагування нотатки знайденої за тайтлом"""
        try:
            note = self.data[title]
            note.content = new_content
        except KeyError:
            f'There is no note with title "{title}".'

    def del_note(self, title: str):
        """Видалення нотатки знайденої за тайтлом"""
        try:
            del self.data[title]

        except KeyError:
            f'There is no note with title "{title}".'

    def save_before_close(self, fh=FILENAME):
        """Збереження словника нотатків до файлу"""
        with open(fh, 'wb') as file:
            pickle.dump(self, file)

    def load_saved_notebook(self, fh=FILENAME):
        """Завантаження словника нотатків з файлу"""
        try:
            with open(fh, 'rb') as file:
                saved_book = pickle.load(file)
            return saved_book

        except FileNotFoundError:
            return self

    def find(self, text: str) -> set:
        """Пошук нотатків"""
        res_set = set()
        # пошук за тайтлом та чатиною його
        for key in self.data.keys:
            if text in key:
                res_set.add(self.data.get(key))

        # пошук за частиною з загального тексту
        for note_rec in self.data.values():
            if note_rec.find_text(text):
                res_set.add(note_rec)
        return res_set

    def search_by_tags(self, tag: str) -> list:
        """Пошук за тегами"""
        result = []
        for note in self.data.values():
            if note.tags:
                if tag in note.tags:
                    result.append(note.content)

        return result

    def sort_by_tags(self):
        """Сортування за тегами"""
        all_tags = []
        result = []
        for note in self.data.values():
            if note.tags:
                for tag in note.tags:
                    all_tags.append(tag)
        all_tags.sort()
        for rang_tag in all_tags:
            result.extend(self.search_by_tags(rang_tag))

        return result