from appdirs import AppDirs
from address_book import AddressBook, AddressContact, Birthday, EmailContact, Phone, Record
from colorama import Fore, Style, init
from notes import Notes, Note, Tag, Body
from sort import sort_fun
import os.path
import emoji

init()


"""
Бот помічник.
Працює з командами (див функцію help.)
"""

PHONE_BOOK = AddressBook()
NOTES = Notes()

DIRS = AppDirs("bot_man_save", "unbreakable")


def input_error(func):
    """
    Декоратор хендлера помилок.
    """

    def inner(*args, **kwargs):
        try:
            result = func(*args)
        except Exception as err:
            return err
        else:
            return result

    return inner


####################################### PHONE_BOOK #################################################


@input_error
def add(args):
    """
    Функція для додавання нового контакту до книги.
    """
    if not args:
        return "Передайте ім'я контакту та номер телефону"
    elif not args[1:]:
        return "Ви не передали номер телефону"

    name = args[0].capitalize()
    phone = args[1:][0]

    if name in PHONE_BOOK:
        return f"{name} вже у словнику"

    PHONE_BOOK.add_record(Record(name))
    PHONE_BOOK[name].add_information(PHONE_BOOK[name].phones, Phone(phone))
    return f"{name} was added with {phone}"


@input_error
def add_address(args):
    """
    Функція для додавання адреси до контакту.
    :return:
    """
    if not args:
        raise ValueError("Не було передано жодного аргументу, ім'я та адреси")

    name = args[0].capitalize()
    address = ' '.join(args[1:])

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в словнику"

    if address:
        PHONE_BOOK[name].add_information(PHONE_BOOK[name].address, AddressContact(address))
        return f" {address} was added to {name}"

    user_address = input("Введіть адресу: ")
    PHONE_BOOK[name].add_information(PHONE_BOOK[name].address, AddressContact(user_address))
    return f" {user_address} was added to {name}"


@input_error
def add_phone(args):
    """
    Функція для додавання телефону до контакту.
    :return:
    """
    if not args:
        return "Передайте ім'я контакту та номер телефону"

    name = args[0].capitalize()
    phone = None
    if args[1:]:
        phone = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if phone:
        PHONE_BOOK[name].add_information(PHONE_BOOK[name].phones, Phone(phone))
        return f" {phone} was added to {name}"

    user_phone = input("Введіть телефон: ")
    PHONE_BOOK[name].add_information(PHONE_BOOK[name].phones, Phone(user_phone))
    return f" {user_phone} was added to {name}"


@input_error
def add_birthday(args):
    """
    Функція для додавання дня народження до контакту.
    :return:
    """

    if not args:
        return "Передайте ім'я контакту та дату"

    birthday = None
    name = args[0].capitalize()
    if args[1:]:
        birthday = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if birthday:
        PHONE_BOOK[name].add_birthday(birthday)
        return f" {birthday} 🎇 додано до {name}"

    user_birthday = input("Введіть ДН: ")
    PHONE_BOOK[name].add_birthday(user_birthday)
    return f" {user_birthday} додано до {name}"


@input_error
def add_email(args):
    """
    Функція для додавання ел. пошти до контакту.
    """
    if not args:
        return "Передайте ім'я контакту та email"

    name = args[0].capitalize()
    email = None
    if args[1:]:
        email = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if email:
        PHONE_BOOK[name].add_information(PHONE_BOOK[name].email_list, EmailContact(email))
        return f" {email} додано до {name}"

    user_email = input("Введіть email: ")
    PHONE_BOOK[name].add_information(PHONE_BOOK[name].email_list, EmailContact(user_email))
    return f" {user_email} додано до {name}"


@input_error
def change_birthday(args):
    """
    Видаляє день народження у контакта. приймає імя контакту
    """
    if not args:
        return "Передайте ім'я контакту та нову дату"
    elif not args[1:]:
        return "Ви не передали нову дату"

    name = args[0].capitalize()
    new_date = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if PHONE_BOOK[name].birthday:
        PHONE_BOOK[name].birthday.value = new_date
        return f"{name} birthday was changing to {new_date}"

    PHONE_BOOK[name].add_birthday(new_date)
    return f"{new_date} was added to {name}"


@input_error
def del_birthday(args):
    """
    Видаляє день народження у контакта. приймає імя контакту
    """
    if not args:
        return "Передайте ім'я контакту"

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    if PHONE_BOOK[name].birthday:
        PHONE_BOOK[name].birthday = None
        return f"Birthday {name} was deleted"

    return "no info about birthday"


@input_error
def change_address(args):
    """
    Функція для редагування адреси контакту.
    :param args:
    :return:
    """
    if not args:
        return "Передайте ім'я контакту та адресу"

    name = args[0].capitalize()
    address = None

    if args[1:]:
        address = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]

    if address:
        record.change_information(AddressContact(address), record.address)
        return f" {address} was changed to {name}"

    user_address = input("Введіть нову адресу: ")
    record.change_information(AddressContact(user_address), record.address)
    return f" {user_address} was changed to {name}"


@input_error
def change_phone(args):
    """
    Функція для заміни телефону
    """
    if not args:
        return "Передайте ім'я контакту та телефон"

    name = args[0].capitalize()
    phone = None

    if args[1:]:
        phone = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]

    if phone:
        record.change_information(Phone(phone), record.phones)
        return f" {phone} was changed to {name}"

    user_phone = input("Введіть телефон: ")
    record.change_information(Phone(user_phone), record.phones)
    return f" {user_phone} was changed to {name}"


@input_error
def change_email(args):
    """
    Функція для редагування електронної пошти контакту.
    """
    if not args:
        return "Передайте ім'я контакту та email"

    name = args[0].capitalize()
    email = None
    if args[1:]:
        email = args[1:][0]

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]

    if email:
        record.change_information(EmailContact(email), record.email_list)
        return f" {email} was changed to {name}"

    user_email = input("Введіть email: ")
    record.change_information(EmailContact(user_email), record.email_list)
    return f" {user_email} was changed to {name}"


@input_error
def show_contact(args):
    """
    Функція виводить всі контакти в книзі. Якщо передано імя виведе данні по цьому контакту
    """
    separate = 30 * '-'
    if args:
        name = args[0].capitalize()
        return f'{separate} \n{PHONE_BOOK.get(name, "no such name")} \n{separate}'

    result = ''
    for contact in PHONE_BOOK:
        result += f'\n{PHONE_BOOK[contact]} \n{separate}'

    return result


@input_error
def search_contacts(args):
    """
    Функція для пошуку контакту.
    """

    if not args:
        return show_contact(args)

    result = ""
    contacts = PHONE_BOOK.search_contacts(args)

    if contacts:
        for contact in contacts:
            result += show_contact([contact.name.value]) +'\n'
        return result
     
    return f"no contacts with such request: {args[0]}"


@input_error
def search_birthday(args):
    """
    Функція повертає всі контакти, в яких
    ДН через days днів
    """
    if not args:
        return "Введіть будь ласка дні"

    days = 7

    try:
        days = int(args[0])
    except ValueError:
        print("Введіть будь ласка числове значення")

    data = PHONE_BOOK.search_contacts_birthday(days)

    if not data:
        if days > 0:
            return f"У жодного з ваших контактів немає дня народження впродовж {days} днів."
        elif days < 0:
            return f"У жодного з ваших контактів не було дня народження {days * (-1)} днів назад"

    to_return = []
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]))

    for contact in sorted_data:
        if sorted_data[contact] == 0:
            to_return.append(
                f"У {contact} сьогодні день народження")
        elif sorted_data[contact] > 0:
            to_return.append(
                f"{contact} має день народження через {data[contact]} дні")
        elif sorted_data[contact] < 0:
            to_return.append(
                f"В {contact} був день народження {data[contact] * (-1)} днів назад")

    return "\n".join(to_return)


@input_error
def delete_address(args):
    """
    Функція для видалення адреси у контакта.
    """
    if not args:
        raise ValueError("Не було введено ім'я контакту для видалення адреси.")

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено у словнику"

    record = PHONE_BOOK[name]
    result = record.delete_information(record.address)

    return result


@input_error
def delete_phone(args):
    """
    функція для видалення номеру телефона
    """
    if not args:
        return "Введіть будь ласка І'мя"

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"{name} ім'я не знайдено у словнику"

    record = PHONE_BOOK[name]
    result = record.delete_information(record.phones)

    return result


@input_error
def delete_email(name):
    """
    функція для видалення вибраної ел. пошти у контакта
    """

    if not name:
        return "Не було введенно жодного аргументу..."

    name = name[0].title()

    if name not in PHONE_BOOK:
        return f" {name} імя не знайдено в адресній книзі, ви можете додати {name} ввівши команду add."

    record = PHONE_BOOK[name]
    result = record.delete_information(record.email_list)
    return result


@input_error
def delete_contact(args):
    """
    Функція видалення контакта з книги
    """
    if not args:
        return "Введіть будь ласка І'мя"

    name = args[0].capitalize()

    if name not in PHONE_BOOK:
        return f"Контакту {name} немає у словнику."

    contact = PHONE_BOOK.delete_record(name)
    return f"{contact} був видалений з книги"


def good_bye(*args):
    """
    Функція для завершення роботи бота.
    """
    save()
    print(f"👋🎅{Fore.CYAN}До побачення{Style.RESET_ALL}👋🎅")
    quit()


def helps(*args):
    """
    Функція повертає список команд на які реагує бот.
    """

    commands = [
        f'{Fore.GREEN}add{Style.RESET_ALL} - will adding new contact to you addressbook in format add: [Name][Phone]',
        f'{Fore.GREEN}add phone{Style.RESET_ALL} - will adding phone to contact in format add: [Name] [Phone]',
        f'{Fore.GREEN}add address{Style.RESET_ALL} - will adding new address to contact in format: [Name] [address]',
        f'{Fore.GREEN}add email{Style.RESET_ALL} - will adding new address to contact in format: [Name] [email]',
        f'{Fore.GREEN}add birthday{Style.RESET_ALL} - will adding new address to contact in format: [Name] [birthday][DD.MM.YYYY]',
        f'{Fore.GREEN}change address{Style.RESET_ALL} - will change address of you contact. format for change: [Name] [New address]',
        f'{Fore.GREEN}change email{Style.RESET_ALL} - will change email of you contact. format for change: [Name] [New email]',
        f'{Fore.GREEN}change phone{Style.RESET_ALL} - will change old phone with new value. format for change: [Name] [New phone]',
        f'{Fore.GREEN}search contacts{Style.RESET_ALL} - will search all contacts by name or phone number. format: [searching text]',
        f'{Fore.GREEN}show contact{Style.RESET_ALL} - will show all contacts. Show without name will show all contacts. format: [searching text]',
        f'{Fore.GREEN}change birthday{Style.RESET_ALL} - will change contact Bday. format [name][new date]',
        f'{Fore.GREEN}delete birthday{Style.RESET_ALL} - will delete contact Bday. format [name]',
        f'{Fore.GREEN}delete contact{Style.RESET_ALL} - will delete contact. format [name]',
        f'{Fore.GREEN}delete address{Style.RESET_ALL} - will delete address. format [name]',
        f'{Fore.GREEN}delete email{Style.RESET_ALL} - will delete selected contact email. format [Name] [email]',
        f'{Fore.GREEN}search birthday{Style.RESET_ALL} - will show you upcoming Bday in  "n" days. format [quantity of days]',
        f'{Fore.GREEN}save{Style.RESET_ALL} - will save you addressbook and notes',
        f'{Fore.GREEN}load{Style.RESET_ALL} - will load you addressbook and notes',
        f'{Fore.GREEN}sort{Style.RESET_ALL} - will make magik and sort you files. Give only dir ;)',

        f'{Fore.BLUE}add note{Style.RESET_ALL} - will adding new note',
        f'{Fore.BLUE}del note{Style.RESET_ALL} - will delete note. format: [record number]',
        f'{Fore.BLUE}change note{Style.RESET_ALL} - will changing note. format: [record number] [new text]',
        f'{Fore.BLUE}change tag{Style.RESET_ALL} - will add or delete tag to you note',
        f'{Fore.BLUE}show notes{Style.RESET_ALL} - will show you all notes',
        f'{Fore.BLUE}sort notes{Style.RESET_ALL} - will show you note with sort. 1/-1 to asc/desc sorting',
        f'{Fore.BLUE}search notes{Style.RESET_ALL} - will searching note for you by text',
        f'{Fore.BLUE}search tag{Style.RESET_ALL} - will searching note for you by tag',

        f'{Fore.RED}good_bye{Style.RESET_ALL} - for exit',
        ]

    return '\n'.join(commands)


def break_f(*args):
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... Try Help"


####################################### NOTES #################################################


@input_error
def add_note(*args):
    """
    Функція викликає окремій юзерінпут і створює Нотатку з тегами.
    """

    while True:
        body = input("Введіть текст нотатки:\n")
        if not body:
            print("введіть текст або оберіть cansel")
        elif body == "cansel":
            return
        else:
            break

    while True:
        tag = input("додайте теги:\n")
        if not tag:
            print("введіть текст або оберіть cansel")
        elif tag == "cansel":
            return
        else:
            break

    NOTES.add_record(Note(tag, body))

    return "Нотатку створено"


@input_error
def del_note(args):
    """
    На вході приймає номери нотатків які треба видалити, при наявності таких видаляє.
    """
    if args:
        number = args
    else:
        raise Exception("Ви не ввели номер нотатки")

    del_numbers = []
    for i in number:
        try:
            del NOTES[int(i) - 1]  # нотатки виводятся з 1
        except IndexError:
            print(f"немає нотатки з таким номером {int(i)}")
        else:
            del_numbers.append(int(i))

    return f"нотатки {del_numbers} були видалені"


@input_error
def change_note(args):
    """
    Приймає номер нотатку і новий текст. міняє.
    """
    if not args:
        raise Exception('Ви не передали номеру нотатки та новий текст')
    # elif not args[1:]:
    #     raise Exception('Ви не передали новий текст')

    number = int(args[0])
    new_text = ' '.join(args[1:])

    if not new_text:
        new_text = input("Введіть новий текст:\n")

    NOTES.cahange_note_text(number - 1, new_text)  # нотатки виводятся з 1

    return f"Нотатка №{number} була змінена"


@input_error
def change_tag(args):
    """Функція дізнається у користувача що саме він хоче зробити, додати чи видалити тег, номер і тег.
    Відповідно до вибору видалить чи додасть тег до обранної нотатки."""

    while True:
        action = input("Оберіть дію add/del:\n")
        if action == "cancel":
            return
        elif not action or action not in ['add', 'del']:
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    while True:
        number = input("Введіть номер нотатки:\n")
        if number == "cancel":
            return
        elif not number or not number.isdigit() or int(number) > len(NOTES):
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    while True:
        tag = input("Введіть тег:\n")
        if tag == "cancel":
            return
        elif not tag:
            print("не коректне значення, для того щоб відмінити дію - оберіть cancel")
        else:
            break

    if action == "add":
        NOTES[int(number) - 1].add_tag(tag)
        return 'Tag was added'
    else:
        NOTES[int(number) - 1].del_tag(tag)
        return 'Tag was deleted'


@input_error
def sort_notes(args):
    """
    Функція для сортування нотаток.
    """
    if args:
        number = int(args[0])
        if number not in [1, -1]:
            return "1 чи порожньо для сортування, -1 для зворотнього сортування"
        return NOTES.sort_notes(number)
    else:
        return NOTES.sort_notes()


def show_notes(args):
    return NOTES.get_notes()


@input_error
def search_notes(args):
    """
    Функція для пошуку нотатки.
    """
    text = ' '.join(args)
    return NOTES.search(text)


@input_error
def search_tag(args):
    """
    Функція для пошуку нотатки за тегом.
    """

    search_args = args

    if search_args:
        result = ""
        for i in search_args:
            print(i)
            result += NOTES.search_by_tag(i)
        if result:
            return result
        else:
            return "нотаток не виявлено"
    else:
        return "ви не вибрали жотдного тегу"


@input_error
def save(*args):
    """
    Функція збереження data.
    """
    global DIRS

    if not os.path.isdir(DIRS.user_data_dir):
        os.makedirs(DIRS.user_data_dir)

    path_addressbook = os.path.abspath(DIRS.user_data_dir + "/save_data.bin")
    path_notes = os.path.abspath(DIRS.user_data_dir + "/save_notes.bin")

    NOTES.dump_data(NOTES.data, path_notes)
    PHONE_BOOK.dump_data(PHONE_BOOK.data, path_addressbook)

    return f"{Fore.RED}data saved in {DIRS.user_data_dir}{Style.RESET_ALL}"


@input_error
def load(*args):
    """
    Функція завантаження data.
    """
    global DIRS
    global NOTES
    global PHONE_BOOK

    path_addressbook = os.path.abspath(DIRS.user_data_dir + "/save_data.bin")
    path_notes = os.path.abspath(DIRS.user_data_dir + "/save_notes.bin")

    if os.path.isfile(path_notes):
        NOTES = Notes(NOTES.load_data(path_notes))

    if os.path.isfile(path_addressbook):
        PHONE_BOOK = AddressBook(PHONE_BOOK.load_data(path_addressbook))

    return f"{Fore.RED}data loaded from {DIRS.user_data_dir}{Style.RESET_ALL}"


def levinstein(str_1, str_2):
    '''Алгоритм Левыншейна, порывнюэ 2 текста ы повертає кількість символів на які вони відрізняються'''
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + \
                1, current_row[j - 1] + 1, previous_row[j - 1]

            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return round(current_row[n] / len(str_1), 5) * 100  # current_row[n] #


def min_fun(value):
    '''знаходить найближче значення до переліку функцій бота'''
    functions = ['add', 'add address', 'add bd', 'add bday', 'add birthday', 'add email', 'add note', 'add phone',
                 'change address',
                 'change bd', 'change bd', 'change bday', 'change birthday', 'change email', 'change note',
                 'change phone',
                 'change tag', 'close', 'del address', 'del bd', 'del bday', 'del birthday', 'del contact', 'del email',
                 'del note',
                 'del phone', 'del phone', 'delete address', 'delete bd', 'delete bday', 'delete birthday',
                 'delete contact',
                 'delete email', 'delete note', 'delete phone', 'exit', 'good bye', 'hello', 'help', 'load', 'save',
                 'search birthday','search bday', 'search contacts', 'search notes', 'search tag', 'show contact', 'show notes',
                 'sort',
                 'sort notes']

    result = [float('inf'), '']
    for item in functions:
        close = levinstein(value, item)
        if close < result[0]:
            result[0], result[1] = close, item

    return result


def analyze_fun(user_input):
    '''Аналізує як поділити введений текст, перші 2 слова чи перше слово на функцію та решту. Для 2ух слів є випередження 25% можливо налаштувати'''
    splited = user_input.split()
    one_element_match = splited[0]

    if not splited[1:]:
        return (min_fun(one_element_match)[1], [])
    else:
        two_element_match = ' '.join(splited[:2])
        rest_one_element = splited[1:]
        rest_two_element = splited[2:]

        one_element_result = min_fun(one_element_match)
        two_element_result = min_fun(two_element_match)

        if two_element_result[0] - 25 < one_element_result[0]:
            return (two_element_result[1], rest_two_element)
        else:
            return (one_element_result[1], rest_one_element)

##############################################################################################################################


def fun_name(fun):
    """
    Хендлер команд від користувача.
    """

    fun_dict = {
        "hello": helps,
        "help": helps,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        "add": add,
        "add phone": add_phone,
        "add address": add_address,
        "add birthday": add_birthday,
        "add bday": add_birthday,
        "add bd": add_birthday,
        "del birthday": del_birthday,
        "del bday": del_birthday,
        "del bd": del_birthday,
        "delete birthday": del_birthday,
        "delete bday": del_birthday,
        "delete bd": del_birthday,
        "change birthday": change_birthday,
        "change bday": change_birthday,
        "change bd": change_birthday,
        "change address": change_address,
        "search contacts": search_contacts,
        "sort": sort_fun,
        "add note": add_note,
        "del note": del_note,
        "delete note": del_note,
        "change note": change_note,
        "change tag": change_tag,
        "sort notes": sort_notes,
        "show notes": show_notes,
        "search notes": search_notes,
        "search tag": search_tag,
        "save": save,
        "load": load,
        "change phone": change_phone,
        "delete phone": delete_phone,
        "del phone": delete_phone,
        "show contact": show_contact,
        "add email": add_email,
        "change email": change_email,
        "delete email": delete_email,
        "del email": delete_email,
        "search birthday": search_birthday,
        "search bday": search_birthday,
        "delete contact": delete_contact,
        "del contact": delete_contact,
        "delete address": delete_address,
        "del address": delete_address

    }

    return fun_dict.get(fun, break_f)


def show_logo():
    """
    Логотип при запуску.
    """
    print("\n"
            f"👋🎅{Fore.CYAN}Вітання{Style.RESET_ALL} {Fore.RED}від {Style.RESET_ALL}{Fore.GREEN}команди{Style.RESET_ALL} {Fore.YELLOW}PyGeniuses{Style.RESET_ALL}👋🎅\n")
      
