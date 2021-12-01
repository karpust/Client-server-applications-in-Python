"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
результаты из байтовового в строковый тип на кириллице."""

import subprocess
import chardet
import platform

web_res = ['yandex.ru', 'youtube.com']


def ping_web(list_of_resources):
    """ф-ция выполняет пинг веб-ресурсов из списка и преобразует
    результаты из байтовового в строковый тип на кириллице
    """
    if platform.system().lower() == "windows":
        system_param = '-n'
    else:
        system_param = '-c'

    for el in list_of_resources:
        args = ['ping', el, system_param, '2']
        res_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in res_ping.stdout:
            # print(line)
            type_of_code = chardet.detect(line)  # -> {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
            new_line = line.decode(type_of_code['encoding']).encode('utf-8')
            # print(chardet.detect(new_line))  # -> {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
            new_line_decode = new_line.decode('utf-8')
            print(new_line_decode)


ping_web(web_res)
