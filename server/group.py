from flask import Blueprint, jsonify, request
from . import db
from .models import *
from .utils import check_len45, generate_new_key, update_birthday, update_calendar, authorize
from datetime import datetime, timedelta
import random, configparser, os, json

group = Blueprint('group', __name__)


@group.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == "POST":
        post_data = request.get_json()
        group_name = post_data.get('group_name')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

    if not check_len45(group_name):
        response_object["message"] = "Error: Group name invalid!"
    else:
        length = random.randint(5, 10)
        rand_num = 0
        while True:
            rand_num = random.randint(1, 100000)
            res = Group.query.filter_by(idgroups=rand_num).first()
            if not res:
                break
        group = Group()
        group.idgroups = rand_num
        group.name = group_name
        group.key_expiry_date = datetime.now() + timedelta(days=7)

        group.invite_key = generate_new_key()

        rel = RelationGroupUser()
        rand_number2 = 0
        while True:
            rand_number2 = random.randint(1, 100000)
            res = RelationGroupUser.query.filter_by(id=rand_number2).first()
            if not res:
                break
        rel.id = rand_number2
        rel.group_id = rand_num
        rel.user_id = user_id
        rel.admin = True
        db.session.add(group)
        db.session.add(rel)
        try:
            db.session.commit()
            response_object["status"] = True
            response_object["message"] = "Group created!"
            response_object["group_id"] = rand_num
            response_object["invite_key"] = group.invite_key
            response_object["key_expiry_date"] = group.key_expiry_date
        except Exception as e:
            print(e)
            response_object["message"] = "Failed to create group"
        try:
            update_birthday(user_id, group.idgroups)
        except Exception as e:
            print(e)
    return jsonify(response_object)


@group.route('/generate-key', methods=['GET', 'POST'])
def generate_key():
    if request.method == "POST":
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    group = Group.query.filter_by(idgroups=group_id).first()
    response_object = {}
    response_object["status"] = False

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

    if group:
        group.invite_key = generate_new_key()
        group.key_expiry_date = datetime.now() + timedelta(days=7)
        try:
            db.session.commit()
            response_object["status"] = True
            response_object["message"] = "Invite key generated!"
            response_object["invite_key"] = group.invite_key
            response_object["key_expiry_date"] = group.key_expiry_date
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
        invite_key = str(post_data.get('invite_key'))
    response_object = {}
    response_object["status"] = False

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

    user = User.query.filter_by(idusers=user_id).first()
    group = Group.query.filter_by(invite_key=invite_key).first()
    if not user:
        response_object["message"] = "Error: User does not exist"
    elif not group:
        response_object["message"] = "Error: Group does not exist"
    else:
        rel = RelationGroupUser.query.filter_by(group_id=group.idgroups, user_id=user_id).first()
        if rel:
            response_object["message"] = "Error: User already in group"
        else:
            if datetime.now() > group.key_expiry_date:
                response_object["expired"] = True
                response_object["message"] = "Error: Invite key expired!"
            else:
                rel_group = RelationGroupUser()
                rand_number = 0
                while True:
                    rand_number = random.randint(1, 100000)
                    res = RelationGroupUser.query.filter_by(id=rand_number).first()
                    if not res:
                        break
                rel_group.id = rand_number
                rel_group.group_id = group.idgroups
                rel_group.user_id = user_id
                db.session.add(rel_group)
                try:
                    db.session.commit()
                    response_object["status"] = True
                    response_object["message"] = "User added to group!"
                    response_object['group_id'] = group.idgroups
                    response_object['group_name'] = group.name
                    response_object['expired'] = False
                except Exception as e:
                    print(e)
                    response_object["message"] = "Failed to join group"
                try:
                    update_birthday(user_id, group.idgroups)
                    update_calendar(user_id, group.idgroups)
                except Exception as e:
                    print(e)
    return jsonify(response_object)


@group.route('/query-group', methods=['GET', 'POST'])
def query_group():
    if request.method == "POST":
        post_data = request.get_json()
        user_id = post_data.get('user_id')
    response_object = {}
    response_object["status"] = False

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist!"
    else:
        if not check_len45(new_name):
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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist!"
    else:
        gatherings = Gathering.query.filter_by(group_id=group_id).all()
        for gathering in gatherings:
            for rel in gathering.relation_gathering:
                if gathering.status:
                    tmp = Suggestion.query.filter_by(id=rel.suggestion_id).first()
                    if tmp:
                        db.session.delete(tmp)
                else:
                    tmp = VoteOptions.query.filter_by(id=rel.vote_id).first()
                    if tmp:
                        db.session.delete(tmp)
                db.session.delete(rel)
            db.session.delete(gathering)

        calendar = Calendar.query.filter_by(group_id=group_id).first()
        if calendar:
            db.session.delete(calendar)

        genealogy = Genealogy.query.filter_by(group_id=group_id).first()
        if genealogy:
            db.session.delete(genealogy)

        posts = PhotoPost.query.filter_by(group_id=group_id).all()
        for post in posts:
            config = configparser.RawConfigParser()
            config.read('config.cfg')
            photo_dict = dict(config.items('PHOTO'))
            upload_folder = photo_dict["upload_folder"]
            # upload_folder = "\\Downloads\\temp\\upload"

            for filename in json.loads(post.media):
                photo = os.path.join(upload_folder, str(post.group_id), filename)
                if os.path.isfile(photo):
                    os.remove(photo)

            for rel in post.relation_post_comment:
                tmp = Comments.query.filter_by(id=rel.comment_id).first()
                db.session.delete(tmp)
                db.session.delete(rel)
            db.session.delete(post)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

    if 'tokens' in request.headers:
        token = request.headers['tokens']
    else:
        response_object['message'] = "Error: No token!"
        return jsonify(response_object)

    status, message = authorize(token)
    if not status:
        response_object['message'] = message
        return jsonify(response_object)

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

