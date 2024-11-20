from pyexpat.errors import messages
from unittest import removeResult

from bson import ObjectId
from flask import jsonify

import services.contacts
from models import user
from models.user import User
from services.userSearchService import get_user_by_username, get_first_hundred_users, get_user_by_username_only, \
    get_users_without_user_id


def search_user_by_username(user_name: str):
    user = get_user_by_username_only(user_name)
    if user:
        return {
            "message": "User found",
            "user_data": user.to_dict()
        }, 200

    return {
        "message": "user does not exist",
        "user_data": [u.to_dict() for u in get_first_hundred_users()]
    }, 201

def get_random_users(user_id: str):
    if not user_id:
        return {
            "message": "Error: not provided connected profile",
            "data": None,
        }, 404

    users = get_users_without_user_id(user_id)

    if not users:
        return {
            "message": "Error: no user profile",
            "data": [],
        }, 201


    result = {
        "message": "success: users found",
        "data": [user.to_dict() for user in users]
    }

    return result, 200

def get_pending_contacts(user_id: str):
    if not user_id:
        return jsonify({
            "message": "Error: not provided connected profile",
            "data": None,
        }), 404

    pending_contacts = services.contacts.get_pending_contacts(user_id)

    if not pending_contacts:
        return jsonify({
            "message": "Error: no us profile",
            "data": [],
        }), 201

    result = [us.to_dict() for us in pending_contacts]
    print(result)

    return jsonify({
            "message": "Error: no us profile",
            "data": result,
        }), 200

def get_user_by_id(user_id: str):
    us = User.objects(id=ObjectId(user_id)).first()
    if us:
        return {
            "message": "Ok",
            "data": us.to_dict()
        }, 200
    else:
        return {
            "message": "Not Found",
            "data": None
        }, 400

def get_users_to_add(active_user_id: str):
    active_user: User = User.objects(id=ObjectId(active_user_id)).first()
    if active_user:
        accepted_user_ids = [ObjectId(contact_id) for contact_id in active_user.contacts["accepted"]]
        pending_user_ids = [ObjectId(contact_id) for contact_id in active_user.contacts["pending"]]
        blocked_user_ids = [ObjectId(contact_id) for contact_id in active_user.contacts["blocked"]]
        asked_user_ids = [ObjectId(contact_id) for contact_id in active_user.contacts["asked"]]

        excluded_user_ids = accepted_user_ids + pending_user_ids + blocked_user_ids + asked_user_ids + [ObjectId(active_user_id)]

        users_to_add = User.objects(id__nin=excluded_user_ids)
        print(users_to_add)
        if users_to_add:
            return {
                "message": "users to add found",
                "data": [user_to_add.to_dict() for user_to_add in users_to_add]
            }, 200
        else:
            return {
                "message": "some users to add are not found",
                "data": []
            }, 202
    else:
        return {
            "message": "given invalid active user",
            "data": []
        }, 403

def get_accepted_contacts(userId: str):
    active_user = User.objects(id=ObjectId(userId)).first()
    if active_user:
        friends_ids = [ObjectId(_id) for _id in active_user.contacts["accepted"]]
        friends = User.objects(id__in=friends_ids)
        return {
            "message": "Ok",
            "data": [f.to_dict() for f in friends]
        }, 200
    else:
        return {
            "message": "Failed",
            "data": []
        }, 400