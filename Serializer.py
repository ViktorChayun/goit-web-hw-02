from abc import ABC, abstractmethod
import pickle

from AddressBook import AddressBook


class Serializer(ABC):
    @abstractmethod
    def save_data(self, data, filename):
        pass

    @abstractmethod
    def load_data(self, filename):
        pass


class PikleSerializer(Serializer):
    def save_data(self, data, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def load_data(self, filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


class DataStorage:
    def __init__(self, filename: str, serializer: Serializer):
        self.serializer = serializer
        self.filename = filename

    def save_data(self, data):
        self.serializer.save_data(data, self.filename)

    def load_data(self):
        return self.serializer.load_data(self.filename)
