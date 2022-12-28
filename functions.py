from addressbook import AddressBook, Record
from notebook import NoteBook, Note
from sorter import sorter
import difflib
from tabulate import tabulate
import holidays
from datetime import date
from weather_func import get_weather

from constants import FILENAME_CONTACTS
from constants import FILENAME_NOTES

CONTACTS = AddressBook()
NOTES = NoteBook()


def input_error(func):
    """ Errors handler """

    def wrapper(*args):
        try:
            return func(*args)
        except KeyError as error:
            return f'Not found. Error: {error}'
        except IndexError as error:
            return f'Sorry, not enough params for command. Error: {error}'
        except ValueError as error:
            return f'Value error: {error}'
        except TypeError as error:
            return f'Not enough arguments. Error: {error}'

    return wrapper


def hello() -> str:
    """Function to greeting user"""
    return (f'Meow! How can I help you?\n'
            f'Type "help" to show help')


def goodbye():
    """Function to end program"""
    print(f'Good bye!')
    quit()


@input_error
def add(name=None, number=None, birthday=None, email=None, address=None) -> str:
    """Function to add new record or add new contact phone number"""
    name = input('Input contact name: ')
    if name not in CONTACTS:
        print('Adding new contact')
        number = input('Input phone number: ')
        birthday = input('Input birthday(DD-MM-YYY): ')
        email = input('Input email: ')
        address = input('Input address: ')
        new_number = Record(name, number, birthday, email, address)
        CONTACTS.add_record(new_number)
        CONTACTS.saver(FILENAME_CONTACTS)
        return f'Contact add successfully'
    else:
        print(f'Contact {name} already exist. Adding new number')
        number = input('Input new phone number: ')
        CONTACTS[name].add_phone(number)
        CONTACTS.saver(FILENAME_CONTACTS)
        return f'New number added to {name}'


@input_error
def adding_note() -> str:
    """Function to add new note and tags"""
    text = input('Input text for the note: ')
    tags = input('Input tags for the note: ')
    tags = tags.split(" ")
    note = Note(text, tags)
    NOTES.add_note(note)
    NOTES.saver(FILENAME_NOTES)
    if note.tags:
        return f'New note with tags added'
    return f'New note added'


@input_error
def change_address(*args) -> str:
    """Function to change address in contact"""

    name, old_value, new_value, *_ = args
    if name in CONTACTS:
        CONTACTS[name].change_field('address', old_value, new_value)
        CONTACTS.saver(FILENAME_CONTACTS)
    else:
        return f'No contact "{name}"'
    return f'Contact address change successfully'


@input_error
def change_birthday(*args) -> str:
    """Function to change birthday in contact"""

    name, old_value, new_value, *_ = args
    if name in CONTACTS:
        CONTACTS[name].change_field('birthday', old_value, new_value)
        CONTACTS.saver(FILENAME_CONTACTS)
    else:
        return f'No contact "{name}"'
    return f'Contact birthday change successfully'


@input_error
def change_email(*args) -> str:
    """Function to change email in contact"""

    name, old_value, new_value, *_ = args
    if name in CONTACTS:
        CONTACTS[name].change_field('email', old_value, new_value)
        CONTACTS.saver(FILENAME_CONTACTS)
    else:
        return f'No contact "{name}"'
    return f'Contact email change successfully'


@input_error
def change(*args) -> str:
    """Function to change phone number in contact"""

    name, old_number, new_number, *_ = args
    if name in CONTACTS:
        CONTACTS[name].change_phone(old_number, new_number)
        CONTACTS.saver(FILENAME_CONTACTS)
    else:
        return f'No contact "{name}"'
    return f'Contact change successfully'


@input_error
def del_phone(name, phone) -> str:
    """Function to delete number phone in contact"""

    if name in CONTACTS:
        CONTACTS[name].del_phone(phone)
        CONTACTS.saver(FILENAME_CONTACTS)
    else:
        return f'No contact "{name}"'
    return f'Phone number deleted successfully'


@input_error
def delete_user(name):
    """Function to delete contact"""
    CONTACTS.remove_record(name)
    return f"User with name {name} was deleted"


@input_error
def delete_note() -> str:
    """Function to delete note"""
    title = input("Input at least 20 first chars of the note for editing: ")
    title = title[:20]
    if NOTES.data.get(title):
        NOTES.delete_note(title)
        NOTES.saver(FILENAME_NOTES)
        return f'Note deleted successfully'
    return f'I can not delete the note. There is no note with title "{title}".'


@input_error
def editing_note() -> str:
    """Function to edit note"""
    title = input("Input at least 20 first chars of the note for editing: ")
    title = title[:20]
    if title in NOTES.data.keys():
        new_text = input("Input the new text of note: ")
        NOTES.edit_note(title, new_text)
        NOTES.saver(FILENAME_NOTES)
        return f'Note changed successfully'
    return f'I can not change the note. There is no note with title "{title}".'


@input_error
def phone_func(*args) -> str:
    """Returns the phone number for specified contact"""

    find_phone = args[0]
    result = []
    for name, data in CONTACTS.data.items():
        if name == find_phone:
            numbers = ", ".join(phone.value for phone in data.phones)
            result.append((name, numbers))
    if len(result) < 1:
        return f'No contact {find_phone}'
    columns = ['Name', 'Phones']
    return tabulate(result, headers=columns, tablefmt='psql')


@input_error
def searching_by_word(word: str) -> str:
    res = NOTES.find_text(word)
    result = ""
    if not len(res):
        return 'Nothing find'
    else:
        for cur_note in res:
            result += str(cur_note)
        return result


def searching_by_tag(word: str) -> str:
    """Function to search by tag"""
    notes_list = list(map(str,NOTES.search_by_tags(word)))
    res = "\n" + "\n\n".join(notes_list) + "\n"
    return res


def sorting_by_tags() -> str:
    """Function to sort by tags"""
    notes_list = list(map(str, NOTES.sort_by_tags()))
    res = "\n" + "\n\n".join(notes_list) + "\n"
    return res


@input_error
def show_all() -> str:
    """Return all contact book"""

    result = []
    for name, data in CONTACTS.data.items():
        numbers = ", ".join(phone.value for phone in data.phones)
        bday = data.birthday.value.date().strftime('%d-%m-%Y') if data.birthday else None
        email = data.email.value if data.email else None
        address = data.address.value if data.address else None
        result.append([name, numbers, bday, email, address])
    if len(result) < 1:
        return f'Contact list is empty'
    columns = ['Name', 'Phones', 'Birthday', 'E-mail', 'Address']
    return tabulate(result, headers=columns, tablefmt='psql')


def show_all_note() -> str:
    """Return all notes"""
    all_notes = list(map(str, NOTES.values()))

    res = "\n" + "\n\n".join(all_notes) + "\n"
    return res


@input_error
def search(*args) -> str:
    """Function implements data search in contact book"""
    result = []
    search_text = str(args[0]).lower()
    for name, data in CONTACTS.data.items():
        numbers = ", ".join(phone.value for phone in data.phones)
        if str(name).lower().find(search_text) >= 0 or \
                numbers.find(search_text) >= 0:
            if data.birthday.value:
                bday = data.birthday.value.date().strftime('%d-%m-%Y')
            else:
                bday = None
            result.append(
                [name, numbers, bday, data.email.value, data.address.value])
    if len(result) < 1:
        return f'No results'
    columns = ['Name', 'Phones', 'Birthday', 'E-mail', 'Address']
    return tabulate(result, headers=columns, tablefmt='psql')


@input_error
def list_record_to_x_day_bd(*args) -> str:
    """Function generates text from list of birthdays on specified days"""
    result = []
    day = int(args[0])
    for user in CONTACTS.list_record_to_x_day_bd(day):
        bday = user.birthday.value.date().strftime('%d-%m-%Y')
        result.append((user.name.value, bday))
    if len(result) < 1:
        return f'No results'
    columns = ['Name', 'Birthday']
    return tabulate(result, headers=columns, tablefmt='psql')


def today_holiday(*args):
    if len(args):
        day = int(args[0])
    else:
        day = 0
    ua_holidays = holidays.country_holidays('UA')
    if day:
        result = []
        d_start = date.today().toordinal()
        for el in range(d_start, d_start+day):
            res = ua_holidays.get(date.fromordinal(el))
            if res:
                result.append((date.fromordinal(el).strftime('%d-%m-%Y'), res))
        if len(result):
            columns = ['Date', 'Name']
            return tabulate(result, headers=columns, tablefmt='psql')
        else:
            return 'No holiday in period'
    else:
        res = ua_holidays.get(date.today())
    if res is None:
        return 'No holiday today'
    return res


def hlp(*args) -> str:
    """Returns brief command help"""

    res = [("help", "this help"),
           ("add_contact", "add new contact or new number for contact"),
           ("change_phone", "change specified number for contact"),
           ("change_address", "change specified address for contact"),
           ("change_birthday", "change specified birthday for contact"),
           ("change_email", "change specified email for contact"),
           ("phone", "show phone numbers for specified contact"),
           ("show_all", "show all contacts"),
           ("search", "search contacts by letters in name or digits in number"),
           ("phone_delete", "delete specified number from contact"),
           ("contact_delete", "delete specified contact"),
           ("exit", "shutdown application"),
           ("note_add", "add new note to the notebook"),
           ("note_delete", "delete the note to the notebook"),
           ("note_edit", "edite the note to the notebook"),
           ("note_show_all", "show all notes"),
           ("tag_search", "search all notes with the tag"),
           ("tag_sort", "sort all notes by tags"),
           ("word_search", "search all notes with the word"),
           ("birthday X", "list of contact with birthday in X days"),
           ("holiday X", "list of holidays in Ukraine today or X days"),
           ("weather X", "show weather in city X"),
           ]
    columns = ['Known commands', 'Description']
    return tabulate(res, headers=columns, tablefmt='psql')


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
    """Function to check correctness"""
    guess = difflib.get_close_matches(msg, operations.keys())
    if guess:
        return f'Do you have paws too? Maybe you mean: {", ".join(guess)}'
    else:
        return f"Sorry, I don't know this command. Type for help for help."


operations = {
    'hello': hello,
    'help': hlp,
    'add_contact': add,
    'change_phone': change,
    'change_address': change_address,
    'change_birthday': change_birthday,
    'change_email': change_email,
    'phone': phone_func,
    'show_all': show_all,
    'exit': goodbye,
    'phone_delete': del_phone,
    'contact_delete': delete_user,
    'search': search,
    'sort': sorter,
    'note_add': adding_note,
    'note_delete': delete_note,
    'note_edit': editing_note,
    'note_show_all': show_all_note,
    'tag_search': searching_by_tag,
    'tag_sort': sorting_by_tags,
    'birthday': list_record_to_x_day_bd,
    'word_search': searching_by_word,
    'holiday': today_holiday,
    'weather': get_weather,
}


def startup_loader():
    CONTACTS.loader(FILENAME_CONTACTS)
    NOTES.loader(FILENAME_NOTES)
