"""
socket — создать сокет
send — передать данные
recv — получить данные
close — закрыть соединение
"""

import json
from common.variables import *


def send_msg(socket_to, msg_dict):
    """
    принимает словарь в джейсоне
    декодирует в байты
    отправляет данные
    """
    msg_json_str = json.dumps(msg_dict)  # сообщение -> строкa в json
    msg_bytes = msg_json_str.encode(ENCODING)  # сообщение в байты
    socket_to.send(msg_bytes)  # сокет сервера|клиента


def recieve_msg(socket):
    """
    проверяет если байты пришли
    декодируем
    в json.loads
    """
    msg_bytes = socket.recv(MAX_PACKAGE_LENGTH)  # получили в байтах
    msg_decode = msg_bytes.decode(ENCODING)  # декодировали
    msg_json_dict = json.loads(msg_decode)  # в jsonObj(dict)
    return msg_json_dict


