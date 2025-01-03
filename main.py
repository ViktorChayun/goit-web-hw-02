import sys

# мої модулі
from ErrorHandler import input_error
import Commands as C
from Serializer import PikleSerializer
from Serializer import DataStorage
from Interface import ConsoleView
################################


@input_error
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
################################


def main():
    view = ConsoleView()
    filename = ".\\addressbook.pkl"
    data_storage = DataStorage(filename, PikleSerializer())
    book = data_storage.load_data()
    # ініціація всіх команд
    invoker = C.Invoker()
    invoker.add_command(C.CommandEnum.ADD, C.CommandAdd(book))
    invoker.add_command(C.CommandEnum.EXIT, C.CommandExit(book))
    invoker.add_command(C.CommandEnum.CHANGE, C.CommandChange(book))
    invoker.add_command(C.CommandEnum.PHONE, C.CommandPhone(book))
    invoker.add_command(C.CommandEnum.ALL, C.CommandAll(book))
    invoker.add_command(C.CommandEnum.ADD_BIRTHDAY, C.CommandAddBirthday(book))
    invoker.add_command(C.CommandEnum.SHOW_BIRTHDAY, C.CommandShowBirthday(book))
    invoker.add_command(C.CommandEnum.BIRTHDAYS, C.CommandBirthdays(book))

    view.welcome()
    while True:
        user_input = view.get_input("Enter a command: ")
        command, *args = parse_input(user_input)

        command_execution_res = ""
        match command:
            case "help":
                view.show_help()
            case "close" | "exit":
                command_execution_res = invoker.run_command(C.CommandEnum.EXIT, [data_storage, *args])
                view.show_message(command_execution_res)
                sys.exit(0)
            case "hello":
                command_execution_res = "How can I help you?"
            case "all":
                command_execution_res = invoker.run_command(C.CommandEnum.ALL, args)
            # add [ім'я] [номер телефону]
            case "add":
                command_execution_res = invoker.run_command(C.CommandEnum.ADD, args)
            # change [ім'я] [old phone] [новий номер телефону]
            case "change":
                command_execution_res = invoker.run_command(C.CommandEnum.CHANGE, args)
            # phone [ім'я]
            case "phone":
                command_execution_res = invoker.run_command(C.CommandEnum.PHONE, args)
            case "add-birthday":
                command_execution_res = invoker.run_command(C.CommandEnum.ADD_BIRTHDAY, args)
            case "show-birthday":
                command_execution_res = invoker.run_command(C.CommandEnum.SHOW_BIRTHDAY, args)
            case "birthdays":
                command_execution_res = invoker.run_command(C.CommandEnum.BIRTHDAYS, args)
            case _:
                command_execution_res = "Invalid command."

        view.show_message(command_execution_res)
################################


if __name__ == "__main__":
    main()
