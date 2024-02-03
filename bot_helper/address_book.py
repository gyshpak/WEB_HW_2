from collections import UserDict
from datetime import date
from re import match
import pickle
# import json


class WrongBirthday(Exception):
    pass
class ExistsPhone(Exception):
    pass
class WrongMemo(Exception):
    pass
class ExistsMemo(Exception):
    pass
class ExistsAddress(Exception):
    pass
class WrongAddress(Exception):
    pass
class WrongEmail(Exception):
    pass
class ExistsEmail(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __repr__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        self.__value = ""
        self.value = value

    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, new_value):
        if new_value == "":
            self.__value = None
        elif self.is_valid_phone(new_value):
            norm_phone = self.normalis_phone(new_value)
            self.__value =  norm_phone
        else:
            raise ValueError
 
    def is_valid_phone(self, value):
        if  value!= "":
            # if match(r"^[\+]?3?8?[\s]?\(?0\d{2}?\)?[\s]?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}$", value) != None:
            if match(r"^[\+]?3?8?\(?\d{3}?\)?\d{3}[\-]?\d{2}[\-]?\d{2}$", value) != None:
                return True
            else:
                return False

    def normalis_phone(self, value):
        norm_mob = value.replace("+","")\
                        .replace(" ","")\
                        .replace("(","")\
                        .replace(")","")\
                        .replace("-","")
        if len(norm_mob) == 10:
            return "+38" + norm_mob
        if len(norm_mob) == 11:
            return "+3" + norm_mob
        if len(norm_mob) == 12:
            return "+" + norm_mob
        return ""

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return NotImplemented
    
    def __repr__(self):
        return self.__value


class Email(Field):
    def __init__(self, value):
        self.__value = ""
        self.value = value

    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, new_value):
        if new_value == "":
            self.__value = None
        elif self.is_valid_email(new_value):
            self.__value = new_value
        else:
            raise WrongEmail
 
    def is_valid_email(self, value):
        # if value == "":
        #     pass
        # else:
        # if  value!= "":
        if match(r"[a-zA-Z0-9]+[\w\-]+[\.]?[a-zA-Z\w\-]+[@]{1}[a-z]+[\.]{1}[a-z]{2,}", value) != None:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.value == other.value
        return NotImplemented   
    
    def __str__(self):
        return str(self.__value)
    
    def __repr__(self):
        return self.__value


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if new_value == "":
            self.__value = None
        elif self.is_valid_birthday(new_value):
            norm_birthday = self.normalis_birthday(new_value)
            if norm_birthday != "":
                self.__value = norm_birthday
            else:
                raise WrongBirthday
        else:
            # self.__value = None
            raise WrongBirthday

    def is_valid_birthday(self, value):
        if value != "":
            if match(r"^\d{2}['\s'|\-|'.'|:]{1}\d{2}[\s|\-|'.'|:]{1}\d{4}$|^\d{4}['\s'|\-|'.'|:]{1}\d{2}[\s|\-|'.'|:]{1}\d{2}$", value) != None:
                return True
            else:
                return False
            
    def normalis_birthday(self, new_value):
        norm_birthday = new_value.replace(".",",")\
                    .replace(" ",",")\
                    .replace("-",",")\
                    .replace(":",",")
        date_birthday = norm_birthday.split(",")
        if len(date_birthday[0]) == 4:
            # try:
            return date(int(date_birthday[0]), int(date_birthday[1]), int(date_birthday[2]))
            # except:
                # raise WrongBirthday
        else:
            # try:
            return date(int(date_birthday[2]), int(date_birthday[1]), int(date_birthday[0]))
            # except:
                # raise WrongBirthday
        
    def __sub__(self, other):
        birthday_month = self.value.month
        birthday_day = self.value.day
        my_birthday = date(other.value.year, birthday_month, birthday_day)
        date_today = other.value
        if my_birthday < date_today:
            my_birthday = my_birthday.replace(year=date_today.year + 1)
        day_to_birthday = my_birthday - date_today
        return day_to_birthday.days
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def __repr__(self):
        return self.value.strftime("%d.%m.%Y")


class Memo(Field):
    def __init__(self, memo_text: str):
        self.__value = ''
        self.value = memo_text

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, memo_text: str):
        if memo_text.isprintable() and len(memo_text)<=240:
            self.__value = memo_text
        else:
            raise WrongMemo

    def __str__(self):
        return str(self.__value)
    
    def __repr__(self):
        return str(self.__value)


class Address(Field):
    def __init__(self, adr_text: str):
        self.__value = None
        self.value = adr_text

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, adr_text):
        if adr_text.isprintable() and len(adr_text) <= 100:
            self.__value = adr_text
        else:
            raise WrongAddress

    def __str__(self):
        return self.__value

    def __repr__(self):
        return self.__value

class Record:
    # def __init__(self, name, birthday = None):
    def __init__(self, name):
        # if birthday is not None:
            # self.birthday = Birthday(birthday)
        self.name = Name(name)
        self.birthday = None
        self.phones = []
        self.emails = None
        self.memos = None
        self.address = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj not in self.phones:
            self.phones.append(phone_obj)

    def remove_phone(self, phone):
        search_phone = Phone(phone)
        self.phones.remove(search_phone)

    def edit_phone(self, phone, new_phone):
        search_phone = Phone(phone)
        chandge_phone = Phone(new_phone)
        index = self.phones.index(search_phone)
        self.phones[index] = chandge_phone
    
    def find_phone(self, phone):
        search_phone = Phone(phone)
        for item in self.phones:
            if item == search_phone:
                return item
            
    def add_email(self, email):
        # if self.emails:
        #     raise ExistsEmail
        email_obj = Email(email)
        self.emails = email_obj
    
    def add_birthday(self, birthday):
        # if self.emails:
        #     raise ExistsEmail
        birthday_obj = Birthday(birthday)
        self.birthday = birthday_obj

    def delete_email(self):
        self.emails = None
                    
    def days_to_birthday(self):
        if hasattr(self, "birthday") and self.birthday is not None:
            today = Birthday(date.today().strftime("%Y %m %d"))
            return self.birthday - today

    def add_memo(self, memo_str):
        if self.memos:
            raise ExistsMemo
        memo = Memo(memo_str)
        self.memos = memo

    def delete_memo(self):
        self.memos = None
        
    def add_address(self, adr_text):
        if self.address:
            raise ExistsAddress
        adr = Address(adr_text)
        self.address = adr
        
    def delete_address(self):
        self.address = None

    def __str__(self):

        msg = f"Contact name: {self.name.value}, phones: {', '.join(p.value for p in self.phones)}"
        if hasattr(self, "birthday"):
            msg += f", birthday: {date.strftime(self.birthday.value, '%d.%m.%Y')}"
        if self.emails:
            msg += f", e-mail: {self.emails}"
        if self.memos:
            msg += f", memos: {self.memos}"
        if self.address:
            msg += f", address: {self.address}"
        return msg

class AddressBook(UserDict):
    qua_for_iter = 10
    list_for_iter = []

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        record = self.data.get(name)
        if record is not None:
            return record
        else:
            raise KeyError
    
    def delete(self, name):
        self.data.pop(name)
    
    def find_records(self, search=None):
        list_rec = []
        for name, records in self.data.items():
            if search.lower() in name.lower():
                list_rec.append(records)
            elif hasattr(records, "memos") and records.memos and (search.lower() in records.memos.value.lower()):
                list_rec.append(records)
            elif hasattr(records, "address") and records.address and (search.lower() in records.address.value.lower()):
                list_rec.append(records)
            elif hasattr(records, "emails") and records.emails and (search.lower() in records.emails.value.lower()):
                list_rec.append(records)
            elif hasattr(records, "phones"):
                for phones in records.phones:
                    if search in phones.value:
                        list_rec.append(records)
        return list_rec
    
    def find_records_for_birthday(self, qua_days):
        list_rec = []
        for records in self.data.values():
            delta_day = records.days_to_birthday()
            if delta_day != None and delta_day <= qua_days:
                list_rec.append(records)
        return list_rec


    def exists_phone(self, phone=None):
        if phone is not None:
            phone_ = Phone(phone)
            for record_ in self.data.values():
                if phone_ in record_.phones:
                    raise ExistsPhone

    def __next__(self):
        if len(self.list_for_iter) == len(self.data):
            self.list_for_iter.clear()
            raise StopIteration
        iter = 0
        for_return = []
        for key, value in self.data.items():
            if key in self.list_for_iter:
                pass
            else:
                for_return.append(str(value))
                self.list_for_iter.append(key)
                iter += 1
            if len(for_return) == self.qua_for_iter:
                break
        # return for_return
        return f"{'; '.join(i for i in for_return)} \n"

    def __iter__(self):
        return self
    
    def save_to_file_pickle(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)
    
    def load_from_file_pickle(self, file_name):
        with open(file_name, 'rb') as file:
            return pickle.load(file)

    def __str__(self):
        ret_list = ""
        for record in self:
            ret_list += str(record)
        return ret_list

            
if __name__ == "__main__":
    pass

###############################################################################

    # book = AddressBook()

    # # # Створення запису для John
    # john_record = Record("John")
    # john_record.add_phone("0234567890")
    # john_record.add_phone("0234567891")
    # john_record.add_phone("(055)555-55-55")
    # john_record.add_birthday("17.12.1975")
    # # john_record.add_phone("(055)555-55-")
    # # print(john_record.days_to_birthday())

    # # # # # Додавання запису John до адресної книги
    # book.add_record(john_record)

    # # # # Створення запису для Jorjy
    # # # # Додавання запису Jorjy до адресної книги
    # jorjy_record = Record("Jorjy")
    # jorjy_record.add_phone("380888888888")
    # jorjy_record.add_birthday("01.01.1980")
    # book.add_record(jorjy_record)
    # # print(jorjy_record.days_to_birthday())

    # jorjy1_record = Record("Jorjy1")
    # jorjy1_record.add_phone("380888888888")
    # jorjy1_record.add_birthday("25.02.1975")
    # book.add_record(jorjy1_record)
    # # print(jorjy1_record.days_to_birthday())

    # jorjy2_record = Record("Jorjy2")
    # jorjy2_record.add_phone("380888888888")
    # # jorjy2_record.add_birthday("25.07.1975")
    # book.add_record(jorjy2_record)
    # # print(jorjy2_record.days_to_birthday())

    # print(book.find_records_for_birthday("500"))