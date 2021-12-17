"""
Функции сервера:
    принимает сообщение клиента; формирует ответ клиенту;
    отправляет ответ клиенту; имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

from socket import *
from common.variables import *
from old.utils import recieve_msg, send_msg
import sys
from ipaddress import ip_address


def take_server_cmd_params():
    #  sys.argv = ['server.py', '-p', 8888, '-a', '127.0.0.1']
    if '-p' in sys.argv:
        try:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        except ValueError:
            print('Введенное значение порта должно быть числом, попробуйте снова')
            sys.exit()
        if listen_port < 1024 or listen_port > 65535:
            print('Вы ввели неверный номер порта, попробуйте снова')
            sys.exit()
    else:
        listen_port = PORT_DEFAULT

    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
        try:
            ip_address(listen_address)
        except ValueError:
            print('Некорректный ip-адрес, попробуйте снова')
            sys.exit()
    else:
        listen_address = SERVER_ADDRESS_DEFAULT
    return listen_address, listen_port


def check_client_msg(client_msg):
    if ACTION and TIME and USER in client_msg \
            and client_msg[ACTION] == PRESENCE \
            and client_msg[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {ERROR: 'Bad request'}


SERV_SOCK = socket(AF_INET, SOCK_STREAM)
SERV_SOCK.bind(take_server_cmd_params())
SERV_SOCK.listen(MAX_CONNECTION)


try:
    while True:
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        from_client_msg = recieve_msg(CLIENT_SOCK)
        print('Получено от клиента: ', from_client_msg)
        from_server_msg = check_client_msg(from_client_msg)
        print('Отправлено клиенту: ', from_server_msg)
        send_msg(CLIENT_SOCK, from_server_msg)
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()




