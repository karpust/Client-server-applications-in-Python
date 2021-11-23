"""
Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу; получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
    addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import time
from socket import *
from common.variables import *
from common.utils import *

addr = ''
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((addr, 7777))


def presence(name_account):
    content = {
        ACTION: PRESENCE,
        TIME: time.time(),
        TYPE: STATUS,
        USER: {
            ACCOUNT_NAME: name_account,
            STATUS: "I'm online"
        }
    }
    return content


