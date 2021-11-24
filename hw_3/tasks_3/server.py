"""
Функции сервера:
    принимает сообщение клиента; формирует ответ клиенту;
    отправляет ответ клиенту; имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

from socket import *
from common.variables import *
from common.utils import recieve_msg, send_msg
import sys


def take_server_cmd_params():
    #  sys.argv = ['server.py', '-p', 8888, '-a', '127.0.0.1']
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        if listen_port < 1024 or listen_port > 65535:
            print('Вы ввели неверный номер порта')
    else:
        listen_port = PORT_DEFAULT

    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
        # а как проверить корректен ли порт?
    else:
        listen_address = SERVER_ADDRESS_DEFAULT
    return listen_address, listen_port


def check_client_msg(client_msg):
    if ACTION and TIME and USER in client_msg \
            and client_msg[ACTION] == PRESENCE:
        return {RESPONSE: 200}
    return {ERROR: 'Bad request'}


# transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# transport.bind(fill_cmd_params())
# transport.listen(1)
# че за транспорт?
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
        # DATA = CLIENT_SOCK.recv(4096)
        # print(f"Сообщение: {DATA.decode('utf-8')} было отправлено клиентом: {ADDR})")
        # MSG = 'привет, клиент!'
        # CLIENT_SOCK.send(MSG.encode('utf-8'))
        CLIENT_SOCK.close()
finally:
    SERV_SOCK.close()




