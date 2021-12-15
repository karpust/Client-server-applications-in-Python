"""
Функции сервера:
    принимает сообщение клиента; формирует ответ клиенту;
    отправляет ответ клиенту; имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
import argparse
import sys
import time
from ipaddress import ip_address
from select import select
from common.variables import ACTION, TIME, USER, PRESENCE, ACCOUNT_NAME, RESPONSE, ERROR, \
    MAX_CONNECTION, PORT_DEFAULT, SERVER_ADDRESS_DEFAULT, MESSAGE, MESSAGE_TEXT, SENDER
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
    def __init__(self, family=-1, type=-1):
        super().__init__(family, type)
        self.listen_address = None
        self.listen_port = None

    @log
    def check_msg(self, message, message_lst, client):
        """
        проверяет сообщение клиента:
        если это сообщение о присутствии - отправить ответ клиенту,
        если это сообщение др клиенту - добавить сообщение в очередь
        """
        # если это сообщение о присутствии и ок, ответим {RESPONSE: 200}
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента {message}.')
        if ACTION in message and TIME in message \
                and USER in message and message[ACTION] == PRESENCE \
                and message[USER][ACCOUNT_NAME] == 'Guest':
            super().send_msg(client, {RESPONSE: 200})
            return
        # если это обычное сообщение, добавим его в очередь
        elif ACTION in message and TIME in message \
                and MESSAGE_TEXT in message and message[ACTION] == MESSAGE:
            message_lst.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        # если некорректное то вернем ERROR: 'Bad request'
        else:
            super().send_msg(client, {RESPONSE: 400, ERROR: 'Bad request'})
            return

    @log
    def server_connect(self):  # сервер, клиент
        self.listen_address, self.listen_port = cmd_arg_parse()
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind((self.listen_address, self.listen_port))
        self.listen(MAX_CONNECTION)
        SERVER_LOGGER.debug('Сервер в ожидании клиента')
        # список клиентов и очередь сообщений:
        clients = []
        messages = []
        while True:  # ждем подключения клиента, если подключится - добавим в список клиентов
            try:
                client, client_addr = self.accept()
            except OSError:  # если таймаут вышел, ловим исключение
                pass
            else:
                clients.append(client)
                SERVER_LOGGER.debug(f'Сервер соединен с клиентом {client_addr}')
            recv_data_lst = []  # список клиентов которые получают на чтение
            send_data_lst = []  # список клиентов которые отправляют
            err_lst = []  # список клиентов на возврат ошибки

            # проверяем есть ли ожидающие клиенты:
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select(clients, clients, [], 0)
                    # на чтение, на отправку, на возврат ошибки
            except OSError:
                pass

            # проверяем есть ли получающие клиенты,
            # если есть, то добавим словарь-сообщение в очередь,
            # если нет сообщения - отключим клиента:
            if recv_data_lst:
                for client_with_msg in recv_data_lst:
                    try:
                        self.check_msg(super().recieve_msg(client_with_msg), messages, client_with_msg)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_with_msg.getpeername()} '
                                           f'отключен от сервера.')
                        clients.remove(client_with_msg)

            # если есть сообщения для отправки, и отправляющие клиенты,
            # сформируем сообщение:
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]  # удалим сообщение из очереди
                for waiting_msg_client in send_data_lst:
                    try:
                        super().send_msg(waiting_msg_client, message)  # отправим сообщение
                    except:
                        SERVER_LOGGER.info(f'Клиент {waiting_msg_client.getpeername()} отключился от сервера.')
                        waiting_msg_client.close()
                        clients.remove(waiting_msg_client)


@log
def cmd_arg_parse():
    parser = argparse.ArgumentParser()  # создаем объект парсер
    # описываем аргументы которые парсер будет считывать из cmd:
    parser.add_argument('-p', default=7777, type=int, nargs='?')  # описываем именные аргументы
    parser.add_argument('-a', default='', nargs='?')
    # nargs='?' значит: если присутствует один аргумент – он будет сохранён,
    # иначе – будет использовано значение из ключа default
    namespace = parser.parse_args(sys.argv[1:])  # все кроме имени скрипта
    listen_address = namespace.a
    listen_port = namespace.p
    if listen_port < 1024 or listen_port > 65535:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием порта {listen_port}. '
                               f'Адрес порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)
    if listen_address != '':
        try:
            ip_address(listen_address)
        except ValueError:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием ip-адреса {listen_address}. '
                                   f'Адрес некорректен')
            sys.exit(1)
    SERVER_LOGGER.info(f'Сервер запущен: ip-адрес для подключений: {listen_address}, '
                       f'номер порта для подключений: {listen_port}')
    return listen_address, listen_port


server = ServSock()
server.settimeout(10)  # будет ждать подключений указанное время


if __name__ == '__main__':
    server.server_connect()





