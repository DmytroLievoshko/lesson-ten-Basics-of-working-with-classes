from typing import List
from collections import UserDict

import parse


def input_error(func):
    def iner(*args):
        try:
            return func(*args)
        except NoNameError:
            return "Enter user name"
        except NoKeyInformation:
            return f"no key information {args[1]}"
        except Exception as ex:
            return ex

    return iner


class NoNameError(Exception):
    pass


class NoKeyInformation(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        if value == "":
            raise NoNameError

        self.value = value


class Phone(Field):
    pass


class Email(Field):
    pass


class Record:
    def __init__(self, name: Name) -> None:
        self.name = name
        self.phones = []
        self.emails = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "phone add"

    def add_email(self, email):
        self.emails.append(Email(email))
        return "email add"

    def delete_phone(self, delete_phone):
        is_in_phones = False
        for phone in self.phones:
            if phone.value == delete_phone:
                self.phones.remove(phone)
                is_in_phones = True
                break

        if is_in_phones:
            return f"phone delete {delete_phone}"
        else:
            return f"{self.name.value} hes no phone {delete_phone}"

    def delete_email(self, delete_email):
        is_in_emails = False
        for email in self.emails:
            if email.value == delete_email:
                self.emails.remove(email)
                is_in_emails = True
                break

        if is_in_emails:
            return f"email delete {delete_email}"
        else:
            return f"{self.name.value} hes no phone {delete_email}"

    def show(self):
        result = self.name.value
        if self.phones:
            list_phones = []
            for phone in self.phones:
                list_phones.append(phone.value)
            result += ' ' + '; '.join(list_phones)
        if self.emails:
            list_emails = []
            for email in self.emails:
                list_emails.append(email.value)
            result += ' ' + '; '.join(list_emails)

        return result


class AddressBook(UserDict):
    @input_error
    def add_record(self, name, phone, email):
        field_name = Name(name)
        record = Record(field_name)
        if phone:
            record.add_phone(phone)
        if email:
            record.add_email(email)

        self.data[record.name.value] = record
        return "done"

    def show_all(self):
        result = "*" * 15 + "\n"
        for record in self.data.values():
            result += record.show() + "\n"

        result += "*" * 15
        return result

    @input_error
    def get_record(self, name):
        if name == "":
            raise NoNameError
        result = self.data.get(name)
        if not result:
            raise NoKeyInformation
        return result


def main():

    addressBook = AddressBook()

    while True:
        user_input = input(">>> ")

        command, args = parse.parse_user_input(user_input)
        phone = parse.get_phone_from_args(args)
        email = parse.get_email_from_args(args)
        name = args.replace(phone, "").replace(email, "").strip()

        if command == "hello":
            print("How can I help you?")
        elif command == "exit":
            print("Good bye!")
            break
        elif command == "add":
            print(addressBook.add_record(name, phone, email))
        elif command == "change":
            record = addressBook.get_record(name)
            if isinstance(record, Record):
                if phone:
                    print(record.add_phone(phone))
                if email:
                    print(record.add_email(email))
            else:
                print(record)
        elif command == "phone":
            record = addressBook.get_record(name)
            if isinstance(record, Record):
                print(record.show())
            else:
                print(record)
        elif command == "show_all":
            print(addressBook.show_all())
        elif command == "delete":
            record = addressBook.get_record(name)
            if isinstance(record, Record):
                if phone:
                    print(record.delete_phone(phone))
                if email:
                    print(record.delete_email(email))
            else:
                print(record)
        else:
            print(f"I don't know what means '{user_input}'")


if __name__ == "__main__":
    main()
