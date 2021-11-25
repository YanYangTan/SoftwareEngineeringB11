from flask import Blueprint, jsonify, request
from . import db
from .models import *
from .utils import check_groupname
import random

group = Blueprint('group', __name__)


@group.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == "POST":
        post_data = request.get_json()
        group_name = post_data.get('group_name')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False
    if not check_groupname(group_name):
        response_object["message"] = "Error: Group name invalid!"
    else:
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

        rel = RelationGroupUser()
        rand_number2 = 0
        while True:
            rand_number2 = random.randint(1, 100000)
            res = RelationGroupUser.query.filter_by(id=rand_number2).first()
            if not res:
                break
        rel.id = rand_number2
        rel.group_id = rand_number
        rel.user_id = user_id
        rel.admin = True
        db.session.add(group)
        db.session.add(rel)
        try:
            db.session.commit()
            response_object["status"] = True
            response_object["message"] = "Group created!"
            response_object["group_id"] = rand_number
            response_object["invite_key"] = tmp
        except Exception as e:
            print(e)
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
    if request.method == "POST":
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
            db.session.add(rel_group)
            try:
                db.session.commit()
                response_object["status"] = True
                response_object["message"] = "User added to group!"
            except Exception as e:
                print(e)
                response_object["message"] = "Failed to join group"
    return jsonify(response_object)


@group.route('/query-group', methods=['GET', 'POST'])
def query_group():
    if request.method == "POST":
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
            item['admin'] = group.admin
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
    if request.method == "POST":
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
            item['admin'] = user.admin
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


@group.route('/query-admin', methods=['GET', 'POST'])
def query_admin():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status']= False
    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not rel:
        response_object['message'] = "Error: User not in group!"
    else:
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['admin'] = rel.admin
    return jsonify(response_object)


@group.route('/set-admin', methods=['GET', 'POST'])
def set_admin():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False
    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not rel:
        response_object["message"] = "Error: User not in group!"
    else:
        if rel.admin:
            response_object["message"] = "Error: User already an admin!"
        else:
            rel.admin = True
            try:
                db.session.commit()
                response_object["status"] = True
                response_object["message"] = "User set as admin"
            except Exception as e:
                print(e)
                response_object["message"] = "Set as admin failed"
    return jsonify(response_object)


@group.route('/remove-admin', methods=['GET', 'POST'])
def remove_admin():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object["message"] = "Error: Group does not exist!"
        return jsonify(response_object)
    else:
        users = group.relation_group_user
        admin_count = 0
        for user in users:
            if user.admin:
                admin_count += 1
        if admin_count == 1:
            response_object['message'] = "Error: Number of admins in a group can't be less than 1!"
            return jsonify(response_object)

    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not rel:
        response_object["message"] = "Error: User not in group!"
    else:
        if not rel.admin:
            response_object["message"] = "Error: User not an admin!"
        else:
            rel.admin = False
            try:
                db.session.commit()
                response_object["status"] = True
                response_object["message"] = "User's admin status removed"
            except Exception as e:
                print(e)
                response_object["message"] = "Remove admin failed"
    return jsonify(response_object)


@group.route('/change-groupname', methods=['GET', 'POST'])
def change_group_name():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        new_name = post_data.get('new_name')
    response_object = {}
    response_object['status'] = False
    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist!"
    else:
        if not check_groupname(new_name):
            response_object["message"] = "Error: New group name invalid!"
        else:
            group.name = new_name
            try:
                db.session.commit()
                response_object['status'] = True
                response_object['message'] = "Group name changed successfully"
            except Exception as e:
                print(e)
                response_object['message'] = "Failed to change group name"
    return jsonify(response_object)


@group.route('/delete-group', methods=['GET', 'POST'])
def delete_group():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    response_object = {}
    response_object['status'] = False
    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist!"
    else:
        groups = group.relation_group_user
        for item in groups:
            db.session.delete(item)
        db.session.delete(group)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Group deleted"
        except Exception as e:
            print(e)
            response_object['message'] = "Delete group failed"
    return jsonify(response_object)


@group.route('/remove-member', methods=['GET', 'POST'])
def remove_member():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False
    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not rel:
        response_object['message'] = "Error: User not in group!"
    else:
        db.session.delete(rel)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "User removed from group"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to remove user"
    return jsonify(response_object)


@group.route('/leave-group', methods=['GET', 'POST'])
def leave_group():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False
    rel = RelationGroupUser.query.filter_by(group_id=group_id, user_id=user_id).first()
    if not rel:
        response_object['message'] = "Error: User not in group!"
    else:
        group = Group.query.filter_by(idgroups=group_id).first()
        if not group:
            response_object["message"] = "Error: Group does not exist!"
            return jsonify(response_object)
        else:
            users = group.relation_group_user
            admin_count = 0
            for user in users:
                if user.admin:
                    admin_count += 1
            if admin_count == 1 and rel.admin:
                response_object['message'] = "Error: Please set another member as admin first!"
                return jsonify(response_object)

        db.session.delete(rel)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Successfully left group"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to leave group"
    return jsonify(response_object)
