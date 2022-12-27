from datetime import datetime
from mainbook import MainBook


class Note:
    """Клас для нотатків
    title (str) - коротка назва
    content (str) - все тіло нотатки
    data (datetime) - дата створення
    tags (str) - теги
    """

    def __init__(self, content: str, tags):

        self.content = content
        self.data = datetime.now()
        self.tags = tags
        if len(content) < 20:
            self.title = content
        self.title = content[:20]

    def __str__(self) -> str:
        """Модифікація виводу нотатки"""
        return 'note: \n' + self.content + '\n insert ' + self.data + '\n' + 'no tags' if not self.tags else self.tags + '\n'

    def find_text(self, text: str):
        """Пошук тексту в нотатці"""
        if -1 != self.content.find(text):
            return True
        else:
            return False


class NoteBook(MainBook):
    """Клас для зберігання нотатків"""

    def add_note(self, note: Note):
        """Внесення нової нотатки"""
        self.data[note.title] = note

    def edit_note(self, title, new_content: str):
        """Редагування нотатки знайденої за тайтлом"""
        note = self.data[title]
        note.content = new_content
        self.data[title] = note

    def delete_note(self, title: str):
        """Видалення нотатки знайденої за тайтлом"""
        del self.data[title].content

    def find_text(self, text: str) -> list:
        """Пошук нотатків"""
        res_set = set()
        # пошук за тайтлом та чатиною його
        for key in self.data.keys():
            if text in key:
                res_set.add(self.data.get(key))

        # пошук за частиною з загального тексту
        for note_rec in self.data.values():
            if note_rec.find_text(text):
                res_set.add(note_rec)
        return list(res_set)

    def search_by_tags(self, tag: str) -> list:
        """Пошук за тегами"""
        result = []
        for note in self.data.values():
            if note.tags:
                if tag in note.tags:
                    result.append(note.content)

        return result

    def sort_by_tags(self, tag: str) -> list:
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
