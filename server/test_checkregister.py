import unittest
from datetime import datetime, timedelta
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

    def test_username2(self):
        self.assertEqual(checkregister({
            'username': 'asdasa',
            'password': 'dadDa22311dd',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('ok', True))

    def test_username3(self):
        self.assertEqual(checkregister({
            'username': 'asdasaaaaa',
            'password': 'dadDa22311dd',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('ok', True))

    def test_username4(self):
        self.assertEqual(checkregister({
            'username': 'asdasaaaaaa',
            'password': 'dadDa22311dd',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('username', False))

    def test_pass1(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'AB12a',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_pass2(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'AB12ab',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('ok', True))

    def test_pass3(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'A1234567890123456a',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('ok', True))

    def test_pass4(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'A1234567890123456aa',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_pass5(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'ab12ab',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_pass6(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'AB12AB',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_pass7(self):
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'ABabAb',
            'phone': '13121771068',
            'email':'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('password', False))

    def test_phone1(self):  # 电话不对
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '1312177106',
            'email': 'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('phone', False))

    def test_phone2(self):  # 电话不对
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('ok', True))

    def test_phone3(self):  # 电话不对
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '131217710681',
            'email': 'asdadadada8989@163.com.cc',
            'birthday':'2000-12-19'
        }), ('phone', False))

    def test_phone4(self):  # 电话不对
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '1312177106a',
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

    def test_birthday1(self):
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.ffdf.asd1asd.add',
            'birthday': yesterday
        }), ('ok', True))

    def test_birthday2(self):
        today = (datetime.today().strftime("%Y-%m-%d"))
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.ffdf.asd1asd.add23',
            'birthday': today
        }), ('ok', True))

    def test_birthday3(self):
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(checkregister({
            'username': 'yy_1219',
            'password': 'dadhdAA1212',
            'phone': '13121771068',
            'email': 'asdadadada8989@sssss.ffdf.asd1asd.add',
            'birthday': tomorrow
        }), ('birthday', False))

if __name__ == '__main__':
    unittest.main()