"""
Логирование с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import sys
import logging

# Создать логгер - регистратор верхнего уроовня
# с именем app
APP_LOG = logging.getLogger('app')
# Установить уровень важности
APP_LOG.setLevel(logging.INFO)

# Создать обработчик который выводит сообщения с уровнем CRITICAL в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setLevel(logging.INFO)

# Создать обработчик который выводит сообщения в файл
FILE_HANDLER = logging.FileHandler('app_4.log', encoding='utf-8')
FILE_HANDLER.setLevel(logging.ERROR)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s %(levelname)-8s - %(message)s ")

# подключить объект Formatter к обработчикам
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# Добавить обработчики к регистратору
APP_LOG.addHandler(STREAM_HANDLER)
APP_LOG.addHandler(FILE_HANDLER)
APP_LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Передать сообщение обработчику
    APP_LOG.debug('Отладочная информация')
    APP_LOG.info('Информационное сообщение')
    APP_LOG.warning('Предупреждение')
    APP_LOG.error('Ошибка')
    APP_LOG.critical('Критическое общение')
