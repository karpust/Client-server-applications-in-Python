import unittest


def split(line, types=None, delimiter=None):
    """ Разбивает текстовую строку и при необходимости
        выполняет преобразование типов.
        Например:
        >>> split('GOOG 100 490.50')
        ['GOOG', '100', '490.50']
        >>> split('GOOG 100 490.50', [str, int, float])
        ['GOOG', 100, 490.5]
        >>>
        По умолчанию разбиение производится по пробельным символам,
        но имеется возможность указать другой символ-разделитель, в виде именованного аргумента:

        >>> split('GOOG,100,490.50', delimiter=',')
        ['GOOG', '100', '490.50']
        >>>
    """
    fields = line.split(delimiter)
    if types:
        fields = [ty(val) for ty, val in zip(types, fields)]
    return fields


# Модульные тесты
# (удобно выносить тесты в отдельный модуль, в примерах этого не делается для упрощения)
class TestSplitFunction(unittest.TestCase):
    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        pass

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def testsimplestring(self):
        r = split('GOOG 100 490.50')
        self.assertEqual(r, ['GOOG', '100', '490.50'])

    def testtypeconvert(self):
        r = split('GOOG 100 490.50', [str, int, float])
        self.assertEqual(r, ['GOOG', 100, 490.5])

    def testdelimiter(self):
        r = split('GOOG,100,490.50', delimiter=',')
        self.assertEqual(r, ['GOOG', '100', '490.50'])


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
