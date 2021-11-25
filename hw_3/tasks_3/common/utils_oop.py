import json
from common.variables import *
import socket


class Sock(socket):
    def __init__(self):
        super().__init__()

    def send_msg(self, socket_to, msg_dict):
        """
        принимает словарь в джейсоне
        декодирует в байты
        отправляет данные
        """
        if isinstance(msg_dict, dict):
            msg_json_str = json.dumps(msg_dict)  # dict json -> str json
            msg_bytes = msg_json_str.encode(ENCODING)  # сообщение в байты
            socket_to.send(msg_bytes)  # сокет сервера|клиента
        else:
            print('Message type is not dict')

    def recieve_msg(self, socket_from):
        """
        проверяет если байты пришли
        декодируем
        в json.loads
        """

        msg_bytes = socket_from.recv(MAX_PACKAGE_LENGTH)  # получили в байтах
        msg_decode = msg_bytes.decode(ENCODING)  # декодировали
        msg_json_dict = json.loads(msg_decode)  # в jsonObj(dict)
        return msg_json_dict


