from flask import Blueprint, jsonify, request, make_response
from . import db
from .models import *
from datetime import datetime
from PIL import Image
import os, configparser, random, uuid, json, pathlib, io

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

    config = configparser.RawConfigParser()
    config.read('config.cfg')
    photo_dict = dict(config.items('PHOTO'))
    upload_folder = photo_dict["upload_folder"]

    dir = os.path.join(upload_folder, group_id)
    if not os.path.exists(dir):
        os.makedirs(dir)

    photo_post = PhotoPost()
    photo_post.id = uuid.uuid4().hex
    photo_post.user_id = int(user_id)
    photo_post.group_id = int(group_id)
    photo_post.caption = caption
    photo_post.like = 0
    photo_post.date_created = datetime.now()
    locations = []
    if files:
        for file in files:
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

    group = Group.query.filter_by(idgroups=group_id).first()
    if not group:
        response_object['message'] = "Error: Group does not exist!"
    else:
        posts = PhotoPost.query.filter_by(group_id=group_id).all()
        ret = []
        for post in posts:
            item = {}
            item['id'] = post.id
            item['user_id'] = post.user_id
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
