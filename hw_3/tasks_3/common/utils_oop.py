import json
from socket import socket
from .variables import ENCODING, MAX_PACKAGE_LENGTH


class Sock(socket):
    def __init__(self, family, type):
        # конструктор класса, family и type заданы в родителе по умолчанию, их не передаем, но передадим
        super().__init__(family, type)  # чтобы обратиться к параметрам родителя и изменить их если нужно

    @staticmethod
    def send_msg(socket_to, msg_dict):
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

    @staticmethod
    def recieve_msg(socket_from):
        """
        проверяет если байты пришли
        декодируем
        в json.loads
        """

        msg_bytes = socket_from.recv(MAX_PACKAGE_LENGTH)  # получили в байтах
        msg_decode = msg_bytes.decode(ENCODING)  # декодировали
        msg_json_dict = json.loads(msg_decode)  # в jsonObj(dict)
        return msg_json_dict


