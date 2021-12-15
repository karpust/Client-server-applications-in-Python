"""
Сравнение производительности потоков при вычислениях
Объём вычислений делится на 2 потока
"""

import time
from threading import Thread


def create_list(min_index, max_index):
    """Функция, которая может быть запущена в потоке"""

    amount = 0
    for x in range(min_index, max_index):
        amount += (x * x) ** x

THR1 = Thread(target=create_list, args=(0, 5000))
THR2 = Thread(target=create_list, args=(5000, 10000))
THR1.daemon = True
THR2.daemon = True


print(f"Время запуска основной программы: {time.ctime()}")
time1 = time.time()

THR1.start()
THR2.start()
THR1.join()
THR2.join()
time2 = time.time()
print(f'first part = {time2 - time1:.2f}')

# на выполнение с потоками требуется не меньше времени чем без них
# а вот мультипроцессинг экономит время

# потоки время экономят с сокетами и бд


