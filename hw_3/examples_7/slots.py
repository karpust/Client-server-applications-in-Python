"""Обычный класс и класс со слотами"""

from pympler import asizeof
from timeit import timeit
"""
Динамическое управление атрибутами нам нужно далеко не всегда — 
очень много случаев, когда мы точно знаем, какие атрибуты будут 
у экземпляров класса. Мы можем уменьшить расход ресурсов.
Как раз для таких случаев в пайтоне есть магический атрибут __slots__, 
который позволяет задать ограниченный набор атрибутов, которыми будет 
обладать экземпляр класса.
"""
# слоты описывают класс и позволяют жестко определить кол-во аргументов в этом классе

class BasicClass:
    """
    В обычной ситуации в Python в объекты можно добавлять
    новые атрибуты вне описания класса
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc(self):
        return self.x ** self.y


bc = BasicClass(5, 6)
# аргументы в классе хранятся ввиде отдельного
# словаря кот вызывается __dict__
print(bc.__dict__)
# сколько байт занимает экземпляр класса bc:
print(asizeof.asizeof(bc))
# добавим аргумент, изменится память и словарь
bc.z = 7
print(bc.__dict__)
print(asizeof.asizeof(bc))

print('=' * 80)
"""
The class variable __slots__: 
1.) reduces memory size of instances
2.) prevents automatic creation of __dict__ and 
disallows adding new attributes to instances 
3.) reduces access time to attributes extraction 
for computation from class instances
"""

# помощью слота мы запретим такое добавление аргументов:
class BasicClassSlots:
    # имеет атрибут(дендраметод) __slots__ но не имеет __dict__
    __slots__ = ('x', 'y')  # меньше можно, но не больше

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc(self):
        return self.x ** self.y


bc_slots = BasicClassSlots(5, 6)
print(bc_slots.__slots__)
print(asizeof.asizeof(bc_slots))  # экономия памяти!
# bc_slots.z = 7
# print(bs_slots.__dict__)


print('=' * 80)
"""
3.) reduces access time to attributes of class instances
"""
print(timeit(bc.calc))
print(timeit(bc_slots.calc))  # у слотов времени уходит меньше


print('=' * 80)
"""
4.) We cannot add attributes to an instance of a class, but we can remove them.
"""
del bc_slots.x
try:
    print(bc_slots.x)
except AttributeError as e:
    print(e.__class__, ":  x attribute does not exist!")

""" And then add it again. """
bc_slots.x = 5
print('bc_slots.x = ', bc_slots.x)

print('=' * 80)

"""
5.) In the case of using __slots__, we cannot add an instance attribute of the class, 
    but we can add a class attribute.
"""

BasicClassSlots.CLASS_ATTR = 555  # к классу можем к слоту нет
print(bc_slots.CLASS_ATTR)
