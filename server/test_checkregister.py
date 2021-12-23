import unittest
from utils import checkregister


class MyTestCase(unittest.TestCase):
    def test_username1(self):
        self.assertEqual(checkregister({
            'username': 'asdas',
            'password': 'dadDa22311dd',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('username', False))
    def test_pass1(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadha22311dd',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_phone(self):  # 电话不对
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '131217710681',
            'email': 'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('phone', False))

    def test_email1(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
             'email':'asdadadada8989@sssss-',
            'birthday':'2000-12-19'
        }), ('email', False))

    def test_email2(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.111',
            'birthday':'2000-12-19'
        }), ('email', False))

    def test_email3(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.aa111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111',
            'birthday':'2000-12-19'
        }), ('email', False))

    def test_birthday(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.ffdf.asd1asd.add',
            'birthday':'2021-12-31'
        }), ('birthday', False))

    def test_success(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.ffdf.asd1asd.add23',
            'birthday':'2000-12-19'
        }), ('ok', True))

if __name__ == '__main__':
    unittest.main()