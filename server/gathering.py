from flask import Blueprint, jsonify, request
from . import db
from .models import *
from .utils import query_username_by_id, update_suggestion, update_vote
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
        allow_multiple_vote = post_data.get('allow_multiple_vote')
        status = post_data.get('status')
        content = post_data.get('content')
    response_object = {}
    response_object['status'] = False

    try:
        content = json.loads(content)
    except Exception as e:
        print(e)

    valid = True
    try:
        if enddate < datetime.now():
            valid = False
    except Exception as e:
        print(e)
        enddate = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')
        if enddate < datetime.now():
            valid = False

    if not valid:
        response_object["message"] = "Error: Cannot set end date earlier than current time!"
        return jsonify(response_object)

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
        gathering.allow_multiple_vote = allow_multiple_vote
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
            item['username'] = query_username_by_id(gathering.user_id)
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
                option['username'] = query_username_by_id(suggestion.user_id)
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
        response_object['allow_multiple_vote'] = gathering.allow_multiple_vote
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
        if gathering.status:
            for rel in gathering.relation_gathering:
                suggest_tmp = Suggestion.query.filter_by(id=rel.suggestion_id).first()
                db.session.delete(suggest_tmp)
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
        else:
            response_object['message'] = "Error: Not a suggestion!"
    return jsonify(response_object)


@gathering.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        post_data = request.get_json()
        vote_ids = post_data.get('vote_ids')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False

    try:
        vote_ids = json.loads(vote_ids)
    except Exception as e:
        print(e)

    flag = True
    for vote_id in vote_ids:
        vote = VoteOptions.query.filter_by(id=vote_id).first()
        if not vote:
            response_object['message'] = "Error: Vote option not found!"
            flag = False
            break
        else:
            vote.vote_count += 1
            voters = json.loads(vote.voters)
            voters.append(user_id)
            vote.voters = json.dumps(voters)

    if flag:
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Vote success!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to vote"
    return jsonify(response_object)


@gathering.route('/refresh-suggest', methods=['GET', 'POST'])
def refresh_suggest():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
    response_object = {}
    response_object['status'] = False

    gathering = Gathering.query.filter_by(id=gathering_id).first()
    if not gathering:
        response_object['message'] = "Error: Gathering not found!"
    else:
        if gathering.status:
            now = datetime.now()
            if now > gathering.enddate:
                status, message = update_suggestion(gathering_id)
                response_object['status'] = status
                response_object['message'] = message
            else:
                response_object['status'] = True
                response_object['message'] = "Not updated"
        else:
            response_object['message'] = "Error: Not a suggestion!"
    return jsonify(response_object)


@gathering.route('/change-enddate', methods=['GET', 'POST'])
def change_enddate():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
        new_date = post_data.get('new_date')
    response_object = {}
    response_object['status'] = False
    valid = True
    try:
        if new_date < datetime.now():
            valid = False
    except Exception as e:
        print(e)
        new_date = datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S')
        if new_date < datetime.now():
            valid = False

    if not valid:
        response_object['message'] = "Error: Can't change to an earlier time than now!"
    else:
        gathering = Gathering.query.filter_by(id=gathering_id).first()
        if not gathering:
            response_object['message'] = "Error: Gathering not found!"
        else:
            gathering.enddate = new_date
            try:
                db.session.commit()
                response_object['status'] = True
                response_object['message'] = "End date successfully changed!"
            except Exception as e:
                print(e)
                response_object['message'] = "Change date failed"
    return jsonify(response_object)


@gathering.route('/refresh-vote', methods=['GET', 'POST'])
def refresh_vote():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
    response_object = {}
    response_object['status'] = False

    gathering = Gathering.query.filter_by(id=gathering_id).first()
    if not gathering:
        response_object['message'] = "Error: Gathering not found!"
    else:
        if not gathering.status:
            now = datetime.now()
            if now > gathering.enddate:
                status, message = update_vote(gathering_id)
                response_object['status'] = status
                response_object['message'] = message
            else:
                response_object['message'] = "Not updated!"
        else:
            response_object['message'] = "Error: Not a vote!"
    return jsonify(response_object)


@gathering.route('/query-calendar', methods=['GET', 'POST'])
def query_calendar():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
    response_object = {}
    response_object['status'] = False

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group not found!"
    else:
        calendar = Calendar.query.filter_by(group_id=group_id).first()
        if calendar:
            response_object['status'] = True
            response_object['message'] = "Query success!"
            response_object['calendar'] = json.loads(calendar.content)
        else:
            new_calendar = Calendar()
            rand_number = 0
            while True:
                rand_number = random.randint(1, 1000000)
                res = Calendar.query.filter_by(id=rand_number).first()
                if not res:
                    break
            new_calendar.id = rand_number
            new_calendar.group_id = group_id
            content = []
            new_calendar.content = json.dumps(content)
            db.session.add(new_calendar)
            try:
                db.session.commit()
                response_object['status'] = True
                response_object['message'] = "Calendar not found! Created empty calendar"
                response_object['calendar'] = content
            except Exception as e:
                print(e)
                response_object['message'] = "Calendar not found! Add calendar failed"
    return jsonify(response_object)


@gathering.route('/save-calendar', methods=['GET', 'POST'])
def save_calendar():
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data.get('group_id')
        content = post_data.get('content')
    response_object = {}
    response_object['status'] = False

    try:
        content = json.loads(content)
    except Exception as e:
        print(e)

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group not found!"
    else:
        calendar = Calendar.query.filter_by(group_id=group_id).first()
        if calendar:
            calendar.content = json.dumps(content)
        else:
            new_calendar = Calendar()
            rand_number = 0
            while True:
                rand_number = random.randint(1, 1000000)
                res = Calendar.query.filter_by(id=rand_number).first()
                if not res:
                    break
            new_calendar.id = rand_number
            new_calendar.group_id = group_id
            new_calendar.content = json.dumps(content)
            db.session.add(new_calendar)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Calendar saved!"
        except Exception as e:
            print(e)
            response_object['message'] = "Save calendar failed!"
    return jsonify(response_object)


@gathering.route('/check-vote', methods=['GET', 'POST'])
def check_vote():
    if request.method == 'POST':
        post_data = request.get_json()
        gathering_id = post_data.get('gathering_id')
        user_id = post_data.get('user_id')
    response_object = {}
    response_object['status'] = False

    gathering = Gathering.query.filter_by(id=gathering_id).first()
    if not gathering:
        response_object['message'] = "Error: Gathering not found!"
    else:
        if gathering.status:
            response_object['message'] = "Error: Not a vote"
        else:
            voted = False
            for rel in gathering.relation_gathering:
                vote = VoteOptions.query.filter_by(id=rel.vote_id).first()
                voters = json.loads(vote.voters)
                for voter in voters:
                    if user_id == voter:
                        voted = True
                        break
                if voted == True:
                    break
            response_object['status'] = True
            response_object['message'] = "Query success!"
            response_object['voted'] = voted
    return jsonify(response_object)