documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def check_document_existance(doc_number):
    """
    Проверяет, существует ли документ с указанным номером.
    """
    return any(doc['number'] == doc_number for doc in documents)


def get_doc_owner_name(doc_number):
    """
    Возвращает имя владельца документа по его номеру.
    """
    for doc in documents:
        if doc['number'] == doc_number:
            return doc['name']
    return None


def get_all_doc_owners_names():
    """
    Возвращает множество имён всех владельцев документов.
    """
    return {doc['name'] for doc in documents if 'name' in doc}


def remove_doc_from_shelf(doc_number):
    """
    Удаляет документ из полки (из directories).
    """
    for shelf in directories.values():
        if doc_number in shelf:
            shelf.remove(doc_number)
            break


def add_new_shelf(shelf_number=None):
    """
    Добавляет новую полку, если её ещё нет.
    """
    if shelf_number is None:
        return None, False  # Защита от ошибок, если не передано
    if shelf_number not in directories:
        directories[shelf_number] = []
        return shelf_number, True
    return shelf_number, False


def append_doc_to_shelf(doc_number, shelf_number):
    """
    Добавляет документ на указанную полку.
    """
    if shelf_number not in directories:
        add_new_shelf(shelf_number)
    directories[shelf_number].append(doc_number)


def delete_doc(doc_number):
    """
    Удаляет документ из каталога и с полки.
    """
    if not check_document_existance(doc_number):
        return doc_number, False
    # Удаляем из списка документов
    for doc in documents:
        if doc['number'] == doc_number:
            documents.remove(doc)
            break
    # Удаляем с полки
    remove_doc_from_shelf(doc_number)
    return doc_number, True


def get_doc_shelf(doc_number):
    """
    Возвращает номер полки, на которой находится документ.
    """
    if not check_document_existance(doc_number):
        return None
    for shelf_number, doc_list in directories.items():
        if doc_number in doc_list:
            return shelf_number
    return None


def move_doc_to_shelf(doc_number, shelf_number):
    """
    Перемещает документ с текущей полки на указанную.
    """
    remove_doc_from_shelf(doc_number)
    append_doc_to_shelf(doc_number, shelf_number)
    return f'Документ номер "{doc_number}" был перемещен на полку номер "{shelf_number}"'


def show_document_info(document):
    """
    Форматирует информацию о документе.
    """
    return '{} "{}" "{}"'.format(document['type'], document['number'], document['name'])


def show_all_docs_info():
    """
    Возвращает список строк с информацией о всех документах.
    """
    result = []
    result.append('Список всех документов:\n')
    for doc in documents:
        result.append(show_document_info(doc))
    return result


def add_new_doc(doc_number, doc_type, doc_owner_name, shelf_number):
    """
    Добавляет новый документ в каталог и на полку.
    """
    new_doc = {
        "type": doc_type,
        "number": doc_number,
        "name": doc_owner_name
    }
    documents.append(new_doc)
    append_doc_to_shelf(doc_number, shelf_number)
    return f'На полку "{shelf_number}" добавлен новый документ: {doc_number}'


def secretary_program_start():
    """
    Основной цикл программы.
    """
    print(
        'Вас приветствует программа помошник!\n',
        '(Введите help, для просмотра списка поддерживаемых команд)\n'
    )
    while True:
        user_command = input('Введите команду - ')
        if user_command == 'p':
            doc_number = input('Введите номер документа - ')
            owner_name = get_doc_owner_name(doc_number)
            if owner_name:
                print('Владелец документа - {}'.format(owner_name))
            else:
                print('Документ не найден')
        elif user_command == 'ap':
            owners = get_all_doc_owners_names()
            print('Список владельцев документов - {}'.format(owners))
        elif user_command == 'l':
            docs_info = show_all_docs_info()
            print('\n'.join(docs_info))
        elif user_command == 's':
            doc_number = input('Введите номер документа - ')
            shelf = get_doc_shelf(doc_number)
            if shelf:
                print('Документ находится на полке номер {}'.format(shelf))
            else:
                print('Документ не найден')
        elif user_command == 'a':
            doc_number = input('Введите номер документа - ')
            doc_type = input('Введите тип документа - ')
            doc_owner_name = input('Введите имя владельца документа - ')
            shelf_number = input('Введите номер полки для хранения - ')
            message = add_new_doc(doc_number, doc_type, doc_owner_name, shelf_number)
            print(message)
        elif user_command == 'd':
            doc_number = input('Введите номер документа - ')
            _, deleted = delete_doc(doc_number)
            if deleted:
                print('Документ с номером "{}" был успешно удален'.format(doc_number))
            else:
                print('Документ не найден')
        elif user_command == 'm':
            doc_number = input('Введите номер документа - ')
            shelf_number = input('Введите номер полки для перемещения - ')
            message = move_doc_to_shelf(doc_number, shelf_number)
            print(message)
        elif user_command == 'as':
            shelf_number = input('Введите номер новой полки - ')
            _, added = add_new_shelf(shelf_number)
            if added:
                print('Добавлена полка "{}"'.format(shelf_number))
            else:
                print('Полка уже существует')
        elif user_command == 'help':
            print(secretary_program_start.__doc__)
        elif user_command == 'q':
            break