from flask import Blueprint, jsonify, request
from . import db
from .models import *
import datetime, random
from sqlalchemy import or_

auth = Blueprint('auth', __name__)


@auth.route('/success', methods=['GET'])
def login_success():
    return jsonify('Success!')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    response_object = {"status": False}
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        user = User.query.filter_by(username=username).first()
        # if user exists
        if user:
            response_object["status"] = True
            response_object["message"] = "Login success!"
        else:
            response_object["message"] = "Incorrect username/password!"
    return jsonify(response_object)


def register():
    username = "Jack"
    password = "0602"
    email = "jack@gmail.com"
    phone = "12345678901"
    birthday = datetime.date(1998, 7, 31)
    user1 = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(email=email).first()
    if user1 or user2:
        print("Username or email occupied!")
    else:
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
