from pyexpat.errors import messages
from typing import Tuple

from bson import ObjectId
from flask import jsonify, Response
from models.user import User
from mongoengine import DoesNotExist

def does_username_exist(username: str) -> bool:
    try:
        user_temp = User.objects.get(username=username)
    except Exception as e:
        return False
    return True

def does_user_id_exist(user_id: str) -> bool:
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        return False
    return True

def does_email_exist(email: str) -> bool:
    try:
        user_temp = User.objects.get(email=email)
    except Exception as e:
        return False
    return True

def get_user_by_username(username: str) -> User:
    user = User.objects(username=username).first()
    if not user:
        user = User.objects(email=username).first()
    return user

def get_user_by_id(user_id: str) -> User|None:
    if does_user_id_exist(user_id):
        return User.objects.get(user_id)
    else:
        return None

def get_first_hundred_users():
    users =  User.objects.limit(100)

def get_user_by_username_only(user_name: str):
    return User.objects(username=user_name).first()

def get_users_without_user_id(user_id: str):
    return User.objects(id__ne=ObjectId(user_id), __raw__={'contacts.pending': {'$nin': [user_id]}})
