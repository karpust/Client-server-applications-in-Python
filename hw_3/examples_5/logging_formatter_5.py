"""
Логирование с использованием модуля logging
Расширенная настройка: логирование значений переменных
"""

import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app.main
LOG = logging.getLogger('app')

# Создать обработчик
FILE_HANDLER = logging.FileHandler("app_2.log", encoding='utf-8')
# выводит сообщения с уровнем DEBUG
FILE_HANDLER.setLevel(logging.DEBUG)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s")
# %(levelname)-8s - это значит что под levelname отведено 8 символов и незанятые заполнятся пробелами
# для красивого вывода

# подключить объект Formatter к обработчику
FILE_HANDLER.setFormatter(FORMATTER)

# Добавить обработчик к регистратору
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)


if __name__ == '__main__':
    # Передать сообщение обработчику
    PARAMS = {'host': 'www.python.org', 'port': 80}  # словарь
    LOG.debug('Отладочная информация. Параметры подключения: %(host)s, %(port)d', PARAMS)
    LOG.info('Информационное сообщение. Параметры подключения: %(host)s, %(port)d', PARAMS)
    LOG.warning('Предупреждение. Параметры подключения: %(host)s, %(port)d', PARAMS)
    LOG.error(f'Ошибка. Параметры подключения: {PARAMS["host"]},  {PARAMS["port"]}')
    LOG.critical(f'Критическое общение. Параметры подключения: {PARAMS["host"]},  {PARAMS["port"]}')
