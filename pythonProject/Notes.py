from csv import DictReader, DictWriter
from os.path import exists
from datetime import datetime


def create_file():
    with open('notes.csv', 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['ID Заметки', 'Заголовок заметки', 'Содержание заметки',
                                                'Дата/время последнего изменения'], delimiter=';')
        f_writer.writeheader()


def overwrite_file(file_name, new_info):
    if exists(file_name):
        with open('notes.csv', 'w', encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['ID Заметки', 'Заголовок заметки', 'Содержание заметки',
                                                    'Дата/время последнего изменения'], delimiter=';')
            f_writer.writeheader()
            f_writer.writerows(new_info)


def get_info():
    note_id = 0
    lst = read_file('notes.csv')
    if len(lst) != 0:
        note_id = int(lst[len(lst) - 1]['ID Заметки'])
    title = input('Введите заголовок заметки: ')
    body = input('Введите тело заметки: ')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    info = [note_id + 1, title, body, dt_string]
    return info


def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:
        f_reader = DictReader(data, delimiter=';')
        res = list(f_reader)
    return res


def read_at_date(file_name):
    date = input('Введите дату, по которой необходимо сделать выборку, в формате dd/mm/yyyy: ')
    flag = True
    with open(file_name, encoding='utf-8') as data:
        f_reader = DictReader(data, delimiter=';')
        lst = list(f_reader)
        res = []
        for row in lst:
            row_date = row['Дата/время последнего изменения'].split(' ')[0]
            if row_date == date:
                res.append(row)
                flag = False
    if flag is True:
        print('В этот день заметок сделано не было')
    return res


def write_note(file_name, lst):
    res = read_file(file_name)
    obj = {'ID Заметки': lst[0], 'Заголовок заметки': lst[1], 'Содержание заметки': lst[2],
           'Дата/время последнего изменения': lst[3]}
    res.append(obj)
    overwrite_file(file_name, res)


def delete_note(file_name):
    note_id = input('Введите id удаляемой заметки: ')
    res = read_file(file_name)
    flag = True
    for el in res:
        if el['ID Заметки'] == note_id:
            res.remove(el)
            flag = False
    if flag is True:
        print('Заметки с таким id не существует!')
    else:
        overwrite_file(file_name, res)


def update_note(file_name):
    note_id = input('Введите id изменяемой заметки: ')
    flag = True
    res = read_file(file_name)
    for el in res:
        if el['ID Заметки'] == note_id:
            flag = False
            el['Заголовок заметки'] = input('Введите новый заголовок: ')
            el['Содержание заметки'] = input('Введите новое тело заметки: ')
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            el['Дата/время последнего изменения'] = dt_string
    if flag is True:
        print('Заметки с таким id не существует!')
    else:
        overwrite_file(file_name, res)


def main():
    while True:
        print('add -       добавить новую заметку')
        print('read -      прочитать все существующие заметки')
        print('read_date - прочитать заметки, сделанные в указанную дату')
        print('update -    изменить заметку')
        print('delete -    удалить заметку')
        print('quit -      выйти из программы')
        print(' ')
        command = input('Введите команду: ')
        match command:
            case 'quit':
                break
            case 'read':
                if not exists('notes.csv'):
                    break
                for row in read_file('notes.csv'):
                    print(row)
            case 'read_date':
                if not exists('notes.csv'):
                    break
                for row in read_at_date('notes.csv'):
                    print(row)
            case 'add':
                if not exists('notes.csv'):
                    create_file()
                write_note('notes.csv', get_info())
            case 'delete':
                if not exists('notes.csv'):
                    break
                delete_note('notes.csv')
            case 'update':
                if not exists('notes.csv'):
                    break
                update_note('notes.csv')
            case _:
                print('Неизвестная команда')


main()
