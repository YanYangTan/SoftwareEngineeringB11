from flask import Blueprint, jsonify, request
from . import db
from .models import *
from .utils import authorize
import random, json

genealogy = Blueprint('genealogy', __name__)


@genealogy.route('/query-genealogy', methods=['GET', 'POST'])
def query_genealogy():
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
        genealogy = Genealogy.query.filter_by(group_id=group_id).first()
        if not genealogy:
            genealogy_new = Genealogy()
            rand_num = 0
            while True:
                rand_num = random.randint(1, 1000000)
                res = Genealogy.query.filter_by(id=rand_num).first()
                if not res:
                    break
            genealogy_new.id = rand_num
            genealogy_new.group_id = group_id
            content = {}
            genealogy_new.content = json.dumps(content)
            db.session.add(genealogy_new)
            try:
                db.session.commit()
                response_object['status'] = True
                response_object['message'] = "Genealogy not found, created empty genealogy!"
                response_object['content'] = content
            except Exception as e:
                print(e)
                response_object['message'] = "Genealogy not found, failed to create empty genealogy"
        else:
            response_object['status'] = True
            response_object['message'] = "Query success!"
            response_object['content'] = json.loads(genealogy.content)
    return jsonify(response_object)


@genealogy.route('/save-genealogy', methods=['GET', 'POST'])
def save_genealogy():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        content = post_data.get('content')
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
        genealogy = Genealogy.query.filter_by(group_id=group_id).first()
        if not genealogy:
            genealogy_new = Genealogy()
            rand_num = 0
            while True:
                rand_num = random.randint(1, 1000000)
                res = Genealogy.query.filter_by(id=rand_num).first()
                if not res:
                    break
            genealogy_new.id = rand_num
            genealogy_new.group_id = group_id
            genealogy_new.content = json.dumps(content)
            db.session.add(genealogy_new)
        else:
            genealogy.content = json.dumps(content)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Successfully saved!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to save"
    return jsonify(response_object)