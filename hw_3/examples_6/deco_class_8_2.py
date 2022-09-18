"""Простейший декоратор-класс"""
import functools


class Log:
    """Класс-декоратор"""
    def __init__(self, func):  # не удобно  т к если декоратор с параметрами, их нужно передать сюда, а тут уже ф-ция см 9
        functools.update_wrapper(self, func)  # для сохранения имени ф-ции а не обертки
        self.func = func

    def __call__(self, *args, **kwargs):
        """Обертка"""
        res = self.func(*args, **kwargs)
        print(f'log: {self.func.__name__}({args}, {kwargs}) = {res}')
        return res


@Log
def my_func(val_1, val_2):
    """Вычисление"""
    return val_1 ** val_2


print('-- Функции с декораторами --')
my_func(4, 5)

# другой подход применения декоратора к функции func3 = Log(my_func)
func3 = Log(my_func)
func3(4, 5)
