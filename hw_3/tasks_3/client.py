"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import time
from socket import *
from common.variables import *
from common.utils import *
import sys


def take_client_cmd_params():
    # sys.argv = ['client.py', '127.0.0.1', 8888]
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    if server_port < 1024 or server_port > 65535:
        print('Вы ввели неверный номер порта')
    else:
        server_port = PORT_DEFAULT
    return server_port, server_address


def create_presence_msg(name_account='guest'):
    content = {
        ACTION: PRESENCE,
        TIME: time.time(),
        TYPE: STATUS,
        USER: {
            ACCOUNT_NAME: name_account,
            STATUS: "I'm online"
        }
    }
    return content



CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCK.connect(take_client_cmd_params())
# MSG = 'привет, сервер!'
client_msg = create_presence_msg()
CLIENT_SOCK.send(MSG.encode('utf-8'))
# send_msg(transport, msg_to_server)
DATA = CLIENT_SOCK.recv(4096)
print(f"Сообщение от сервера: {DATA.decode('utf-8')} длиной {len(DATA)} байт")
CLIENT_SOCK.close()








# if __name__ == '__main__':
#     main()