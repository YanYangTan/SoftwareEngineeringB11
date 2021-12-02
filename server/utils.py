import scrypt, base64, configparser
import re
import datetime
from .models import *


def encrypt_password(pw):
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    db_dict = dict(config.items('DATABASE'))
    salt = db_dict["salt"]
    key = scrypt.hash(pw, salt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")


def checkregister(content):
    # username
    if len(content['username'])<6 or len(content['username'])>10:
        return "username", False
    # 密码
    if re.match("^(?![0-9]+$)(?![A-Z]+$)(?![a-z]+$)(?![a-zA-Z]+$)(?![0-9A-Z]+$)(?![0-9a-z]+$)[0-9A-Za-z]{6,18}$",content['password'])==None:
        return "password", False
    # 电话
    if re.match("[0-9]{11}$", content['phone']) == None:
        return "phone", False
    # email
    if re.match(
            "[a-zA-Z0-9]{1,63}@(([a-zA-Z0-9]+[a-zA-Z0-9-]*[a-zA-Z0-9]+\.)|([a-zA-Z0-9]*\.)|(\.))*(([a-zA-Z]+[a-zA-Z-]*[a-zA-Z]+)|([a-zA-Z]+)|([a-zA-Z0-9]+([a-zA-Z0-9-]*[a-zA-Z-]+[a-zA-Z0-9-]*)+[a-zA-Z0-9]+)|())$",
            content['email']) == None:
        return "email", False

    place = int((content['email']).find('@'))
    if len(content['email']) - place > 63:
        return "email", False

    # 生日日期
    birth=content['birthday']
    birth=birth.replace('-','')
    birth=int(birth)
    nowtime = int(datetime.datetime.now().date().strftime('%Y%m%d'))
    if birth > nowtime:
        return "birthday", False

    return "ok", True


def check_groupname(name):
    flag = True
    if len(name) == 0 or len(name) > 45:
        flag = False
    return flag


def query_username_by_id(user_id):
    user = User.query.filter_by(idusers=user_id).first()
    return user.username