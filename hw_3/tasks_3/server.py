"""
Функции сервера:
    принимает сообщение клиента; формирует ответ клиенту;
    отправляет ответ клиенту; имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
#  server.py -p 8888 -a 127.0.0.1
import sys
from socket import *
from common.variables import *
from common.utils import *


sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', 7777))
sock.listen(1)
while True:
    client, addr = sock.accept()
    data =


def fill_cmd_params():
    if '-p' in sys.argv:
        listen_port = sys.argv[]


