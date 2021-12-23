from flask import Blueprint, jsonify, request, make_response
from . import db
from .models import *
from datetime import datetime
from .utils import query_username_by_id, check_len45, authorize
from sqlalchemy import desc
import os, configparser, random, uuid, json, pathlib

photowall = Blueprint('photowall', __name__)


@photowall.route('/upload-post', methods=['GET', 'POST'])
def upload_post():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        user_id = request.form.get('user_id')
        group_id = request.form.get('group_id')
        caption = request.form.get('caption')
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

    config = configparser.RawConfigParser()
    config.read('config.cfg')
    photo_dict = dict(config.items('PHOTO'))
    upload_folder = photo_dict["upload_folder"]
    # upload_folder = "\\Downloads\\temp\\upload"

    if not check_len45(caption):
        response_object['message'] = "Error: Invalid caption"
        return jsonify(response_object)

    dir = os.path.join(upload_folder, group_id)
    if not os.path.exists(dir):
        os.makedirs(dir)

    if files:
        for file in files:
            photo_post = PhotoPost()
            rand_num = 0
            while True:
                rand_num = random.randint(1, 1000000)
                res = PhotoPost.query.filter_by(id=rand_num).first()
                if not res:
                    break
            photo_post.id = rand_num
            photo_post.user_id = int(user_id)
            photo_post.group_id = int(group_id)
            photo_post.caption = caption
            photo_post.like = 0
            like_users = []
            photo_post.like_users = json.dumps(like_users)
            photo_post.date_created = datetime.now()
            locations = []
            file_ext = pathlib.Path(file.filename).suffix
            filename = uuid.uuid4().hex + file_ext
            path = os.path.join(dir, filename)
            file.save(path)
            locations.append(filename)
            photo_post.media = json.dumps(locations)
            db.session.add(photo_post)

    try:
        db.session.commit()
        response_object['status'] = True
        response_object['message'] = "Photos uploaded!"
        response_object['post_id'] = photo_post.id
    except Exception as e:
        print(e)
        response_object['message'] = "Upload failed!"

    return jsonify(response_object)


@photowall.route('/query-all-post', methods=['GET', 'POST'])
def query_all_post():
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
        posts = PhotoPost.query.filter_by(group_id=group_id).order_by(desc(PhotoPost.date_created)).all()
        ret = []
        for post in posts:
            item = {}
            item['id'] = post.id
            item['user_id'] = post.user_id
            item['username'] = query_username_by_id(post.user_id)
            item['caption'] = post.caption
            item['media'] = json.loads(post.media)
            item['like'] = post.like
            item['date_created'] = post.date_created
            ret.append(item)
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['post_list'] = ret
    return jsonify(response_object)


@photowall.route('/show/<int:group_id>/<string:filename>', methods=['GET'])
def show_photo(group_id, filename):
    if request.method == 'GET':
        response_object = {}
        response_object["status"] = False
        if not filename:
            response_object["message"] = "Error: Too few arguments!"
            return jsonify(response_object)
        else:
            config = configparser.RawConfigParser()
            config.read('config.cfg')
            photo_dict = dict(config.items('PHOTO'))
            upload_folder = photo_dict["upload_folder"]
            # upload_folder = "\\Downloads\\temp\\upload"

            file_dir = os.path.join(upload_folder, str(group_id))
            file = os.path.join(file_dir, filename)
            if not os.path.isfile(file):
                response_object["message"] = "Error: File does not exist!"
                return jsonify(response_object)
            else:
                image_data = open(file, "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response


@photowall.route('/like-post', methods=['GET', 'POST'])
def like_post():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data['post_id']
        user_id = post_data['user_id']
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    else:
        post.like += 1
        like_users = json.loads(post.like_users)
        like_users.append(user_id)
        post.like_users = json.dumps(like_users)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Liked!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed!"
    return jsonify(response_object)


@photowall.route('/add-comment', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data.get('post_id')
        user_id = post_data.get('user_id')
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

    if not check_len45(content):
        response_object['message'] = "Error: Comment invalid!"
        return jsonify(response_object)

    post = PhotoPost.query.filter_by(id=post_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    else:
        comment = Comments()
        rand_number = 0
        while True:
            rand_number = random.randint(1, 1000000)
            res = Comments.query.filter_by(id=rand_number).first()
            if not res:
                break
        comment.id = rand_number
        comment.user_id = user_id
        comment.content = content
        comment.date_created = datetime.now()

        rel_post_comment = RelationPostComment()
        rand_number = 0
        while True:
            rand_number = random.randint(1, 1000000)
            res2 = RelationPostComment.query.filter_by(id=rand_number).first()
            if not res2:
                break
        rel_post_comment.id = rand_number
        rel_post_comment.post_id = post_id
        rel_post_comment.comment_id = comment.id
        db.session.add(comment)
        db.session.add(rel_post_comment)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Comment added!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to comment"
    return jsonify(response_object)


@photowall.route('/query-comment', methods=['GET', 'POST'])
def query_comment():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data.get('post_id')
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    else:
        rels = post.relation_post_comment
        ret = []
        for rel in rels:
            item = {}
            comment_id = rel.comment_id
            comment = Comments.query.filter_by(id=comment_id).first()
            item['id'] = comment.id
            item['user_id'] = comment.user_id
            item['username'] = query_username_by_id(comment.user_id)
            item['content'] = comment.content
            item['date_created'] = comment.date_created
            ret.append(item)
        ret.sort(key=lambda x: x['date_created'])
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['comments_list'] = ret
    return jsonify(response_object)


@photowall.route('/query-like', methods=['GET', 'POST'])
def query_like():
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data.get('user_id')
        post_id = post_data.get('post_id')
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    else:
        like_users = json.loads(post.like_users)
        liked = False
        for like_user in like_users:
            if like_user == user_id:
                liked = True
                break
        response_object['status'] = True
        response_object['message'] = "Query success!"
        response_object['liked'] = liked
    return jsonify(response_object)


@photowall.route('/delete-post', methods=['GET', 'POST'])
def delete_post():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data.get('post_id')
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    elif user_id != post.user_id:
        response_object['message'] = "Error: User not creator of post!"
    else:
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        photo_dict = dict(config.items('PHOTO'))
        upload_folder = photo_dict["upload_folder"]
        # upload_folder = "\\Downloads\\temp\\upload"

        for filename in json.loads(post.media):
            print(filename)
            photo = os.path.join(upload_folder, str(post.group_id), filename)
            if os.path.isfile(photo):
                os.remove(photo)

        for rel in post.relation_post_comment:
            tmp = Comments.query.filter_by(id=rel.comment_id).first()
            db.session.delete(tmp)
            db.session.delete(rel)
        db.session.delete(post)

        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Post deleted!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to delete"
    return jsonify(response_object)


@photowall.route('/delete-comment', methods=['GET', 'POST'])
def delete_comment():
    if request.method == 'POST':
        post_data = request.get_json()
        comment_id = post_data.get('comment_id')
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

    comment = Comments.query.filter_by(id=comment_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not comment:
        response_object['message'] = "Error: Comment does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    elif user_id != comment.user_id:
        response_object['message'] = "Error: User not creator of comment!"
    else:
        for rel in comment.relation_post_comment:
            db.session.delete(rel)
        db.session.delete(comment)
        try:
            db.session.commit()
            response_object['status'] = True
            response_object['message'] = "Comment deleted!"
        except Exception as e:
            print(e)
            response_object['message'] = "Failed to delete!"
    return jsonify(response_object)


@photowall.route('/cancel-like', methods=['GET', 'POST'])
def cancel_like():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data.get('post_id')
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    user = User.query.filter_by(idusers=user_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    elif not user:
        response_object['message'] = "Error: User does not exist!"
    else:
        liked = False
        like_users = json.loads(post.like_users)
        for like_user in like_users:
            if user_id == like_user:
                liked = True
                break
        if not liked:
            response_object['message'] = "Error: User haven't liked the post!"
        else:
            like_users.remove(user_id)
            post.like -= 1
            post.like_users = json.dumps(like_users)
            try:
                db.session.commit()
                response_object['status'] = True
                response_object['message'] = "Successfully unliked!"
            except Exception as e:
                print(e)
                response_object['message'] = "Failed to unlike"
    return jsonify(response_object)


@photowall.route('/query-post', methods=['GET', 'POST'])
def query_post():
    if request.method == 'POST':
        post_data = request.get_json()
        post_id = post_data.get('post_id')
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

    post = PhotoPost.query.filter_by(id=post_id).first()
    if not post:
        response_object['message'] = "Error: Post does not exist!"
    else:
        response_object['status'] = True
        response_object['message'] = "Query success!"
        item = {}
        item['post_id'] = post.id
        item['user_id'] = post.user_id
        item['username'] = query_username_by_id(post.user_id)
        item['caption'] = post.caption
        item['media'] = json.loads(post.media)
        item['like'] = post.like
        item['date_created'] = post.date_created
        response_object['content'] = item
    return jsonify(response_object)