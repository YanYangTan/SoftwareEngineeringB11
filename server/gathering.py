from flask import Blueprint, jsonify, request
from . import db
from .models import *
from .utils import query_username_by_id
from datetime import datetime
import random, json

gathering = Blueprint('gathering', __name__)


@gathering.route('/create-gathering', methods=['GET', 'POST'])
def create_gathering():
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data.get('user_id')
        group_id = post_data.get('group_id')
        name = post_data.get('name')
        description = post_data.get('description')
        enddate = post_data.get('enddate')
        status = post_data.get('status')
        content = post_data.get('content')
    response_object = {}
    response_object['status'] = False

    try:
        content = json.loads(content)
    except Exception as e:
        print(e)

    rel_user = RelationGroupUser.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not rel_user:
        response_object['message'] = "Error: User not in group!"
    else:
        rand_number = 0
        while True:
            rand_number = random.randint(1, 100000)
            res = Gathering.query.filter_by(id=rand_number).first()
            if not res:
                break
        gathering = Gathering()
        gathering.id = rand_number
        gathering.user_id = user_id
        gathering.group_id = group_id
        gathering.name = name
        gathering.description = description
        gathering.enddate = enddate
        gathering.status = status
        db.session.add(gathering)
        if gathering.status:        # Is gathering suggest
            for item in content:
                suggestion = Suggestion()
                rand_number = 0
                while True:
                    rand_number = random.randint(1, 1000000)
                    res2 = Suggestion.query.filter_by(id=rand_number).first()
                    if not res2:
                        break
                suggestion.id = rand_number
                suggestion.user_id = user_id
                suggestion.content = json.dumps(item)

                rel = RelationGathering()
                rand_number = 0
                while True:
                    rand_number = random.randint(1, 1000000)
                    res3 = RelationGathering.query.filter_by(id=rand_number).first()
                    if not res3:
                        break
                rel.id = rand_number
                rel.gathering_id = gathering.id
                rel.suggestion_id = suggestion.id
                rel.status = True
                db.session.add(suggestion)
                db.session.add(rel)
        else:           # Is gathering vote
            for item in content:
                vote = VoteOptions()
                rand_number = 0
                while True:
                    rand_number = random.randint(1, 1000000)
                    res2 = VoteOptions.query.filter_by(id=rand_number).first()
                    if not res2:
                        break
                vote.id = rand_number
                vote.content = json.dumps(item)
                voters = []
                vote.voters = json.dumps(voters)

                rel = RelationGathering()
                rand_number = 0
                while True:
                    rand_number = random.randint(1, 1000000)
                    res3 = RelationGathering.query.filter_by(id=rand_number).first()
                    if not res3:
                        break
                rel.id = rand_number
                rel.gathering_id = gathering.id
                rel.vote_id = vote.id
                rel.status = False
                db.session.add(vote)
                db.session.add(rel)
        try:
            db.session.commit()
            response_object["status"] = True
            response_object["message"] = "Gathering created!"
            response_object["gathering_id"] = gathering.id
        except Exception as e:
            print(e)
            response_object["message"] = "Failed to create gathering"
    return jsonify(response_object)


@gathering.route('/query-all-gathering', methods=['GET', 'POST'])
def query_all_gathering():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    response_object = {}
    response_object['status'] = False

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist"
    else:
        gatherings = Gathering.query.filter_by(group_id=group_id).all()
        ret = []
        for gathering in gatherings:
            item = {}
            item['id'] = gathering.id
            item['user_id'] = gathering.user_id
            item['name'] = gathering.name
            item['description'] = gathering.description
            item['enddate'] = gathering.enddate
            item['status'] = gathering.status
            ret.append(item)
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['gathering_list'] = ret
    return jsonify(response_object)


@gathering.route('/query-gathering', methods=['GET', 'POST'])
def query_gathering():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
    response_object = {}
    response_object['status'] = False

    gathering = Gathering.query.filter_by(id=gathering_id).first()
    if not gathering:
        response_object['message'] = "Error: Gathering not found!"
    else:
        rels = gathering.relation_gathering
        ret = []
        for rel in rels:
            option = {}
            if rel.status:  # Is gathering suggestion
                suggest_id = rel.suggestion_id
                suggestion = Suggestion.query.filter_by(id=suggest_id).first()
                option['id'] = suggest_id
                option['user_id'] = suggestion.user_id
                option['content'] = json.loads(suggestion.content)
            else:  # Is gathering vote
                vote_id = rel.vote_id
                vote = VoteOptions.query.filter_by(id=vote_id).first()
                option['id'] = vote_id
                option['content'] = json.loads(vote.content)
                option['vote_count'] = vote.vote_count
                option['voters'] = []
                for voter in json.loads(vote.voters):
                    option['voters'].append(query_username_by_id(voter))
            ret.append(option)
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['options'] = ret
    return jsonify(response_object)


@gathering.route('/save-suggestion', methods=['GET', 'POST'])
def save_suggestion():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
        user_id = post_data.get('user_id')
        content = post_data.get('content')
    response_object = {}
    response_object['status'] = False

    try:
        content = json.loads(content)
    except Exception as e:
        print(e)


    gathering = Gathering.query.filter_by(id=gathering_id).first()
    if not gathering:
        response_object['message'] = "Error: Gathering not found!"
    else:
        for rel in gathering.relation_gathering:
            db.session.delete(rel)
        for item in content:
            suggestion = Suggestion()
            rand_number = 0
            while True:
                rand_number = random.randint(1, 1000000)
                res = Suggestion.query.filter_by(id=rand_number).first()
                if not res:
                    break
            suggestion.id = rand_number
            suggestion.user_id = user_id
            suggestion.content = json.dumps(item)

            rel = RelationGathering()
            rand_number = 0
            while True:
                rand_number = random.randint(1, 1000000)
                res2 = RelationGathering.query.filter_by(id=rand_number).first()
                if not res2:
                    break
            rel.id = rand_number
            rel.gathering_id = gathering.id
            rel.suggestion_id = suggestion.id
            rel.status = True
            db.session.add(suggestion)
            db.session.add(rel)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Suggestion successfully saved!"
        except Exception as e:
            print(e)
            response_object['message'] = "Save suggestion failed!"
    return jsonify(response_object)


@gathering.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        post_data = request.get_json()
        vote_id = post_data.get('vote_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False

    vote = VoteOptions.query.filter_by(id=vote_id).first()
    if not vote:
        response_object['message'] = "Error: Vote option not found!"
    else:
        vote.vote_count += 1
        voters = json.loads(vote.voters)
        voters.append(user_id)
        vote.voters = json.dumps(voters)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Vote success!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to vote"
    return jsonify(response_object)
