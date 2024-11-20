from flask import request, jsonify

from services.login import login

def launch_login(data_json):
    if not data_json:
        return jsonify({'message': 'No data provided'}), 400

    username_given = data_json.get('username').strip()
    password_given = data_json.get('password').strip()

    # Check if username and password are provided
    if not (username_given and password_given):
        return jsonify({'message': 'You must provide both username and password'}), 400

    result = login(username_given, password_given)
    if result.get("access_token"):
        return jsonify(result), 200
    else:
        return jsonify(result), 400