"""
Сравнение производительности потоков при вычислениях
Все вычисления происходят ТОЛЬКО в главном потоке
"""

import time
from threading import Thread


def create_list(min_index, max_index):
    """Функция, которая может быть запущена в потоке"""

    amount = 0
    for x in range(min_index, max_index):
        amount += (x * x) ** x


# потоки просто декларируются, но не вызываются
# замеряем время без потоков
THR1 = Thread(target=create_list, args=(0, 5000))
THR2 = Thread(target=create_list, args=(5000, 10000))
THR1.daemon = True
THR2.daemon = True


print(f"Время запуска основной программы: {time.ctime()}")
time1 = time.time()
create_list(0, 5000)
create_list(5000, 10000)
time2 = time.time()
print(f'total = {time2 - time1:.2f}')

