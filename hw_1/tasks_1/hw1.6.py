"""
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку
файла по умолчанию. Принудительно открыть файл в формате Unicode и
вывести его содержимое.
"""

import locale
import chardet

file_name = 'test_file.txt'
string_list = ['сетевое программирование', 'сокет', 'декоратор']

with open(file_name, 'w') as test:
    test.writelines('\n'.join(string_list))
    code_by_default = locale.getpreferredencoding()
# with open('test_file.txt') as test:
#     print(test.read())
with open(file_name, 'rb') as test_bin:
    test_bin = test_bin.read()            # open('test_file.txt', 'rb').read()
    code_test = chardet.detect(test_bin)['encoding']
    test_content = test_bin.decode(code_test).encode('utf-8').decode('utf-8')
    print(test_content)

