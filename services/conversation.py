from typing import List

import mongoengine
from bson import ObjectId
from flask import jsonify
from mongoengine import DoesNotExist, ReferenceField

from models.conversation import Conversation
from models.user import User


def does_conversation_id_exist(conv_id: str) -> bool:
    if Conversation.objects(id=conv_id).first():
        return True
    else:
        return False

def get_conversation_by_id(conv_id: str) -> Conversation|None:
    return Conversation.objects(id=conv_id).first()

def get_conversations_by_user_id(user_id: str):
    user = User.objects(id=user_id).first()
    if user:
        convs_ids = user.conversations
        print(convs_ids)
        convs = Conversation.objects(id__in=convs_ids)
        convs_list = [conv.to_dict() for conv in convs]
        return jsonify({"conversations": convs_list}), 200
    else:
        return jsonify({"error": "User Conversation Not Found"}), 404

def create_conversation(members: List[ObjectId], admins: List[str], title: str) -> Conversation:
    conv = Conversation(members=members,
                        admins=admins,
                        title=title)
    return conv


def add_conversation_to_users(conversation_id: str, user_ids: List[str]):
    conversation = Conversation.objects(id=ObjectId(conversation_id)).first()
    if conversation:
        for user_id in user_ids:
            user = User.objects(id=ObjectId(user_id)).first()
            if user:
                existing_conversation_ids = [str(conv.id) for conv in user.conversations]
                if not str(conversation_id) in existing_conversation_ids:
                    user.conversations.append(conversation)
                    user.save()

def add_users_to_conversation(conversation_id: str, user_ids: List[str]):
    conversation = Conversation.objects(id=ObjectId(conversation_id)).first()
    existing_user_ids = [str(u.id) for u in conversation.members]
    if conversation:
        for user_id in user_ids:
            user = User.objects(id=ObjectId(user_id)).first()
            if user and not str(user.id) in existing_user_ids:
                conversation.members.append(user)
                conversation.save()