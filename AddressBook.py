from collections import UserDict
import datetime
import re
import pickle

FILENAME = 'contacts.dat'


class AddressBook(UserDict):
    """Клас AddressBook - зберігає, додає записи та віддає записи книги контактів через ітератор"""

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, count: int):
        for key, value in self:
            i = 1
            container = {}
            while i <= count:
                container[key] = value
                i += 1
            yield container

    def __iter__(self):
        for key, value in self.data.items():
            yield key, value

    def search(self, value):
        ''' A method that searching a contact in adressbook and return list with coincidences'''
        record_result = []
        for record in self.data.values():
            if value in record.name.value:
                record_result.append(record)
                continue
            for phone in record.phones:
                if value in phone.value:
                    record_result.append(record)
        if not record_result:
            raise ValueError('Contact does not exist')
        return record_result

    def loader(self) -> None:
        """Функція завантажує дані з файлу, якщо він існує"""
        try:
            with open(FILENAME, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def saver(self) -> None:
        """Функція зберігає дані у файл"""
        with open(FILENAME, "wb") as file:
            pickle.dump(self.data, file)


class Field:
    """Батьківський клас для всіх записів у книзі контактів"""

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    """Обов'язкове поле з ім'ям в книзі контактів"""
    pass


class Phone(Field):
    """Необов'язкове поле з номером телефону(або кількома)"""

    @classmethod
    def check_phone(cls, phone):
        """Метод для валідації синтаксису номера телефона"""
        phone_format = r"\([0-9]{3}\)[0-9]{3}-[0-9]{2}-[0-9]{2}"
        if len(re.findall(phone_format, phone)) == 0:
            raise ValueError(
                'Incorrect phone format, should be (XXX)AAA-BB-CC')
        return phone

    @Field.value.setter
    def value(self, value):
        self._value = self.check_phone(value)


class Birthday(Field):
    """Необов'язкове поле з датою народження"""

    @classmethod
    def check_date(cls, birthday):
        """Метод для валідації синтаксису дати народження"""
        if birthday:
            try:
                return datetime.datetime.strptime(birthday, '%d-%m-%Y')
            except ValueError:
                print('Incorrect date format, should be DD-MM-YYYY')
        else:
            return None

    @Field.value.setter
    def value(self, value):
        self._value = self.check_date(value)


class Record:
    """Відповідає за логіку додавання/видалення/редагування полів.
    А також реалізує метод розрахунку днів до наступного дня народження(якщо параметр задано для поля)"""

    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []

        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for el in self.phones:
            if el.value == old_phone:
                el.value = new_phone

    def del_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)

    def days_to_birthday(self):
        today = datetime.date.today()
        birthday = self.birthday.value
        next_birthday = datetime.date(
            year=today.year, month=birthday.month, day=birthday.day)

        if next_birthday < today:
            next_birthday = datetime.date(
                year=today.year + 1, month=birthday.month, day=birthday.day)

        delta = next_birthday - today

        if delta.days == 0:
            return "birthday today!"
        else:
            return f'{delta.days} days to birthday'
