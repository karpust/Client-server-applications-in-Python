"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import argparse
import json
import sys
import time
from common.variables import ACTION, PRESENCE, TIME, TYPE, STATUS, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, CLIENT_ADDRESS_DEFAULT, PORT_DEFAULT
from ipaddress import ip_address
from common.utils import Sock
import logging
import logs.client_log_config
from errors import *
from decos import log

CLIENT_LOGGER = logging.getLogger('client')


class ClientSock(Sock):
    def __init__(self, family=-1, type=-1):
        super().__init__(family, type)
        self.server_address = None
        self.server_port = None

    @staticmethod
    @log
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
    @log
    def check_server_msg(server_msg):
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера {server_msg}')
        if RESPONSE in server_msg:
            if server_msg[RESPONSE] == 200:
                return '200: OK'
            return '400: ' + server_msg[ERROR]
        raise FieldMissingError(RESPONSE)

    @log
    def client_connect(self):
        self.server_address, self.server_port = cmd_arg_parse()
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

@log
def cmd_arg_parse():  # sys.argv = ['client.py', '127.0.0.1', 8888]
    parser = argparse.ArgumentParser()  # создаем объект парсер
    parser.add_argument('addr', default='127.0.0.1', nargs='?')  # описываем позиционные аргументы
    parser.add_argument('port', default=7777, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    try:
        ip_address(server_address)
    except ValueError:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием ip-адреса {server_address}. '
                               f'Адрес некорректен')
        sys.exit(1)

    if server_port < 1024 or server_port > 65535:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с указанием порта: {server_port}. '
                               f'Адрес порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)
    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: адрес сервера: {server_address}, '
                       f'порт сервера: {server_port}.')
    return server_address, server_port


client = ClientSock()


if __name__ == '__main__':
    client.client_connect()


