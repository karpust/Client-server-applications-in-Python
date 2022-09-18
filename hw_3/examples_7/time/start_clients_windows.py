"""
Служебный скрипт запуска/останова нескольких клиентских приложений
"""

from subprocess import Popen, CREATE_NEW_CONSOLE


P_LIST = []

while True:
    USER = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if USER == 'q':
        break

    elif USER == 's':
        for _ in range(2):

            P_LIST.append(Popen('python time_client_random.py', creationflags=CREATE_NEW_CONSOLE))
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли

        print(' Запущено 10 клиентов')
    elif USER == 'x':
        for p in P_LIST:
            p.kill()
        P_LIST.clear()
