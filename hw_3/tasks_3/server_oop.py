"""
Функции сервера:
    принимает сообщение клиента; формирует ответ клиенту;
    отправляет ответ клиенту; имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

import sys
from ipaddress import ip_address
from common.variables import ACTION, TIME, USER, PRESENCE, ACCOUNT_NAME, RESPONSE, ERROR, \
    MAX_CONNECTION, PORT_DEFAULT, SERVER_ADDRESS_DEFAULT
from common.utils_oop import Sock
from socket import SOL_SOCKET, SO_REUSEADDR


class ServSock(Sock):
    def __init__(self, listen_address, listen_port, family=-1, type=-1):
        super().__init__(family, type)
        self.listen_address = listen_address
        self.listen_port = listen_port

    @staticmethod
    def check_presence_msg(client_msg):
        if ACTION in client_msg and TIME in client_msg \
                and USER in client_msg and client_msg[ACTION] == PRESENCE \
                and client_msg[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {RESPONSE: 400, ERROR: 'Bad request'}

    def server_connect(self):  # сервер, клиент
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind((self.listen_address, self.listen_port))
        self.listen(MAX_CONNECTION)
        print('Сервер в ожидании клиента')
        while True:
            client, addr = self.accept()
            print('Сервер соединен с клиентом')
            from_client_msg = super().recieve_msg(client)
            print('Получено от клиента: ', from_client_msg)
            from_server_msg = self.check_presence_msg(from_client_msg)
            print('Отправлено клиенту: ', from_server_msg)
            super().send_msg(client, from_server_msg)
            client.close()


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


server = ServSock(*take_server_cmd_params())


if __name__ == '__main__':
    server.server_connect()





