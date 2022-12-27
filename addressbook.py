from datetime import datetime, date
import re
from mainbook import MainBook


class AddressBook(MainBook):
    """Клас AddressBook - зберігає, додає записи та віддає записи книги контактів через ітератор"""

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name: str):
        self.data.pop(name)

    def iterator(self, count: int):
        for key, value in self.data.items():
            i = 1
            container = {}
            while i <= count:
                container[key] = value
                i += 1
            yield container

    def __iter__(self):
        return self

    def list_record_to_x_day_bd(self, day_to_birthday=0) -> list:
        list_of_record = []
        today = date.today()
        for record in self.data.values():
            # перевірка на наявність дати
            if not record.birthday.value:
                continue
            birthday = record.birthday.value

            shift = (datetime(today.year, birthday.month,
                     birthday.day).date() - today).days
            if shift < 0:
                shift = (datetime(today.year+1, birthday.month,
                         birthday.day).date() - today).days

            if shift <= day_to_birthday:
                list_of_record.append(record)
        return list_of_record

    def search(self, value):
        """A method that searching a contact in adressbook and return list with coincidences"""
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


class Address(Field):
    """For address of contact"""
    pass


class Email(Field):
    """Необов'язкове поле з емайлом"""

    @classmethod
    def check_email(cls, email):
        """validation email
        if first haven't !#$%^&*() and one @
        domains from 1-63 len and 1st domen name just letter 1-6 len
        """
        parse = re.search(
            r"^(([A-Za-z0-9]+_+)|([A-Za-z0-9]+\-+)|([A-Za-z0-9]+\.+)|([A-Za-z0-9]+\++))*[A-Za-z0-9]+@((\w+\-+)|(\w+\.))*\w{1,63}\.[a-zA-Z]{2,6}$",
            email)
        if not parse:
            raise ValueError(
                'Incorrect email format')
        return email

    @Field.value.setter
    def value(self, value):
        self._value = self.check_email(value)


class Phone(Field):
    """Необов'язкове поле з номером телефону(або кількома)"""

    @classmethod
    def check_phone(cls, phone):
        """Validation phone number for match some mask:
        +380991112233 or 099-111-22-33 or 099-111-2233 or 0991112233
        or (099)1112233 or (099)111-22-33 or (099)111-2233"""

        parse = re.search(
            r"\d{3}\-\d{3}\-\d{2}\-\d{2}|\d{3}\-\d{3}\-\d{4}|\(\d{3}\)\d{3}\-\d{2}\-\d{2}|\(\d{3}\)\d{3}\-\d{4}|\(\d{3}\)\d{7}|\d{10}|\+\d{12}$",
            phone)
        if not parse:
            raise ValueError(
                'Incorrect phone format, should be: \n + 380991112233 or 099-111-22-33 or 099-111-2233 or 0991112233 \n or (099)1112233 or (099)111-22-33 or (099)111-2233')
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
                return datetime.strptime(birthday, '%d-%m-%Y')
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

    def __init__(self, name, phone=None, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday)
        self.email = Email(email)
        self.address = Address(address)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_field(self, field_name, old_value, new_value):
        if field_name == 'phones':
            for phone in self.phones:
                if phone.value == old_value:
                    phone.value = new_value
        elif field_name == 'birthday':
            self.birthday = Birthday(new_value)
        elif field_name == 'email':
            self.email = Email(new_value)
        elif field_name == 'address':
            self.address = Address(new_value)

    def change_phone(self, old_phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == old_phone:
                phone_number.value = new_phone

    def del_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                self.phones.remove(phone_number)

    def days_to_birthday(self):
        today = date.today()
        birthday = self.birthday.value
        next_birthday = date(
            year=today.year, month=birthday.month, day=birthday.day)

        if next_birthday < today:
            next_birthday = date(
                year=today.year + 1, month=birthday.month, day=birthday.day)

        delta = next_birthday - today

        if delta.days == 0:
            return "birthday today!"

        return f'{delta.days} days to birthday'
