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
    register()
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
        else:
            response_object["message"] = "Incorrect username/password!"
    return jsonify(response_object)


def register():
    username = "Kun"
    password = encrypt_password("0602")
    email = "kun@gmail.com"
    phone = "12345678901"
    birthday = datetime.date(1999, 6, 2)
    user1 = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(email=email).first()
    if user1 and not user2:
        print("Username occupied!")
    elif user2 and not user1:
        print("Email occupied!")
    elif not user1 and not user2:
        rand_number = 0
        while True:
            rand_number = random.randint(1, 100000)
            res = User.query.filter_by(idusers=rand_number).first()
            if not res:
                break
        new_user = User(idusers=rand_number, username=username, password=password, email=email, phone=phone, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        print("Registered!")
