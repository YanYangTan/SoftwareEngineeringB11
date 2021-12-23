import unittest
from utils import check_len45, check_len100

class MyTestCase(unittest.TestCase):
    def test_len45_1(self):
        self.assertEqual(check_len45(None), False)


    def test_len45_2(self):
        self.assertEqual(check_len45(""), False)


    def test_len45_3(self):
        self.assertEqual(check_len45("a"), True)


    def test_len45_4(self):
        self.assertEqual(check_len45("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), True)

    def test_len45_5(self):
        self.assertEqual(check_len45("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), False)


    def test_len100_1(self):
        self.assertEqual(check_len100(None), False)


    def test_len100_2(self):
        self.assertEqual(check_len100(""), False)


    def test_len100_3(self):
        self.assertEqual(check_len100("a"), True)


    def test_len100_4(self):
        s = ""
        for i in range(100):
            s += "a"
        self.assertEqual(check_len100(s), True)


    def test_len100_5(self):
        s = ""
        for i in range(101):
            s += "a"
        self.assertEqual(check_len100(s), False)