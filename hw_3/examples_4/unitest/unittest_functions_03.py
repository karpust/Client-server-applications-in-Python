"""assertEqual"""

import unittest


def sum_kv_ij(i, j):
    """Сумма квадратов"""
    return i * i + j * j


def val_compare(val_1, val_2):
    """Сравнение значений"""
    return val_1 > val_2


class Plane:
    """class"""
    pass


class Car:
    """class"""
    pass


def is_compare(val_1, val_2):
    return val_1 is val_2


def is_none(val_1):
    val_2 = val_1
    return val_2


class TestSumKV(unittest.TestCase):
    """создаем тестовый случай"""
    def testequal(self):
        """создаем сам тест"""

        # используем функцию assertEqual
        self.assertEqual(sum_kv_ij(2, 3), 13)

    def testnotequal(self):

        """используем функцию assertNotEqual"""
        self.assertNotEqual(sum_kv_ij(2, 3), 10)

    def testtrue(self):

        """используем функцию assertTrue"""
        self.assertTrue(val_compare(10, 3), True)

    def testfalse(self):

        """используем функцию assertTrue"""
        self.assertFalse(val_compare(10, 30), False)

    def testis(self):

        """используем функцию assertIs"""
        self.assertIs(is_compare(Plane(), Plane()), False)

    def testisnot(self):

        """используем функцию assertIsNot"""
        self.assertIsNot(is_compare(Plane(), Plane()), True)

    def testisnone(self):

        """используем функцию assertIsNone"""
        self.assertIsNone(is_none(None), True)

    def testisnotnone(self):

        """используем функцию assertIsNotNone"""
        self.assertIsNotNone(is_none("string"), True)

    def testin(self):

        """используем функцию assertIn"""
        self.assertIn(1, [1, 2, 3])

    def testnotin(self):

        """используем функцию assertNotIn"""
        self.assertNotIn(4, [1, 2, 3])

    def testisinstance(self):

        """используем функцию assertIsInstance"""
        self.assertIsInstance(Plane(), Plane)

    def testnotisinstance(self):

        """используем функцию assertNotIsInstance"""
        self.assertNotIsInstance(Plane(), Car)

    def testraises(self):

        """используем функцию assertRaises"""
        with self.assertRaises(ZeroDivisionError):
            1 // 0


if __name__ == '__main__':
    unittest.main()
