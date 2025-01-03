from abc import ABC, abstractmethod

# Абстрактний базовий клас для представлень
class View(ABC):
    # метод зчитування даних від юзера
    @abstractmethod
    def get_input(self, message):
        pass

    # метод відображення даних
    @abstractmethod
    def show_message(self, message):
        pass

    # довідка по командам
    @abstractmethod
    def show_help(self):
        pass
    
    # стартове вікно юзера
    @abstractmethod
    def welcome(self):
        pass

# Конкретна реалізація UI представлення для консолі
class ConsoleView(View):
    def get_input(self, message):
        return input(message)
    
    def show_message(self, message):
        print(message)

    def welcome(self):
        print("Welcome to the assistant bot!")
    
    def show_help(self):
        print("Available commands:")
        print(" - help")
        print(" - hello")
        print(" - add [name] [phone]")
        print(" - change [name] [old_phone] [new_phone]")
        print(" - phone [name]")
        print(" - all")
        print(" - add-birthday [name] [birthday]")
        print(" - show-birthday [name]")
        print(" - birthdays")
        print(" - close | exit")