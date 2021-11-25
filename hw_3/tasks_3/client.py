"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""

from common.utils import *
import sys
import time
from socket import *
from common.variables import *


def take_client_cmd_params():
    # sys.argv = ['client.py', '127.0.0.1', 8888]
    try:
        server_address = sys.argv[1]
    except IndexError:
        server_address = CLIENT_ADDRESS_DEFAULT
    try:
        server_port = int(sys.argv[2])
    except IndexError:
        server_port = PORT_DEFAULT

    if server_port < 1024 or server_port > 65535:
        print('Вы ввели неверный номер порта')
    else:
        server_port = PORT_DEFAULT
    return server_address, server_port


def create_presence_msg(name_account='guest'):
    return {
        ACTION: PRESENCE,
        TIME: time.time(),
        TYPE: STATUS,
        USER: {
            ACCOUNT_NAME: name_account,
            STATUS: "I'm online"
        }
    }


def check_server_msg(server_msg):
    if RESPONSE in server_msg and server_msg[RESPONSE] == 200:
        return '200: OK'
    return '400:' + server_msg[ERROR]


CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(take_client_cmd_params())
client_msg = create_presence_msg()
print('Отправлено серверу: ', client_msg)
send_msg(CLIENT_SOCK, client_msg)
server_msg = recieve_msg(CLIENT_SOCK)
print('Получено от сервера: ', server_msg)
from_server_msg = check_server_msg(server_msg)
print('Сообщение от сервера: ', from_server_msg)
CLIENT_SOCK.close()








# if __name__ == '__main__':
#     main()