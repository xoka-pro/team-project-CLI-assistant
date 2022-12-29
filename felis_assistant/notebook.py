from datetime import datetime
from .mainbook import MainBook


class Note:
    """Notes class
    title (str) - short name
    content (str) - full note
    data (datetime) - creation date
    tags (str) - tags
    """

    def __init__(self, content: str, tags):

        self.content = content
        self.data = datetime.now()
        self.tags = tags
        if len(content) < 20:
            self.title = content
        self.title = content[:20]

    def __str__(self) -> str:
        """Modification note output"""
        format_data = self.data.strftime('%d-%m-%Y')
        tag_text = 'no tags' if not self.tags else ','.join(self.tags)
        return f'note: {self.title}\n{self.content}\ninsert: {format_data}\nTAGS: {tag_text}'

    def find_text(self, text: str):
        """Find text in note"""
        return -1 != self.content.find(text)


class NoteBook(MainBook):
    """Class for saving notes"""

    def add_note(self, note: Note):
        """Adding new note"""
        self.data[note.title] = note

    def edit_note(self, title, new_content: str):
        """Editing note found by title"""
        note = self.data[title]
        note.content = new_content
        self.data[title] = note

    def delete_note(self, title: str):
        """Deleting note by title"""
        del self.data[title]

    def find_text(self, text: str) -> list:
        """Notes search"""
        res_set = set()
        # search by title
        for key in self.data.keys():
            if text in key:
                res_set.add(self.data.get(key))

        # search by text
        for note_rec in self.data.values():
            if note_rec.find_text(text):
                res_set.add(note_rec)
        return list(res_set)

    def search_by_tags(self, tag: str) -> list:
        """Search by tags"""
        result = []
        for note in self.data.values():
            if note.tags:
                if tag in note.tags:
                    result.append(note)

        return result

    def sort_by_tags(self) -> list:
        """Sorting by tags"""
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
