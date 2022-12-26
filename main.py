from AddressBook import AddressBook, Record
from NoteBook import NoteBook, Note
from sorter import sorter
import difflib

CONTACTS = AddressBook()
NOTES = NoteBook()


def input_error(func):
    """ Errors handler """

    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as error:
            return f'No name in contacts. Error: {error}'
        except IndexError as error:
            return f'Sorry, not enough params for command. Error: {error}'
        except ValueError as error:
            return f'Value error: {error}'
        except TypeError as error:
            return f'Not enough arguments. Error: {error}'

    return wrapper


def hello() -> str:
    """Функція для вітання користувача"""
    CONTACTS.loader()
    NOTES.loader()
    return (f'How can I help you?\n'
            f'Type "h" or "help" to show help')


def goodbye():
    """Функція завершення програми"""
    print(f'Good bye!')
    quit()


@input_error
def add(name, number, birthday=None, email=None) -> str:
    """Функція для додавання нового запису або додавання нового телефону контакту"""

    if name not in CONTACTS:
        new_number = Record(name, number, birthday, email)
        CONTACTS.add_record(new_number)
        CONTACTS.saver()
        return f'Contact add successfully'
    else:
        CONTACTS[name].add_phone(number)
        CONTACTS.saver()
        return f'New number added to {name}'


def adding_note() -> str:
    text = input('Input text for the note: ')
    tags = input('Input tags for the note: ')
    tags = tags.split(" ")
    note = Note(text, tags)
    NOTES.add_note(note)
    NOTES.saver()
    if note.tags:
        return f'New note with tags added'
    return f'New note added'


@input_error
def change(*args) -> str:
    """Функція для заміни номеру телефона контакту"""

    name, old_number, new_number, *_ = args
    if name in CONTACTS:
        CONTACTS[name].change_phone(old_number, new_number)
        CONTACTS.saver()
    else:
        return f'No contact "{name}"'
    return f'Contact change successfully'


@input_error
def del_phone(name, phone) -> str:
    """Функція видалення номера телефона у контакту"""

    if name in CONTACTS:
        CONTACTS[name].del_phone(phone)
        CONTACTS.saver()
    else:
        return f'No contact "{name}"'
    return f'Phone number deleted successfully'


def delete_note() -> str:
    title = input("Input at least 20 first chars of the note for editing: ")
    title = title[:20]
    if NOTES.data.get(title):
        NOTES.delete_note(title)
        NOTES.saver()
        return f'Note deleted successfully'
    return f'I can not delete the note. There is no note with title "{title}".'


@input_error
def delete_user(name):
    CONTACTS.remove_record(name)
    return f"User with name {name} was deleted"


def editing_note() -> str:
    title = input("Input at least 20 first chars of the note for editing: ")
    title = title[:20]
    if NOTES.data.get(title):
        new_text = input("Input the new text of note: ")
        NOTES.edit_note(title, new_text)
        NOTES.saver()
        return f'Note changed successfully'
    return f'I can not change the note. There is no note with title "{title}".'


@input_error
def phone_func(*args) -> str:
    """Повертає номер телефону для зазначеного контакту"""

    find_phone = args[0]
    result = []
    for el in CONTACTS.iterator(5):
        for name, data in el.items():
            if name == find_phone:
                result.append(
                    f'Name: {name} | Numbers: {", ".join(phone.value for phone in data.phones)}')

    if len(result) < 1:
        return f'No contact {find_phone}'
    return '\n'.join(result)


def searching_by_tag(word: str) -> str:
    res = NOTES.search_by_tags(word)
    res = "\n".join(res)
    return res


def sorting_by_tags(word: str) -> str:
    res = "\n".join(NOTES.sort_by_tags(word))
    return res


@input_error
def show_all() -> str:
    """Повертає всю книгу контактів"""

    result = []
    for el in CONTACTS.iterator(5):
        for name, data in el.items():
            numbers = ", ".join(phone.value for phone in data.phones)
            if hasattr(data, 'birthday'):
                bday = data.birthday.value.date().strftime('%d-%m-%Y')
                to_birthday = CONTACTS[name].days_to_birthday()
                result.append(
                    f'Name: {name} | Numbers: {numbers} | Birthday: {bday} - {to_birthday}')
            else:
                result.append(f'Name: {name} | Numbers: {numbers}')
    if len(result) < 1:
        return f'Contact list is empty'
    return '\n'.join(result)


@input_error
def search(*args) -> str:
    """Функія реалізовує пошук даних у книзі контактів"""
    result = []
    search_text = str(args[0]).lower()
    for el in CONTACTS.iterator(5):
        for name, data in el.items():
            numbers = ", ".join(phone.value for phone in data.phones)
            if str(name).lower().find(search_text) >= 0 or \
                    numbers.find(search_text) >= 0:
                if hasattr(data, 'birthday'):
                    bday = data.birthday.value.date().strftime('%d-%m-%Y')
                    to_birthday = CONTACTS[name].days_to_birthday()
                    result.append(
                        f'Name: {name} | Numbers: {numbers} | Birthday: {bday} - {to_birthday}')
                else:
                    result.append(f'Name: {name} | Numbers: {numbers}')
    if len(result) < 1:
        return f'No results'
    return '\n'.join(result)


@input_error
def list_record_to_x_day_bd(*args) -> str:
    """Функія формує текст зі списку днів народження в вказані дні"""
    result = []
    day = int(args[0])
    for el in CONTACTS.list_record_to_x_day_bd(day):
        numbers = ", ".join(phone.value for phone in el.phones)
        bday = el.birthday.value.date().strftime('%d-%m-%Y')
        result.append(
            f'Name: {el.name.value} | Numbers: {numbers} | Birthday: {bday}')
    if len(result) < 1:
        return f'No results'
    return '\n'.join(result)


def hlp(*args) -> str:
    """Повертає коротку допомогу по командах"""
    return (f'Known commands:\n'
            f'hello, help -- this help\n'
            f'add -- add new contact or new number for contact\n'
            f'change -- change specified number for contact\n'
            f'phone --  show phone numbers for specified contact\n'
            f'show all -- show all contacts\n'
            f'search -- search contacts by letters in name or digits in number\n'
            f'delete -- delete specified number from contact\n'
            f'good bye, close, exit -- shutdown application\n'
            f'note_add -- add new note to the notebook\n'
            'note_delete -- delete the note to the notebook\n'
            'note_edite -- edite the note to the notebook\n'
            'tag_search -- search all notes with the tag\n'
            'tag_sort -- sort all notes by tags\n'
            )


def parser(msg: str):
    """ Parser and handler AIO """
    command = None
    params = []

    for key in operations:
        if msg.lower().startswith(key):
            command = operations[key]
            msg = msg.lstrip(key)
            for item in filter(lambda x: x != '', msg.split(' ')):
                params.append(item)
            return command, params
    return command, params


def incorrect_input(msg):
    guess = difflib.get_close_matches(msg, operations.keys())
    if guess:
        return f'Sorry, unknown command. Maybe you mean: {" ,".join(guess)}'
    else:
        return f'Sorry, unknown command, try again. Type "h" for help.'


operations = {
    'hello': hello,
    'h': hlp,
    'help': hlp,
    'add': add,
    'change': change,
    'phone': phone_func,
    'show all': show_all,
    'good bye': goodbye,
    'close': goodbye,
    'exit': goodbye,
    'del phone': del_phone,
    'delete': delete_user,
    'del': delete_user,
    'search': search,
    'sort': sorter,
    'note_add': adding_note,
    'note_delete': delete_note,
    'note_edite': editing_note,
    'tag_search': searching_by_tag,
    'tag_sort': sorting_by_tags,
    'birthday': list_record_to_x_day_bd,
}


def main():
    """ Main function - all interaction with user """
    print(hello())
    while True:
        msg = input("Input command: ")
        command, params = parser(msg)
        if command:
            print(command(*params))
        else:
            print(incorrect_input(msg))


if __name__ == '__main__':
    main()
