

# class Log:
#     def __init__(self, address, port):  # передаем все из инита декорируемого класса
#         pass
#
#     def __call__(self, *args, **kwargs):
#         def make_log(func):
#             pass
#             # проверяем какому классу принадлежит декорируемый метод: getOwner(func)
#             # если функция класса сервер ServSock
#             # вызываем логгер сервера
#             # если функция класса клиент ClientSock
#             # вызываем логгер клиента
import inspect
import logging
import sys
import traceback
import logs.server_log_config
import logs.client_log_config
from functools import wraps


def log(func):
    """это декоратор"""
    # @wraps(func)  # возвращает имя функции и ее докстринг
    def wrapper(*args, **kwargs):
        """это обертка"""
        # определим к какому модулю относится декорируемая ф-я
        # чтобы понять какой регистратор использовать
        if sys.argv[0].find('server.py') == -1:  # если строка не найдена find вернет -1
            LOGGER = logging.getLogger('client')
        else:
            LOGGER = logging.getLogger('server')

        f = func(*args, **kwargs)
        LOGGER.debug(f'Вызов функции {func.__name__} из модуля {func.__module__}.\n'
                     f'Эта функция вызвана с параметрами {args}, {kwargs}.\n'
                     f'Функция {func.__name__} вызывается из функции '
                     f'{traceback.format_stack()[0].split()[-1]}\n'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return f
    return wrapper



