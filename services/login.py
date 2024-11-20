from flask import jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User


def login(username_given: str, password_given: str):
    user = User.objects(username=username_given).first()
    if not user:
        user = User.objects(email=username_given).first()
        if user is None:
            return {
                "access_token": None,
                "user_data": None,
                "message": f"Account with {username_given} doesn't exist"
            }

    if user and check_password_hash(user.password, password_given):
        access_token = create_access_token(identity=str(user.id))
        user_data = user.to_dict()
        result_data = {
            "access_token": access_token if access_token else None,
            "user_data": user_data,
            "message": f"Connected successfully as {user.username}"
        }
        return result_data
    return {
        "access_token": None,
        "user_data": None,
        "message": "wrong credentials"
    }

def logout():
    """"""