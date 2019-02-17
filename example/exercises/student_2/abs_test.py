from unittest import TestCase

# Doens't exists now.. but this file will be copied and executed over every directory in `exercises`.
from my_abs import my_abs


class AbsTest(TestCase):
    def test_abs_positive(self):
        self.assertEqual(7, my_abs(7))

    def test_abs_zero(self):
        self.assertEqual(0, my_abs(0))

    def test_abs_negative(self):
        self.assertEqual(1, my_abs(-1))

