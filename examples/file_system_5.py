"""Модуль file_system"""

# получаем кодировку для файла, с которым работаем
F_N = open('test.txt', 'w', encoding='utf-8')
F_N.write('тест тест тест')
F_N.close()
print(type(F_N))

# явное указание кодировки при работе с файлом
with open('test.txt', encoding='utf-8') as f_n:
    for el_str in f_n:
        print(el_str, end='')
    print()


# # определение кодировки по умолчанию
import locale
default_encoding = locale.getpreferredencoding()
print(default_encoding)
