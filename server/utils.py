import scrypt, base64, configparser, random, json
import re
from datetime import datetime, timedelta
from . import scheduler
from .models import *
import random, string


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
    nowtime = int(datetime.now().date().strftime('%Y%m%d'))
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


def generate_new_key():
    length = random.randint(5, 10)
    rand_key = ''
    while True:
        rand_key = rand_key.join((random.choice(string.ascii_uppercase) for x in range(length)))
        res = Group.query.filter_by(invite_key=rand_key).first()
        if not res:
            break
    return rand_key


def update_suggestion():
    with scheduler.app.app_context():
        triggered = False
        gatherings = Gathering.query.filter_by(status=True).all()
        for gathering in gatherings:
            if datetime.now() > gathering.enddate:
                triggered = True
                gathering.enddate = gathering.enddate + timedelta(days=3)
                gathering.status = False
                for rel in gathering.relation_gathering:
                    suggest_tmp = Suggestion.query.filter_by(id=rel.suggestion_id).first()
                    vote = VoteOptions()
                    rand_number = 0
                    while True:
                        rand_number = random.randint(1, 10000000)
                        res = VoteOptions.query.filter_by(id=rand_number).first()
                        if not res:
                            break
                    vote.id = rand_number
                    vote.content = suggest_tmp.content
                    vote.vote_count = 0
                    voters = []
                    vote.voters = json.dumps(voters)

                    relation = RelationGathering()
                    rand_number = 0
                    while True:
                        rand_number = random.randint(1, 10000000)
                        res2 = RelationGathering.query.filter_by(id=rand_number).first()
                        if not res2:
                            break
                    relation.id = rand_number
                    relation.gathering_id = gathering.id
                    relation.vote_id = vote.id
                    relation.status = False
                    db.session.delete(suggest_tmp)
                    db.session.delete(rel)
                    db.session.add(vote)
                    db.session.add(relation)
        if triggered:
            try:
                db.session.commit()
                print("Suggestion updated to vote!")
            except Exception as e:
                print(e)


def update_vote():
    with scheduler.app.app_context():
        triggered = False
        gatherings = Gathering.query.filter_by(status=False).all()
        for gathering in gatherings:
            if datetime.now() > gathering.enddate:
                triggered = True
                max = 0
                highest_option = {}
                for rel in gathering.relation_gathering:
                    vote = VoteOptions.query.filter_by(id=rel.vote_id).first()
                    if vote.vote_count >= max:
                        max = vote.vote_count
                        highest_option = json.loads(vote.content)
                    db.session.delete(vote)
                    db.session.delete(rel)
                group = Group.query.filter_by(idgroups=gathering.group_id).first()
                if not group:
                    continue
                calendar = Calendar.query.filter_by(group_id=gathering.group_id).first()
                highest_option['name'] = gathering.name
                highest_option['description'] = gathering.description
                if not calendar:
                    new_calendar = Calendar()
                    rand_number = 0
                    while True:
                        rand_number = random.randint(1, 1000000)
                        res = Calendar.query.filter_by(id=rand_number).first()
                        if not res:
                            break
                    new_calendar.id = rand_number
                    new_calendar.group_id = gathering.group_id
                    content = []
                    content.append(highest_option)
                    new_calendar.content = json.dumps(content)
                    db.session.add(new_calendar)
                else:
                    content = json.loads(calendar.content)
                    content.append(highest_option)
                    calendar.content = json.dumps(content)
                db.session.delete(gathering)
        if triggered:
            try:
                db.session.commit()
                print("Highest vote added to calendar")
            except Exception as e:
                print(e)

