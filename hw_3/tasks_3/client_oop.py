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
from ipaddress import ip_address


def take_client_cmd_params():
    # sys.argv = ['client.py', '127.0.0.1', 8888]
    try:
        server_address = sys.argv[1]
        try:
            ip_address(server_address)
        except ValueError:
            print('Некорректный ip-адрес, попробуйте снова')
            sys.exit()
    except IndexError:
        server_address = CLIENT_ADDRESS_DEFAULT

    try:
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            print('Вы ввели неверный номер порта, попробуйте снова')
            sys.exit()
    except IndexError:
        server_port = PORT_DEFAULT
    return server_address, server_port


def create_presence_msg(name_account='Guest'):
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









# if __name__ == '__main__':
#     main()