from collections import UserDict
from datetime import datetime
from datetime import timedelta
from datetime import date
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError(f"Incorret phone value: '{value}'")
        super().__init__(value)

    def _is_valid(self, value) -> bool:
        pattern = r"^\d{10}$"
        return re.match(pattern, value) if value else False

    def __repr__(self):
        return f"{self.value}"


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") 
    
    @property
    def date(self) -> date:
        return datetime.strptime(self.value, "%d.%m.%Y").date() if self.value else None

 
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  # список з обєктами класу Phone
        self.birthday = None
        
    def add_phone(self, phone):
        p = Phone(phone)
        # перевірка чи такий номер вже існує, щоб не додавати дубль
        if not self.find_phone(phone):
            self.phones.append(p)
    
    def remove_phone(self, phone):
        value = self.find_phone(phone)
        if value:
            self.phones.remove(value)
    
    def edit_phone(self, old_phone: str, new_phone: str):
        # якщо номеру телефону який хочемо змінити не існує або новий номер некоректно заданий - викликаємо помилку
        if not self.find_phone(old_phone):
            raise ValueError(f"Can't edit. Old phone '{old_phone}' is not found.")        
        # якщо телефон дійсно змінився
        if old_phone != new_phone:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
    
    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
        
    def __str__(self):
        return f"Contact name: {self.name}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
  
            
class AddressBook(UserDict):
    def add_record(self, record: Record):
        # якщо такого запису по імені людини ще не існує, тоді додаємо
        if not self.find(record.name.value):
            self.data[record.name.value.lower()] = record
    
    def find(self, name) -> Record:
        return self.data.get(name.lower())

    def delete(self, name):
        if self.find(name):
            del self.data[name]
            
    def __str__(self):
        return "\n".join(str(rec) for rec in self.data.values())

    @staticmethod
    def _find_next_weekday(start_date, weekday: int):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
    
    @staticmethod
    def _adjust_for_weekend(date):
        if date.weekday() >= 5:
            return AddressBook._find_next_weekday(date, 0)
        return date

    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                dt = record.birthday.date  # атрибут класу Birthday, що повертає значення в datetime
                # дата народження в цьому році
                birthday_this_year = dt.replace(year=today.year)
                
                # ящо ДН вже відбувся вцьому році, дивомось коли буде в наступному році
                if birthday_this_year < today:
                    birthday_this_year = dt.replace(year=today.year+1)

                if 0 <= (birthday_this_year - today).days <= days:
                    birthday_this_year = AddressBook._adjust_for_weekend(birthday_this_year)
                    congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({"name": str(record.name), "birthday": congratulation_date_str})
        return upcoming_birthdays