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
from common.utils import Sock
from socket import SOL_SOCKET, SO_REUSEADDR
import logging
import logs.server_log_config
import json
from errors import *
from decos import log


# cсылка на созданный логгер:
SERVER_LOGGER = logging.getLogger('server')

class ServSock(Sock):
    def __init__(self, listen_address, listen_port, family=-1, type=-1):
        super().__init__(family, type)
        self.listen_address = listen_address
        self.listen_port = listen_port

    @staticmethod
    @log
    def check_presence_msg(client_msg):
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента {client_msg}.')
        if ACTION in client_msg and TIME in client_msg:
            if USER in client_msg and client_msg[ACTION] == PRESENCE \
                    and client_msg[USER][ACCOUNT_NAME] == 'Guest':
                return {RESPONSE: 200}
            return {RESPONSE: 400, ERROR: 'Bad request'}
        raise IncorrectDataRecievedError

    @log
    def server_connect(self):  # сервер, клиент
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind((self.listen_address, self.listen_port))
        self.listen(MAX_CONNECTION)
        SERVER_LOGGER.debug('Сервер в ожидании клиента')
        while True:
            client, client_addr = self.accept()
            SERVER_LOGGER.debug(f'Сервер соединен с клиентом {client_addr}')
            try:
                from_client_msg = super().recieve_msg(client)
                SERVER_LOGGER.debug(f'От клиента {client_addr} получено сообщение: {from_client_msg}')
                from_server_msg = self.check_presence_msg(from_client_msg)
                SERVER_LOGGER.info(f'Клиенту {client_addr} отправлено сообщение: {from_server_msg}')
                super().send_msg(client, from_server_msg)
            except IncorrectDataRecievedError:
                SERVER_LOGGER.error(f'От клиента {client_addr} приняты некорректные данные. '
                                    f'Соединение разорвано.')
            except json.JSONDecodeError:
                SERVER_LOGGER.error(f'Не удалось декодировать json-строку, '
                                    f'полученную от клиента {client_addr}. '
                                    f'Соединение разорвано')
            except NotDictInputError as dict_err:
                SERVER_LOGGER.error(f'Полученное от сервера сообщение {dict_err.not_dict} не является словарем')
            finally:
                SERVER_LOGGER.info(f'Завершено соединение с клиентом {client_addr}.')
                client.close()


@log
def take_server_cmd_params():
    #  sys.argv = ['server.py', '-p', 8888, '-a', '127.0.0.1']
    if '-p' in sys.argv:
        listen_port = sys.argv[sys.argv.index('-p') + 1]
        try:
            listen_port = int(listen_port)
        except ValueError:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием порта {listen_port}. '
                                   f'Введенное значение порта должно быть числом')
            sys.exit()
        listen_port = int(listen_port)
        if listen_port < 1024 or listen_port > 65535:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием порта {listen_port}. '
                                   f'Адрес порта должен быть в диапазоне от 1024 до 65535')
            sys.exit()
    else:
        listen_port = PORT_DEFAULT

    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
        try:
            ip_address(listen_address)
        except ValueError:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием ip-адреса {listen_address}. '
                                   f'Адрес некорректен')
            sys.exit()
    else:
        listen_address = SERVER_ADDRESS_DEFAULT
    SERVER_LOGGER.info(f'Сервер запущен: ip-адрес для подключений: {listen_address}, '
                       f'номер порта для подключений: {listen_port}')
    return listen_address, listen_port


server = ServSock(*take_server_cmd_params())


if __name__ == '__main__':
    server.server_connect()





