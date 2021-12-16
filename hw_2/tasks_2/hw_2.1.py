"""Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV. Для этого:

    Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
    с данными, их открытие и считывание данных. В этой функции из считанных
    данных необходимо с помощью регулярных выражений извлечь значения
    параметров «Изготовитель системы», «Название ОС», «Код продукта»,
    «Тип системы». Значения каждого параметра поместить в соответствующий
    список. Должно получиться четыре списка — например, os_prod_list,
    os_name_list, os_code_list, os_type_list. В этой же функции создать
    главный список для хранения данных отчета — например, main_data — и
    поместить в него названия столбцов отчета в виде списка: «Изготовитель
    системы», «Название ОС», «Код продукта», «Тип системы». Значения для
    этих столбцов также оформить в виде списка и поместить в файл main_data
    (также для каждого файла);
    Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
    В этой функции реализовать получение данных через вызов функции get_data(),
    а также сохранение подготовленных данных в соответствующий CSV-файл;
    Проверить работу программы через вызов функции write_to_csv().
"""


import chardet
import re
import csv

parameters = [
    'Изготовитель ОС',
    'Название ОС',
    'Код продукта',
    'Тип системы'
]

files = [
    'info_1.txt',
    'info_2.txt',
    'info_3.txt',
]


def get_data(list_of_files, params):
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    for file in list_of_files:
        with open(file, 'rb') as f:
            f = f.read()
            file_format = chardet.detect(f)['encoding']  # узнали кодировку

        with open(file, encoding=file_format) as fil:
            for line in fil:
                for param in params:
                    if re.match(r'\A' + param, line):  # есть ли в строке заданный параметр
                        position = re.search(r'\A' + param, line).span()[1] + 1  # берем значения для параметров
                        line = re.sub(r'\s{2}|\n', "", line[position:])  # убираем пробельные символы
                        if param == params[0]:
                            os_prod_list.append(line)
                        elif param == params[1]:
                            os_name_list.append(line)
                        elif param == params[2]:
                            os_code_list.append(line)
                        elif param == params[3]:
                            os_type_list.append(line)
    eval_list = [os_prod_list, os_name_list, os_code_list, os_type_list]
    # транспонируем матрицу:
    main_data = [[eval_list[el][i] for el in range(len(eval_list))] for i in range(len(eval_list[0]))]
    main_data.insert(0, params)  # добавили заголовки
    return main_data


def write_to_csv(csv_file):
    """
    ф -ция сохраняет данные в csv файле
    """
    data_list = get_data(files, parameters)
    with open(csv_file, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter='|')
        file_writer.writerows(data_list)


write_to_csv('1.csv')

