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
    ACCOUNT_NAME, RESPONSE, ERROR, CLIENT_ADDRESS_DEFAULT, PORT_DEFAULT, MESSAGE, MESSAGE_TEXT, SENDER
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
        self.client_mode = None

    @staticmethod
    @log
    def check_messages_by_server(message):
        """
        Обрабатывает сообщения других
        пользователей, которые приходят с сервера
        """
        if ACTION in message and message[ACTION] and \
                SENDER in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                  f'{message[MESSAGE_TEXT]}')
            CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                               f'{message[MESSAGE_TEXT]}')
        else:
            CLIENT_LOGGER.error(f'От сервера получено некорректное сообщение {message}:')

    @log
    def create_message_msg(self, name_account='Guest'):
        """
        Создает сообщение(словарь) для
        отправки другому пользователю
        """
        msg = input('Введите текст сообщения, или "!!!" для завершения работы')
        if msg == '!!!':
            CLIENT_LOGGER.info(f'Пользователь завершил работу')
            self.close()
            sys.exit(0)
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: name_account,
            MESSAGE_TEXT: msg
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения {message}')
        return message

    @staticmethod
    @log
    def create_presence_msg(name_account='Guest'):
        """
        Создает сообщение-присутствие(словарь),
        подтверждающее, что пользоватьель онлайн.
        """
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
        self.server_address, self.server_port, self.client_mode = cmd_arg_parse()
        CLIENT_LOGGER.info(f'Запущен клиент с параметрами: адрес сервера: {self.server_address}, '
                           f'порт {self.server_port}, режим работы: {self.client_mode}.')
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
            sys.exit(1)
        except json.JSONDecodeError:
            CLIENT_LOGGER.error(f'Клиенту не удалось декодировать json-строку, полученную от сервера')
            sys.exit(1)
        except IncorrectDataRecievedError:
            CLIENT_LOGGER.error(f'Серверу не удалось обработать сообщение от клиента {self}. '
                                f'Соединение разорвано.')
            sys.exit(1)
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}. '
                                   f'Конечный узел отверг запрос на подключение')
            sys.exit(1)
        except NotDictInputError as dict_err:
            CLIENT_LOGGER.error(f'Полученное клиентом сообщение {dict_err.not_dict} не является словарем. ')
            sys.exit(1)
        if self.client_mode == 'send':
            print('Режим работы этого клиента - отправка сообщений. ')
        else:
            print('Режим работы этого клиента - прием сообщений. ')
        # если режим работы - отправка сообщений:
        while True:
            if self.client_mode == 'send':
                try:
                    super().send_msg(self, self.create_message_msg())
                except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно. ')
                    sys.exit(1)
            if self.client_mode == 'listen':
                try:
                    self.check_messages_by_server(super().recieve_msg(self))
                except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно. ')
                    sys.exit(1)


@log
def cmd_arg_parse():  # sys.argv = ['client.py', '127.0.0.1', 8888]
    parser = argparse.ArgumentParser()  # создаем объект парсер
    parser.add_argument('addr', default='127.0.0.1', nargs='?')  # описываем позиционные аргументы
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Выбранный режим {client_mode} - не допустим. Можно использовать listen или send.')
        sys.exit(1)
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
    return server_address, server_port, client_mode


client = ClientSock()


if __name__ == '__main__':
    client.client_connect()


