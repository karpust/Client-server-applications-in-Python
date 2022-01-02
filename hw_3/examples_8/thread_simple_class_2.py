"""Отдельный класс-поток"""
# thread_simple_1.0.py на ооп

import time
from threading import Thread


class ClockThread(Thread):
    """Класс-наследник потока"""
    def __init__(self, interval):
        super().__init__()
        # self.daemon = True
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval)
            print(self.interval)
            print(f"Текущее время: {time.ctime()}")


THR = ClockThread(1)
THR.start()

"""
Чтобы проследить работу потока после вызова метода t.start(),
необходимо также добавить вызов метода t.join(). 
Иначе приложение завершится сразу после запуска потока.
"""

THR.join()
