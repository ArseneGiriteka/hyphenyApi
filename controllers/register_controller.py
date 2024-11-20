from flask import jsonify

from services.register import register


def launch_register(json_data):
    if not json_data:
        return jsonify({'message': 'No data provided'}), 400

    username_given = json_data.get('username').strip()
    email_given = json_data.get('email').strip()
    password_given = json_data.get('password').strip()

    print(f"--{username_given}--{email_given}--{password_given}--")

    if not (username_given and email_given and password_given):
        return jsonify({'message': 'You must provide username, email and password'}), 400

    try:
        message = register(username_given, email_given, password_given)
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 401