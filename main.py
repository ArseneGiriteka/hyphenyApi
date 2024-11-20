

from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from mongoengine import connect

import controllers.friendship_controller
import services.userSearchService
from controllers import user_data_controller
from controllers.conversation_controller import get_conversations_with_user_id
from controllers.login_controller import launch_login
from controllers.message_controller import send_message
from controllers.register_controller import launch_register
from controllers.update_user import update_user
from controllers.user_data_controller import search_user_by_username
from datetime import datetime, timedelta
from services.messages import create_message

connect(db='hyphenyApi_test', alias='core')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Me_and8_My_Homy'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to hypheny!"}), 200

@app.route("/hypheny_landing_page")
def bring_landing_page():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login_route():
    return launch_login(request.get_json())




@app.route('/register', methods=['GET', 'POST'])
def register_user():
    return launch_register(request.get_json())


@app.route('/search/user/username', methods=['GET', 'POST'])
@jwt_required()
def search_on_username():
    data_json = request.get_json()
    username = data_json.get('username')

    if username:
        username = username.strip()

    result = search_user_by_username(username)
    return result

@app.route("/user/id", methods=['GET', 'POST'])
@jwt_required()
def search_user_by_id():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    return controllers.user_data_controller.get_user_by_id(user_id)


@app.route('/random/users', methods=['GET', 'POST'])
@jwt_required()
def get_random_users():
    data_json = request.get_json()
    user_id = data_json.get('id')

    result = user_data_controller.get_random_users(str(user_id))
    print(result)
    return result

@app.route('/user/contacts/to_add', methods=['GET', 'POST'])
@jwt_required()
def get_users_to_add():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    return controllers.user_data_controller.get_users_to_add(user_id)


@app.route('/user/contacts/accepted', methods=['GET', 'POST'])
@jwt_required()
def get_friends():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    return controllers.user_data_controller.get_accepted_contacts(user_id)


@app.route('/user/ask-friendship', methods=['GET', 'POST', 'UPDATE'])
@jwt_required()
def ask_friendship():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    target_id = data_json.get('targetId')
    return controllers.friendship_controller.ask_friendship(user_id, target_id)


@app.route('/user/accept-friendship', methods=['GET', 'POST', 'UPDATE'])
@jwt_required()
def accept_friendship():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    target_id = data_json.get('targetId')
    return controllers.friendship_controller.accept_friendship(user_id, target_id)




@app.route('/user/contacts/pending', methods=['GET', 'POST', 'UPDATE'])
@jwt_required()
def get_pending_contacts():
    data_json = request.get_json()
    user_id = data_json.get('user_id')
    return user_data_controller.get_pending_contacts(user_id)

@app.route("/user", methods=['GET'])
def get_user_by_username():
    json_data = request.get_json()
    username = json_data.get("username").strip()
    return services.userSearchService.get_user_by_username(username)


@app.route("/user/update", methods=['GET', 'POST'])
@jwt_required()
def update_user_profile():
    json_data = request.get_json()
    user_id = json_data.get("userId")
    username = json_data.get("username")
    email = json_data.get("email")
    password = json_data.get("password")

    return update_user(user_id, username, email, password)




@app.route("/get_message", methods=['GET'])
def get_message():
    json_data = request.get_json()
    message_id = json_data.get("message_id")
    conversation_id = json_data.get("conversation_id")
    sender_id = json_data.get("sender_id")

@app.route("/conversation/private/new", methods=['GET', 'POST', 'UPDATE'])
def create_private_conversation():
    data_json = request.get_json()
    user_id = data_json.get('userId')
    user = data_json.get('user')
    title = ""


@app.route("/user/conversation", methods=['GET', 'POST'])
@jwt_required()
def get_conversations_by_user_id():
    json_data = request.get_json()
    user_id = json_data.get("userId")
    return get_conversations_with_user_id(user_id)


@app.route('/conversation/id', methods=['GET', 'POST'])
@jwt_required()
def get_conversation_by_id():
    json_data = request.get_json()
    conversation_id = json_data.get("conversationId")
    result = controllers.conversation_controller.get_conversation_by_id(conversation_id)
    print(result)
    return result


@app.route('/user/conversation/send/new_message', methods=['GET', 'POST'])
@jwt_required()
def create_message():
    json_data = request.get_json()
    sender_id = json_data.get("senderId")
    conversation_id = json_data.get("conversationId")
    content = json_data.get("body")
    message_type = json_data.get("messageType")
    return send_message(sender_id=sender_id, conversation_id=conversation_id, content=content, message_type=message_type)

@app.route('/user/conversation/get/messages', methods=['GET', 'POST'])
@jwt_required()
def get_message_of_conversation():
    json_data = request.get_json()
    user_id = json_data.get("userId")
    conversation_id = json_data.get("conversationId")
    result = controllers.message_controller.get_messages_of_conversation(user_id, conversation_id)
    return result



@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Hello, user {current_user_id}!"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
