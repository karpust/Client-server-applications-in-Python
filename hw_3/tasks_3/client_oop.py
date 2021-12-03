"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import json
import sys
import time
from common.variables import ACTION, PRESENCE, TIME, TYPE, STATUS, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, CLIENT_ADDRESS_DEFAULT, PORT_DEFAULT
from ipaddress import ip_address
from common.utils_oop import Sock
import logging
import logs.client_log_config
from errors import *

CLIENT_LOGGER = logging.getLogger('client')


class ClientSock(Sock):
    def __init__(self, server_address, server_port, family=-1, type=-1):
        super().__init__(family, type)
        self.server_address = server_address
        self.server_port = server_port

    @staticmethod
    def create_presence_msg(name_account='Guest'):
        res = {
            ACTION: PRESENCE,
            TIME: time.time(),
            TYPE: STATUS,
            USER: {
                ACCOUNT_NAME: name_account,
                STATUS: "I'm online"
            }
        }
        CLIENT_LOGGER.debug(f'Создано сообщение {res} пользователя {name_account}')
        return res

    @staticmethod
    def check_server_msg(server_msg):
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера {server_msg}')
        if RESPONSE in server_msg:
            if server_msg[RESPONSE] == 200:
                return '200: OK'
            return '400: ' + server_msg[ERROR]
        raise FieldMissingError(RESPONSE)

    def client_connect(self):
        try:
            self.connect((self.server_address, self.server_port))
            client_msg = self.create_presence_msg()
            super().send_msg(self, client_msg)
            server_msg = super().recieve_msg(self)
            CLIENT_LOGGER.info(f'Получено сообщение от сервера: {server_msg}')
            self.check_server_msg(server_msg)
        except FieldMissingError as missing_err:
            CLIENT_LOGGER.critical(f'В ответе сервера отсутствует необходимое поле:'
                                   f'{missing_err.miss_field}')
        except json.JSONDecodeError:
            CLIENT_LOGGER.error(f'Клиенту не удалось декодировать json-строку, полученную от сервера')
        except IncorrectDataRecievedError:
            CLIENT_LOGGER.error(f'Серверу не удалось обработать сообщение от клиента {self}. '
                                f'Соединение разорвано.')
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}. '
                                   f'Конечный узел отверг запрос на подключение')
        except NotDictInputError as dict_err:
            CLIENT_LOGGER.error(f'Полученное клиентом сообщение {dict_err.not_dict} не является словарем')
        CLIENT_LOGGER.info(f'Клиент завершил соединение с сервером')
        self.close()


def take_client_cmd_params():
    # sys.argv = ['client.py', '127.0.0.1', 8888]
    try:
        server_address = sys.argv[1]
        try:
            ip_address(server_address)
        except ValueError:
            CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием ip-адреса {server_address}.'
                                   f'Адрес некорректен')
            sys.exit()
    except IndexError:
        server_address = CLIENT_ADDRESS_DEFAULT

    try:
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием порта: {server_port}'
                                   f'Адрес порта должен быть в диапазоне от 1024 до 65535')
            sys.exit()
    except IndexError:
        server_port = PORT_DEFAULT
    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: адрес сервера: {server_address}, '
                       f'порт сервера: {server_port}.')
    return server_address, server_port


client = ClientSock(*take_client_cmd_params())


if __name__ == '__main__':
    client.client_connect()


