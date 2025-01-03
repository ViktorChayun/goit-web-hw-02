from enum import Enum
from abc import ABC, abstractmethod
# from functools import wraps

# мої модулі
from AddressBook import AddressBook
from AddressBook import Record
from ErrorHandler import input_error


# формуємо перелік всіх допустимих команд через Enum-довідник
class CommandEnum(Enum):
    ADD = "add"
    EXIT = "exit"
    HELLO = "hello"
    ALL = "all"
    CHANGE = "change"
    PHONE = "phone"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"


class Command(ABC):
    def __init__(self, book: AddressBook):
        self.book = book

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


# add [ім'я] [номер телефону]
class CommandAdd(Command):
    @input_error
    def execute(self, *args, **kwargs):
        name, phone, *_ = args
        record = self.book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."

        if phone:
            record.add_phone(phone)
        return message


class CommandExit(Command):
    @input_error
    def execute(self, *args, **kwargs):
        data_storage, *_ = args
        data_storage.save_data(self.book)  # Викликати перед виходом з програми
        return "Good bye!"


# change [ім'я] [старий телефон] [новий телефон]
class CommandChange(Command):
    @input_error
    def execute(self, *args, **kwargs) -> str:
        name, old_phone, new_phone, *_ = args
        record = self.book.find(name)
        if record is None:
            return f"Contact '{name}' is not found."
        record.edit_phone(old_phone, new_phone)
        return "Phone is changed."


# phone [ім'я]
class CommandPhone(Command):
    @input_error
    def execute(self, *args, **kwargs):
        name, *_ = args
        record = self.book.find(name)
        return record.phones


# all
class CommandAll(Command):
    @input_error
    def execute(self, *args, **kwargs):
        return str(self.book)


# add-birthday [ім'я] [дата народження]
class CommandAddBirthday(Command):
    @input_error
    def execute(self, *args, **kwargs):
        name, birthday, *_ = args
        record = self.book.find(name)
        record.add_birthday(birthday)
        return "Birthday is added"


# show-birthday [ім'я]
class CommandShowBirthday(Command):
    @input_error
    def execute(self, *args, **kwargs):
        name, *_ = args
        record = self.book.find(name)
        return str(record.birthday)


# birthdays
@input_error
class CommandBirthdays(Command):
    def execute(self, *args, **kwargs):
        # Показати дні народження на найближчі 7 днів з датами, коли їх треба привітати.
        return self.book.get_upcoming_birthdays()


# викликає  команди
class Invoker:
    commands = {}

    # додаємо команду у довідник команд
    def add_command(self, command_type: CommandEnum, command: Command):
        self.commands[command_type] = command

    def run_command(self, command_type: CommandEnum, args):
        if command_type not in self.commands.keys():
            return f"Error: Command {command_type} is not decalred."
        return self.commands[command_type].execute(*args)
