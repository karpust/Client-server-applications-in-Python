"""
Логирование с использованием модуля logging
Расширенная настройка. Форматирование, обработчики
"""

import logging

# Создать логгер - регистратор верхнего уровня
# с именем app.main
LOG = logging.getLogger('app.main')

# Создать обработчик
FILE_HANDLER = logging.FileHandler("app.log", encoding="utf-8")
# выводит сообщения с уровнем DEBUG
FILE_HANDLER.setLevel(logging.DEBUG)

# Создать объект Formatter
# Определить формат сообщений
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s ")

# подключить объект Formatter к обработчику
FILE_HANDLER.setFormatter(FORMATTER)

# Добавить обработчик к регистратору
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Передать сообщение обработчику
    LOG.debug('Отладочная информация')
    LOG.info('Информационное сообщение')
    LOG.warning('Предупреждение')
    LOG.error('Ошибка')
    LOG.critical('Критическое общение')
