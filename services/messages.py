from datetime import datetime
from typing import List

from flask import jsonify

from models.conversation import Conversation
from models.message import Message
from services.conversation import does_conversation_id_exist
from services.userSearchService import get_user_by_id, does_user_id_exist

def does_message_id_exist(msg_id: str) -> bool:
    if Message.objects(id=msg_id).first():
        return True
    else:
        return False

def create_message(conversation_id, sender_id, body, message_type="text", emotion_flag=None):
    if not does_user_id_exist(sender_id):
        return jsonify({"error": "sender does not exist"}), 403

    if not does_conversation_id_exist(conversation_id):
        return jsonify({"error": "Conversation does not exist"}), 403

    try:
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            body=body,
            message_type=message_type,
            emotion_flag=emotion_flag,
            created_at=datetime.now,
            modified_at=None,  # Assuming modified_at is set to None initially
            deleted_at=None    # Assuming deleted_at is set to None initially
        )
    except Exception as e:
        return jsonify({"error": e})
    message.save()
    print(f"Message created: {body}")
    return jsonify({"message": "Message created successfully"}), 200

def get_message_by_id(msg_id: str) -> Message|None:
    return Message.objects.get(id=msg_id).first()

def get_message_by_conversation_id(conv_id: str) -> List[Message]:
    return Message.objects(conversation_id=conv_id).first()