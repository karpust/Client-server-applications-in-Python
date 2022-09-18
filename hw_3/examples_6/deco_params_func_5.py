"""Простейший декоратор-функция с параметром"""

import time


def sleep(timeout):  # 3  отсюда: @sleep(3)
    """Внешняя функция (формально - декоратор)"""
    def decorator(func):  # чтобы использовать декоратор с параметром,
        # добавим вложение чтобы расширить область видимости
        """Сам декоратор"""
        def decorated(*args, **kwargs):
            """Обертка"""

            time.sleep(timeout)
            res = func(*args, **kwargs)

            print(f'Функция {func.__name__} зависла')
            return res
        return decorated
    return decorator


@sleep(3)
def factorial(param):
    """Вычисляем факториал
    Факториал числа n — это произведение натуральных чисел от 1 до n
    """
    if param <= 1:
        return 1
    else:
        return param * factorial(param - 1)


print(' -- Использован декоратор, реализованный через функцию --')
print('!!! Обратите внимание на то, сколько раз будет вызван декоратор (рекурсия) !!!')
print(factorial(5))
print()
# sleep(3)(factorial)(param) - запуск