from json import load, dump
from prettytable import PrettyTable
from math import ceil


'''
Запись телефонного справочника имеет следующую структуру:
    id: int — номер записи справочника
    surname: str — фамилия 
    name: str — имя
    patronymic: str — отчество
    organization: str — название организации
    phoneWork: str — рабочий телефон
    phonePersonal: str — личный телефон
'''


# Строковая константа с названием json-файла, в котором хранится справочник
PHONEBOOK_FILENAME = "phonebook.json"


def read_json_phonebook(phonebook_filename: str) -> list[dict[str, str | int]]:
    '''Принимает строку с названием файла справочника, возвращает его 
    содержимое в формате json
    '''
    phonebook_json: list = []
    try:
        with open(phonebook_filename, 'r', encoding='utf-8') as f: 
            phonebook_json = load(f)
    except Exception as e:
        print("Произошла ошибка при чтении файла:", e)
    return phonebook_json


def write_json_phonebook(phonebook_filename: str, modified_json_data: list[dict[str, str | int]]) -> None:
    '''Принимает строку с названием файла справочника и данные для записи
      в формате json, записывает данные в указанный файл'''
    try:
        with open(phonebook_filename, "w", encoding='utf-8') as f:
            dump(modified_json_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Произошла ошибка при записи файла:", e)


def transform_json_to_table(phonebook_json: list[dict[str, str | int]]) -> PrettyTable:
    '''Принимает содержимое справочника в формате json и преобразовывает
      в таблицу с использованием библиотеки prettytable'''
    table = PrettyTable()
    table.title = "Телефонный справочник"
    table.field_names = ["№", 
                         "Фамилия", 
                         "Имя", 
                         "Отчество", 
                         "Организация", 
                         "Телефон (рабочий)", 
                         "Телефон (личный)"]
    table.hrules = True

    if phonebook_json:
        for row in phonebook_json:
            table.add_row(row.values())
    return table


def display_table_by_pages(phonebook_table: PrettyTable) -> None:
    '''Принимает сформированную с помощью prettytable таблицу и осуществляет
      постраничный вывод в консоль'''
    page_size: int = 5
    start_row: int = 0
    last_page_number: int = ceil(len(phonebook_table._rows) / page_size)
    while start_row < len(phonebook_table._rows):
        print(phonebook_table.get_string(start=start_row, end=min(start_row + page_size, len(phonebook_table._rows))))

        current_page_number: int = start_row // page_size + 1
        
        print(f'\nСтраница {current_page_number}/{last_page_number}\n')
        
        start_row += page_size

        if start_row < len(phonebook_table._rows):
            decision = input("Нажмите Enter для отображения следующей страницы, или введите 'q' для отмены дальнейшего вывода: ")
            if decision.lower() == 'q':
                break


def read_phonebook(phonebook_filename: str) -> None:
    '''Функция-агрегатор: принимает строку с названием файла справочника,
      выводит содержимое в виде таблицы постранично на экран'''
    phonebook_json = read_json_phonebook(phonebook_filename)
    if phonebook_json:
        phonebook_table = transform_json_to_table(phonebook_json)
        display_table_by_pages(phonebook_table)
    else:
        print("Справочник пуст.")


def input_new_entry() -> dict[str, str | int]:
    '''Осуществляет ввод записи для добавления в справочник, возвращает введенную запись'''
    new_entry: dict = {'id':-1}

    variable_names: list = ['surname', 'name', 'patronymic', 'organization', 'phoneWork', 'phonePersonal']

    for var_name in variable_names:
        user_input = input(f"Введите значение для поля {var_name} (или 'q' для отмены): ")
            
        if user_input.lower() == 'q':
            print("Ввод отменен.")
            break
        
        new_entry[var_name] = user_input

    return new_entry if len(new_entry) - 1 == len(variable_names) else {}    # Если заполнены не все поля, возвращаем пустой словарь


def add_entry_to_phonebook(phonebook_filename: str, new_entry: dict[str, str | int]) -> None:
    '''Функция-агрегатор: принимает строку с названием файла справочника и новой записью в формате словаря,
    записывает переданную запись в файл справочника'''
    phonebook_json = read_json_phonebook(phonebook_filename)

    new_entry['id'] = max((id.get('id', 0) for id in phonebook_json), default=0) + 1
    phonebook_json.append(new_entry)

    write_json_phonebook(phonebook_filename, phonebook_json)


def input_entry_id_to_edit() -> int:
    '''Осуществляет ввод номера записи справочника для ее изменения, возвращает введенный номер записи'''
    entry_id = input("Введите № записи, которую хотите отредактировать: ")

    if entry_id.isdigit():
        entry_id = int(entry_id)
    else:
        print("Введен неверный символ, ввод отменен.")
        entry_id = 0

    return entry_id


def input_new_values_to_edit(phonebook_filename: str, entry_id: int) -> dict[str, str | int]:
    '''Принимает строку с названием файла справочника и номер записи, 
    осуществляет ввод новых значений для записи под данным номером, возвращает введенные значения'''
    new_values: dict = {}

    entry = find_entries_by_values(read_json_phonebook(phonebook_filename), {'id':entry_id})
    if not entry:
        print("Записи под данным номером в справочнике нет.")
        return new_values

    for key, value in entry[0].items():
        if key == 'id':
            continue

        user_input = input(f"\nВведите значение для поля {key} | Текущее значение: {value}\nНажмите Enter, если хотите оставить текущее значение (или 'q' для отмены редактирования): ")
            
        if user_input.lower() == 'q':
            print("Редактирование отменено.")
            new_values = {}
            break
        elif not user_input:
            continue
        else:
            new_values[key] = user_input

    return new_values


def replace_values_in_entry(phonebook_json: list[dict[str, str | int]], entry_id: int, new_values: dict[str, str | int]) -> list[dict[str, str | int]]:
    '''Принимает содержимое справочника в формате json, номер изменяемой записи и данные
      для замены в этой записи в формате словаря, возвращает измененный json-справочник'''
    for entry in phonebook_json:
        if entry.get('id') == entry_id: 
            for key, value in new_values.items():
                entry[key] = value
    return phonebook_json


def edit_phonebook_entry(phonebook_filename: str) -> None:
    '''Функция-агрегатор: принимает строку с названием файла справочника,
    осуществляет ввод номера записи и новых данных для замены в ней, производит замену значений записи'''
    entry_id = input_entry_id_to_edit()
    if entry_id:
        new_values = input_new_values_to_edit(phonebook_filename, entry_id)
        if new_values:
            phonebook_json = read_json_phonebook(phonebook_filename)
            phonebook_json = replace_values_in_entry(phonebook_json, entry_id, new_values) 
            write_json_phonebook(phonebook_filename, phonebook_json)


def input_values_to_find() -> dict[str, str | int]:
    '''Осуществляет ввод характеристик, по которым производится поиск записей, возвращает введенные характеристики'''
    find_menu = '''
Выберите номер поля из списка, по которому будет производиться поиск, или завершите поиск:
1. Фамилия
2. Имя
3. Отчество
4. Организация
5. Телефон (рабочий)
6. Телефон (личный)
0. Отмена поиска
'''
    required_values: dict = {}

    field_num: int = 42
    while field_num:
        print(find_menu) if not required_values else print(find_menu + "7. Осуществить поиск по заданным полям")
        try:
            field_num = int(input())
        except:
            field_num = 42
            print("Введен неверный символ.")
        if field_num == 1:
            in_value = input("Введите искомое значение поля Фамилия: ")
            if in_value:
                required_values['surname'] = in_value
        elif field_num == 2:
            in_value = input("Введите искомое значение поля Имя: ")
            if in_value:
                required_values['name'] = in_value
        elif field_num == 3:
            in_value = input("Введите искомое значение поля Отчество: ")
            if in_value:
                required_values['patronymic'] = in_value
        elif field_num == 4:
            in_value = input("Введите искомое значение поля Организация: ")
            if in_value:
                required_values['organization'] = in_value
        elif field_num == 5:
            in_value = input("Введите искомое значение поля Телефон (рабочий): ")
            if in_value:
                required_values['phoneWork'] = in_value
        elif field_num == 6:
            in_value = input("Введите искомое значение поля Телефон (личный): ")
            if in_value:
                required_values['phonePersonal'] = in_value
        elif field_num == 7 and required_values:
            break
        elif field_num == 0:
            required_values = {}
        
    return required_values


def find_entries_by_values(phonebook_json: list[dict[str, str | int]], required_values: dict[str, str | int]) -> list[dict[str, str | int]]:
    '''Принимает содержимое справочника в формате json и словарь с искомыми значениями
      характеристик, возвращает найденные записи из справочника, соответствующие этим значениям'''
    found_entries: list = []

    for entry in phonebook_json:
        match = True
        for key, value in required_values.items():
            if entry.get(key) != value:
                match = False
                break

        if match:
            found_entries.append(entry)

    return found_entries


def find_phonebook_entries(phonebook_filename: str):
    '''Функция-агрегатор: принимает строку с названием файла справочника, осуществляет поиск записей'''
    required_values = input_values_to_find()
    if required_values:
        phonebook_json = read_json_phonebook(phonebook_filename)

        found_entries = find_entries_by_values(phonebook_json, required_values)
        if found_entries:
            display_table_by_pages(transform_json_to_table(found_entries))
        else:
            print("К сожалению, записей с данными характеристиками найдено не было.")


def show_menu() -> None:
    '''Выводит меню'''
    print('''
Выберите опцию из списка:
1. Показать записи справочника
2. Добавить новую запись в справочник
3. Отредактировать существующую запись справочника
4. Найти записи справочника по определенным характеристикам
0. Выход
''')


def menu_interaction() -> None:
    '''Осуществляет взаимодействие с пользователем; выводит меню и обрабатывает ввод'''
    phonebook_filename: str = PHONEBOOK_FILENAME

    menu_option: int = 42
    while menu_option:
        show_menu()
        try:
            menu_option = int(input())
        except:
            menu_option = 42
            print("Необходимо ввести номер опции из списка меню.")

        if menu_option == 1:
            read_phonebook(phonebook_filename)
        elif menu_option == 2:
            new_entry = input_new_entry()
            if new_entry:
                add_entry_to_phonebook(phonebook_filename, new_entry)
        elif menu_option == 3:
            edit_phonebook_entry(phonebook_filename)
        elif menu_option == 4:
            find_phonebook_entries(phonebook_filename)
        else:
            pass


def main() -> None:
    '''Основная функция; точка входа'''
    menu_interaction()


if __name__ == '__main__':
    main()
