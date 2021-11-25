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
from ipaddress import ip_address
from common.utils_oop import Sock


class ServSock(Sock):
    def __init__(self, family, connect_type):
        super().__init__()
        self.family = family
        self.type = connect_type

    def take_server_cmd_params(self):
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

    def check_client_msg(self, client_msg):
        if ACTION and TIME and USER in client_msg \
                and client_msg[ACTION] == PRESENCE \
                and client_msg[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {ERROR: 'Bad request'}


class Connector:
    def __init__(self, connect_1, connect_2):
        self.connect_1 = connect_1
        self.connect_2 = connect_2

    def server_connect(self):  # сервер, клиент
        try:
            while True:
                self.connect_2, ADDR = self.connect_1.accept()
                from_client_msg = recieve_msg(self.connect_2)
                print('Получено от клиента: ', from_client_msg)
                from_server_msg = self.connect_1.check_client_msg(from_client_msg)
                print('Отправлено клиенту: ', from_server_msg)
                send_msg(self.connect_2, from_server_msg)
                self.connect_2.close()
        finally:
            self.connect_2.close()

    def client_connect(self):
        self.connect_1.connect(self.connect_1.take_client_cmd_params)
        client_msg = self.connect_1.create_presence_msg
        print('Отправлено серверу: ', client_msg)
        send_msg(self.connect_1, client_msg)
        server_msg = recieve_msg(self.connect_1)
        print('Получено от сервера: ', server_msg)
        from_server_msg = self.connect_1.check_server_msg(server_msg)
        print('Сообщение от сервера: ', from_server_msg)
        self.connect_1.close()


server = ServSock(AF_INET, SOCK_STREAM)
server.bind(server.take_server_cmd_params)
server.listen(MAX_CONNECTION)
server_up = Connector(server, client)
server_up.server_connect


