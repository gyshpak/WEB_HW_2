"""Консольний бот для управління додатком"""
# import os
# import bot_helper.address_book as book
# import bot_helper.note_book as notebook
# import bot_helper.pretty as pretty
# from bot_helper.clean import sorting_files
# from bot_helper.commands import *

import os
import address_book as book
import note_book as notebook
import pretty as pretty
from clean import sorting_files
from commands import *


def input_error(func):
    """Функія-декоратор, що ловить помилки вводу"""
    def inner(my_book, val):
        try:
            return_data = func(my_book, val)
        except IndexError:
            return_data = ("Give me name please", )   #and phone please", )
        except TypeError:
            return_data = ("Wrong command, try again", )
        except KeyError:
            return_data = ("Wrong user, repeat please", )
        except ValueError:
            return_data = ("Wrong number, repeat please", )
        except book.WrongBirthday:
            return_data = ("Wrong birthday, repeat please", )
        except book.ExistsPhone:
            return_data = ("Phone is exist", )
        except book.ExistsMemo:
            return_data = ("User already has a memo", )
        except book.WrongMemo:
            return_data = ("Not printable characters in Memo or record size excides.", )
        except book.ExistsAddress:
            return_data = ("User already has an address", )
        except book.WrongAddress:
            return_data = ("Not printable characters in Address or record size excides.", )
        except book.WrongEmail:
            return_data = ("Wrong e-mail, repeat please", )
        except book.ExistsEmail:
            return_data = ("User already has an e-mail", )
        return return_data
    return inner


def handler_hello(my_book, _ = None):
    """Метод обробляє команду 'hello'
    """
    return "How can I help you?"

def handler_add(my_book, list_):
    """Метод обробляє команду 'add'
    """
    if list_[0] == "":
        raise IndexError
    my_book.exists_phone(list_[1])
    try:
        record = my_book.find(list_[0].capitalize())
    except:
        record = book.Record(list_[0].capitalize())
    else:
        my_book.add_record(record)
    finally:
        if list_[1] != "":
            record.add_phone(list_[1])
        if list_[2] != "":
            record.add_birthday(list_[2])
        if list_[3] != "":
            record.add_email(list_[3])
        if list_[4] != "":
            record.add_address(list_[4])
        if list_[5] != "":
            record.add_memo(list_[5])
        my_book.add_record(record)
    return "Command successfully complete"

def handler_change(my_book, list_):
    """Метод обробляє команду 'change'
    """
    my_book.exists_phone(list_[2])
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.edit_phone(list_[1], list_[2])
    return f"Phone {list_[1]} from user {list_[0].capitalize()} successfully changet to phone {list_[2]}"

def handler_add_email(my_book, list_):
    """Метод обробляє команду 'email-add'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        new_email = ' '.join(list_[1:])
        record.add_email(new_email)
        return f"To user {list_[0].capitalize()} successfully added e-mail:\n\t {new_email}"

def handler_delete_email(my_book, list_):
    """Метод обробляє команду 'email-delete'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.delete_email()
        return f"From user {list_[0].capitalize()} successfully deleted e-mail."

def handler_replace_email(my_book, list_):
    """Метод обробляє команду 'email-replace'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        email = record.emails.value
        record.delete_email()
        try:
            new_email = ' '.join(list_[1:])
            record.add_email(new_email)
            return f"For user {list_[0].capitalize()} e-mail successfully changed to:\n\t {new_email}"
        except:
            record.add_email(email)

def handler_add_memo(my_book, list_):
    """Метод обробляє команду 'memo-add'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        new_memo = ' '.join(list_[1:])
        record.add_memo(new_memo)
        return f"To user {list_[0].capitalize()} successfully added memo:\n\t {new_memo}"

def handler_delete_memo(my_book, list_):
    """Метод обробляє команду 'memo-delete'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.delete_memo()
        return f"From user {list_[0].capitalize()} successfully deleted memo."

def handler_replace_memo(my_book, list_):
    """Метод обробляє команду 'memo-replace'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        if record.memos is not None:
            memo = record.memos.value
            record.delete_memo()
            try:
                new_memo = ' '.join(list_[1:])
                record.add_memo(new_memo)
                return f"For user {list_[0].capitalize()} memo successfully changed to:\n\t {new_memo}"
            except:
                record.add_memo(memo)
        else:
            return handler_add_memo(my_book, list_)

def handler_add_addr(my_book, list_):
    """Метод обробляє команду 'address-add'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        new_addr = ' '.join(list_[1:])
        record.add_address(new_addr)
        return f"To user {list_[0].capitalize()} successfully added address:\n\t {new_addr}"

def handler_delete_addr(my_book, list_):
    """Метод обробляє команду 'address-delete'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.delete_address()
        return f"From user {list_[0].capitalize()} successfully deleted address."

def handler_replace_addr(my_book, list_):
    """Метод обробляє команду 'address-replace'
    """
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        if record.address is not None:
            addr = record.address.value
            record.delete_address()
            try:
                new_addr = ' '.join(list_[1:])
                record.add_address(new_addr)
                return f"For user {list_[0].capitalize()} address successfully changed to:\n\t {new_addr}"
            except:
                record.add_address(addr)
        else:
            return handler_add_addr(my_book, list_)

def handler_show_all(my_book, _ = None):
    """Метод обробляє команду 'show-all'
    """
    if my_book:
        return my_book
    return 'No users'

def handler_exit(my_book, _ = None):
    """Метод обробляє команди виходу """
    return "Good bye!"

def handler_back(my_book, _ = None):
    """Метод обробляє команди повернення до вибору режимів """
    return None

def handler_find(my_book, list_):
    """Метод обробляє команду 'find'
    """
    list_rec = my_book.find_records(list_[0].capitalize())
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        ret_book.qua_for_iter = my_book.qua_for_iter
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return "Contact not found"

def handler_find_birthday(my_book, list_):
    """Метод обробляє команду 'find-birthday'
    """
    qua_days = list_[0]
    if qua_days == "":
        qua_days = 10
    else:
        qua_days = int(qua_days)
    list_rec = my_book.find_records_for_birthday(qua_days)
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        ret_book.qua_for_iter = my_book.qua_for_iter
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return f"Contact for {qua_days} days not found"

def handler_delete_phone(my_book, list_):
    """Метод обробляє команду 'delete-telephone'
    """
    record = my_book.find(list_[0].capitalize())
    record.remove_phone(list_[1])
    return f"Phone {list_[1]} of user {list_[0].capitalize()} successfully deleted"

def handler_delete_user(my_book, list_):
    """Метод обробляє команду 'delete-user'
    """
    my_book.delete(list_[0].capitalize())
    return f"User {list_[0].capitalize()} successfully deleted"

def handler_next_birthday(my_book, list_):
    """Метод обробляє команду 'next-birthday'
    """
    record = my_book.find(list_[0].capitalize())
    days = record.days_to_birthday()
    return f"Next birthday for user {list_[0].capitalize()} after {days} days"

#Coded by Illia

def handler_add_note(my_book, list_):
    """Метод додає нотаток"""
    try:
        record = my_book.find(list_[0].capitalize())
    except:
        record = notebook.Record(list_[0].capitalize(),list_[1])

    record.add_tag(list_[2])
    my_book.add_record(record)
    return "Command successfully complete"

def handler_change_note(my_book, list_):
    """Метод змінює текст нотаток"""
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.edit_text(list_[1])
    return f"Text from note {list_[0].capitalize()} successfully changed"

def handler_find_note(my_book, list_):
    """Метод пошуку нотаток"""
    list_rec = my_book.find_records(list_[0].capitalize())
    if len(list_rec) != 0:
        ret_book = notebook.NoteBook()
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return "Note not found"

def handler_find_note_by_tag(my_book, list_):
    """Метод шукає нотаток за тегом"""
    list_rec = my_book.find_records_by_tag(list_[0].lower())
    if len(list_rec) != 0:
        ret_book = notebook.NoteBook()
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return "Note not found"

def handler_delete_tag(my_book, list_):
    """Метод видаляє тег"""
    record = my_book.find(list_[0].capitalize())
    record.remove_tag(list_[1].lower())
    return f"Tag {list_[1]} of note {list_[0].capitalize()} successfully deleted"

def handler_add_tag(my_book, list_):
    """Метод додає тег"""
    record = my_book.find(list_[0].capitalize())
    record.add_tag(list_[1])
    return f"Tag {list_[1]} of note {list_[0].capitalize()} successfully added"

def handler_delete_note(my_book, list_):
    """Метод видаляє нотатки"""
    my_book.delete(list_[0].capitalize())
    return f"Note {list_[0].capitalize()} successfully deleted"

def handler_show_all_notes(my_book, _=None):
    """Метод показує всі нотатки"""
    if my_book:
        return my_book
    return 'No notes'

def mode_change(my_book = None, _ = None):
    """Метод вибирає режим (книга контактів чи нотатки)"""
    i = True
    while i:
        mode = input("Please choose mode\n 1. Address book\n 2. Notes\n 3. Sort folder\n 4. Exit\n")
        if mode in "1234":
        # if mode == "1" or mode == "2" or mode == "3":
            return mode
        print("Wrong number!")

def handler_help(my_book = None, _ = None):
    """Метод обробляє команду 'help'
    """
    help_list = [
        ['help', 'command description'],
        ['hello', 'greets the user'],
        ['add <name> \[phone] \[birthday] \[Email] \[postal address] \[memos]',
        'for add user, if user is exist will be added\n'
        'variation format for telefon number:\n'
        '+38(055)111-22-33\n'
        '38(055)111-22-34\n'
        '8(055)111-22-35\n'
        '(055)111-22-36\n'
        '055111-22-37\n'
        'and all variant without "-"'],
        ['change <name> <from phone> <to phone>', 'for chandge phone'],
        ['show-all' , 'for show all records'],
        ['find <some letters> | find <some numbers>', 'for find record by name or phone'],
        ['delete-telephone <user> <phone>', 'for delete phone from user'],
        ['delete-user <user>', 'for delete user from address book'],
        ['email-add <name> <email text>', 'to add e-mail to user'],
        ['email-delete <name>', 'to delete Email from user'],
        ['email-replace <name> <new Email>', 'to replace existing Email with new text'],
        ['next-birthday <name>', 'shows the number of days until the subscriber`s next birthday'],
        ['finde-birthday \[number of days]', 'displaying a list of subscribers for the nearest specified number of days'],
        ['memo-add <name> <note text>',
            'to add note to user (max.240 printable characters)'],
        ['memo-delete <name>', 'to delete note from user'],
        ['memo-replace <name> <note text>', 'to replace existing note at user with new text'],
        ['address-add <name> <address text>', 'to add address to user (max.100 printable characters)'],
        ['address-delete <name>', 'to delete address from user'],
        ['address-replace <name> <new address>', 'to replace existing address at user with new text'],
        ['add-note <title> <text> \[tag]',' to add note'],
        ['change-note <title> <new_text>', 'to change text in note by title'],
        ['show-all-notes', 'to show all notes'],
        ['find-note <some text>', 'to find notes by <some_text> in title of note'],
        ['find-note-by-tag <some text>', 'to find notes by <some_text> in tags of note'],
        ['delete-note-tag <title> <tag>', 'to delete tag <tag> in note <title>'],
        ['add-note-tag <title> <tag>', 'to add tag <tag> in note <title>'],
        ['delete-note <title>', 'to delete note by <title>'],
        ['sort-folder <path>', 'sorts files in a folder path'],
        ['good-bye | close | exit', 'for exit']
    ]

    pretty.table(
        title='List of commands with format',
        header=['Command', 'Description'],
        rows=help_list,
    )
    return ""

NAME_COMMANDS = {

    "help": handler_help,
    "hello": handler_hello,
    "add": handler_add,
    "change": handler_change,
    "show-all": handler_show_all,
    "goodbye": handler_exit,
    "close": handler_exit,
    "exit": handler_exit,
    "find": handler_find,
    "delete-telephone": handler_delete_phone,
    "delete-user": handler_delete_user,
    "next-birthday": handler_next_birthday,
    "finde-birthday": handler_find_birthday,
    "sort-folder" : sorting_files,
    "email-add": handler_add_email,
    "email-delete": handler_delete_email,
    "email-replace": handler_replace_email,
    "memo-add": handler_add_memo,
    "memo-delete": handler_delete_memo,
    "memo-replace": handler_replace_memo,
    "address-add": handler_add_addr,
    "address-delete": handler_delete_addr,
    "address-replace": handler_replace_addr,
    "back": handler_back,
    "add-note": handler_add_note,
    "change-note": handler_change_note,
    "show-all-notes": handler_show_all_notes,
    "find-note": handler_find_note,
    "find-note-by-tag": handler_find_note_by_tag,
    "delete-note-tag": handler_delete_tag,
    "add-note-tag":handler_add_tag,
    "delete-note": handler_delete_note

}


def defs_commands(comm):
    """Метод додає до команди функцію"""
    return NAME_COMMANDS[comm]

@input_error
def parser_command(my_book, command):
    """Парсер команд"""
    list_command = command
    if list_command[0] in NAME_COMMANDS:
        any_command = defs_commands(list_command[0])
        ret_rezault = any_command(my_book, list_command[1:])
        return ret_rezault
    any_command = defs_commands()
    return ret_rezault


current_path = os.path.abspath(os.getcwd())
file_name_phones_p = os.path.join(current_path, 'bot_helper', 'book_pickle.bin')
file_name_notes_p = os.path.join(current_path, 'bot_helper', 'notes_book_pickle.bin')

def main():
    """Метод відновлює книги контактів та нотатки, обирає режим роботи"""
    # handler_help()

    if os.path.exists(file_name_phones_p):
        my_book_phones_p = book.AddressBook()
        my_book_phones = my_book_phones_p.load_from_file_pickle(file_name_phones_p)
    else:
        my_book_phones = book.AddressBook()
    if os.path.exists(file_name_notes_p):
        my_book_notes_p = notebook.NoteBook()
        my_book_notes = my_book_notes_p.load_from_file_pickle(file_name_notes_p)
    else:
        my_book_notes = notebook.NoteBook()
    
    ret_rezault = None
    while True:
        # #Вибір режиму (телефонна книга або нотатки)
        if ret_rezault == None:
            mode = mode_change()
        if mode == "1":
            command = get_command_suggestions("", mode)
            ret_rezault = parser_command(my_book_phones, command)
        elif mode == "2":
            command = get_command_suggestions("", mode)
            ret_rezault = parser_command(my_book_notes, command)
        elif mode == "3":
            command = ["sort-folder"]
            command.append(input("Please enter path for folder for sorting "))
            ret_rezault = parser_command(my_book_phones, command)
        elif mode == "4":
            ret_rezault = "Good bye!"
        if ret_rezault:
            pretty.parser(ret_rezault, mode)
            if ret_rezault == "Good bye!":
                my_book_phones.save_to_file_pickle(file_name_phones_p)
                my_book_notes.save_to_file_pickle(file_name_notes_p)
                exit()
        if mode == "3":
            ret_rezault = None

if __name__ == "__main__":
    main()
