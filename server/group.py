from flask import Blueprint, jsonify, request
from . import db
from .models import *
import random

group = Blueprint('group', __name__)


@group.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == "POST":
        post_data = request.get_json()
        group_name = post_data.get('group_name')
    response_object = {}
    rand_number = 0
    while True:
        rand_number = random.randint(1, 100000)
        res = Group.query.filter_by(idgroups=rand_number).first()
        if not res:
            break
    group = Group()
    group.idgroups = rand_number
    group.name = group_name
    tmp = random.randint(10000, 1000000)
    group.invite_key = tmp
    try:
        db.session.add(group)
        db.session.commit()
        response_object["status"] = True
        response_object["message"] = "Group created!"
        response_object["group_id"] = rand_number
        response_object["invite_key"] = tmp
    except Exception as e:
        print(e)
        response_object["status"] = False
        response_object["message"] = "Failed to create group"
    return jsonify(response_object)


@group.route('/generate-key', methods=['GET', 'POST'])
def generate_key():
    if request.method == "POST":
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    group = Group.query.filter_by(idgroups=group_id).first()
    response_object = {}
    response_object["status"] = False
    if group:
        tmp = random.randint(10000, 1000000)
        group.invite_key = tmp
        try:
            db.session.commit()
            response_object["status"] = True
            response_object["message"] = "Invite key generated!"
            response_object["invite_key"] = tmp
        except Exception as e:
            print(e)
            response_object["message"] = "Failed to generate invite key!"
    else:
        response_object["message"] = "Error: Group does not exist"
    return jsonify(response_object)


@group.route('/join-group', methods=['GET', 'POST'])
def join_group():
    if request.get_method == "POST":
        post_data = request.get_json()
        user_id = post_data.get('user_id')
        group_id = post_data.get('group_id')
        invite_key = str(post_data.get('invite_key'))
    response_object = {}
    response_object["status"] = False
    user = User.query.filter_by(idusers=user_id).first()
    group = Group.query.filter_by(idgroups=group_id).first()
    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if rel:
        response_object["message"] = "Error: User already in group"
    elif not user:
        response_object["message"] = "Error: User does not exist"
    elif not group:
        response_object["message"] = "Error: Group does not exist"
    else:
        if group.invite_key != invite_key:
            response_object["message"] = "Error: Invalid invite key!"
        else:
            rel_group = RelationGroupUser()
            rand_number = 0
            while True:
                rand_number = random.randint(1, 100000)
                res = RelationGroupUser.query.filter_by(id=rand_number).first()
                if not res:
                    break
            rel_group.id = rand_number
            rel_group.group_id = group_id
            rel_group.user_id = user_id
            try:
                db.session.add(rel_group)
                db.session.commit()
                response_object["status"] = True
                response_object["message"] = "User added to group!"
            except Exception as e:
                print(e)
                response_object["message"] = "Failed to join group"
    return jsonify(response_object)


@group.route('/query-group', methods=['GET', 'POST'])
def query_group():
    if request.get_method == "POST":
        post_data = request.get_json()
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False
    user = User.query.filter_by(idusers=user_id).first()
    if user:
        groups = user.relation_group_user
        ret = []
        for group in groups:
            item = {}
            id_tmp = group.group_id
            item['id'] = id_tmp
            group_tmp = Group.query.filter_by(idgroups=id_tmp).first()
            if group_tmp:
                item['group_name'] = group_tmp.name
            ret.append(item)
        response_object["status"] = True
        response_object["message"] = "Query success!"
        response_object["group_list"] = ret
    else:
        response_object["message"] = "Error: User does not exist"
    return jsonify(response_object)


@group.route('/query-user', methods=['GET', 'POST'])
def query_user():
    if request.get_method == "POST":
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    response_object = {}
    response_object["status"] = False
    group = Group.query.filter_by(idgroups=group_id).first()
    if group:
        users = group.relation_group_user
        ret = []
        for user in users:
            item = {}
            id_tmp = user.user_id
            item['id'] = id_tmp
            user_tmp = User.query.filter_by(idusers=id_tmp).first()
            if user_tmp:
                item['username'] = user_tmp.username
            ret.append(item)
        response_object["status"] = True
        response_object["message"] = "Query success!"
        response_object["user_list"] = ret
    else:
        response_object["message"] = "Error: Group does not exist"
    return jsonify(response_object)


