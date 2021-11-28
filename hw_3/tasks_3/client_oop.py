"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""

import sys
import time
from common.variables import ACTION, PRESENCE, TIME, TYPE, STATUS, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, CLIENT_ADDRESS_DEFAULT, PORT_DEFAULT
from ipaddress import ip_address
from common.utils_oop import Sock


class ClientSock(Sock):
    def __init__(self, server_address, server_port, family=-1, type=-1):
        super().__init__(family, type)
        self.server_address = server_address
        self.server_port = server_port

    @property
    def create_presence_msg(self, name_account='Guest'):
        return {
            ACTION: PRESENCE,
            TIME: time.time(),
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: name_account,
                STATUS: "I'm online"
            }
        }

    @staticmethod
    def check_server_msg(server_msg):
        if RESPONSE in server_msg and server_msg[RESPONSE] == 200:
            return '200: OK'
        return '400:' + server_msg[ERROR]

    def client_connect(self):
        self.connect((self.server_address, self.server_port))
        client_msg = self.create_presence_msg
        print('Отправлено серверу: ', client_msg)
        super().send_msg(self, client_msg)
        server_msg = super().recieve_msg(self)
        print('Получено от сервера: ', server_msg)
        from_server_msg = self.check_server_msg(server_msg)
        print('Сообщение от сервера: ', from_server_msg)
        self.close()


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
    client = ClientSock(server_address, server_port)
    client.client_connect()


if __name__ == '__main__':
    take_client_cmd_params()

