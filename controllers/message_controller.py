from bson import ObjectId
from flask import jsonify

from models.conversation import Conversation
from models.message import Message
from models.user import User


def send_message(sender_id: str, conversation_id: str, content: str, message_type: str):
    conversation = Conversation.objects(id=ObjectId(conversation_id)).first()

    print(f"content = {content}")
    if conversation:
        new_message = Message(sender_id=sender_id, conversation_id= conversation_id, body=content, message_type=message_type)
        new_message.save()
        conversation.messages.append(new_message)
        conversation.last_message = content
        conversation.save()
        return {
            "message": "message sent"
        }, 200

    return {
        "message": "conversation does not exist"
    }, 403

def get_messages_of_conversation(user_id: str, conversation_id: str):
    user = User.objects(id=ObjectId(user_id)).first()
    conversation = Conversation.objects(id=ObjectId(conversation_id)).first()
    if user and conversation:
        print(conversation.messages)
        messages = []
        for msg_id in conversation.messages:
            print(str(msg_id))
            msg = Message.objects(id=ObjectId(str(msg_id.id))).first()
            if msg:
                messages.append(msg.to_dict())
        return {
            "message": "Ok",
            "data": messages
        }, 200
    return {
        "message": "Can't get messages",
        "data": None
    }, 403