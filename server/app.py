from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

USERS = [
    {
        'username': 'kky',
        'password': 'abc123'
    },
    {
        'username': 'Kun',
        'password': 'CTID'
    }
]


# sanity check route
@app.route('/success', methods=['GET'])
def ping_pong():
    return jsonify('Success!')


@app.route('/login', methods=['GET', 'POST'])
def all_books():
    response_object = {"status": False}
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        user_found = False
        for user in USERS:
            if username == user["username"]:
                user_found = True
                if password == user["password"]:
                    response_object["status"] = True
                    response_object["message"] = "Login success!"
                else:
                    response_object["message"] = "Wrong password!"
        if not user_found:
            response_object["message"] = "User does not exist!"
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)