from flask import Blueprint, jsonify, request
from . import db
from .models import *
import datetime, random
from .utils import *

auth = Blueprint('auth', __name__)


@auth.route('/success', methods=['GET'])
def login_success():
    return jsonify('Success!')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # register()
    response_object = {"status": False}
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        pw = encrypt_password(str(password))
        user = User.query.filter_by(username=username, password=pw).first()
        # if user exists
        if user:
            response_object["status"] = True
            response_object["message"] = "Login success!"
            response_object["userid"] = user.idusers
        else:
            response_object["message"] = "Incorrect username/password!"
    return jsonify(response_object)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        email = post_data.get('email')
        phone = post_data.get('phone')
        birthday = post_data.get('birthday')

    # 检查是否合法
    content = {}
    content['username'] = username
    content['password'] = password
    content['email'] = email
    content['phone'] = phone
    content['birthday'] = birthday
    response_object = {}
    message, status = checkregister(content)
    response_object["status"] = status
    response_object["message"] = message
    if status is not True:
        return jsonify(response_object)

    # 如果合法判断是否已经存在
    pw = encrypt_password(password)
    user1 = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(email=email).first()
    if user1 and not user2:
        print("Username occupied!")
        response_object["status"] = False
        response_object["message"] = "Username occupied!"
    elif user2 and not user1:
        print("Email occupied!")
        response_object["status"] = False
        response_object["message"] = "Email occupied!"
    elif not user1 and not user2:
        rand_number = 0
        while True:
            rand_number = random.randint(1, 100000)
            res = User.query.filter_by(idusers=rand_number).first()
            if not res:
                break
        new_user = User(idusers=rand_number, username=username, password=pw, email=email, phone=phone, birthday=birthday)
        try:
            db.session.add(new_user)
            db.session.commit()
            print("Registered!")
            response_object["message"] = "Registered!"
            response_object["userid"] = new_user.idusers
        except Exception as e:
            print(e)
            response_object["status"] = False
            response_object["message"] = "Registered failed"
    return jsonify(response_object)


@auth.route('/query-username', methods=['GET', 'POST'])
def query_username():
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False

    user = User.query.filter_by(idusers=user_id).first()
    if not user:
        response_object['message'] = "Error: User does not exist!"
    else:
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['username'] = query_username_by_id(user_id)
    return jsonify(response_object)
