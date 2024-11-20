from crypt import methods
from typing import List

from bson import ObjectId, DBRef
from flask import jsonify

from models.conversation import Conversation
from models.user import User
from services.conversation import add_conversation_to_users, add_users_to_conversation


def create_private_conversation(users: List[str]):
    new_conversation = Conversation(members=users, admins=users)
    new_conversation.save()
    add_conversation_to_users(str(new_conversation.id), users)
    add_users_to_conversation(str(new_conversation.id), users)
    print(new_conversation.to_dict())
    new_conversation.save()
    return {
        'message': 'conversation created successfully'
    }, 200

def get_conversations_with_user_id(user_id: str):
    try:
        user = User.objects(id=ObjectId(user_id)).first()
        conversations: List[Conversation] = []
        if user:
            print(f"{user.to_dict()}")
            convs = user.conversations
            print(f"convs: {convs}")
            conv_ids = [str(ref.id) for ref in convs]
            print(f"conv_ids: {conv_ids}")
            for conv_id in conv_ids:
                conv = Conversation.objects(id=ObjectId(conv_id)).first()
                print(f"conv: {conv}")
                if conv:
                    conversations.append(conv.to_dict())
                print(f"conv_id: {conv_id}, conv: {conv.to_dict()}")
            return {
                'message': 'conversations found',
                'data': conversations
            }, 200
    except Exception as e:
        print(e)
        return {
            "message": f'{e}',
            "data": None
        }, 403


def get_conversation_by_id(conversation_id: str):
    conversation = Conversation.objects(id=ObjectId(conversation_id)).first()

    if conversation:
        return {
            "message": "conversation found",
            "data": conversation.to_dict()
        }, 200
    else:
        return {
            "message": "conversation not found",
            "data": None
        }, 403