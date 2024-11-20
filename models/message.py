import mongoengine
from datetime import datetime


class Message(mongoengine.Document):
    conversation_id = mongoengine.ReferenceField('Conversation', required=True)
    sender_id = mongoengine.ReferenceField('User', required=True)
    body = mongoengine.StringField(required=True)
    message_type = mongoengine.StringField(choices=("text", "image", "audio", "video", "link"),
                                           default="text", required=True)  # Fixed typo
    emotion_flag = mongoengine.StringField(default=None)
    created_at = mongoengine.DateTimeField(default=datetime.now)
    modified_at = mongoengine.DateTimeField(default=None)
    deleted_at = mongoengine.DateTimeField(default=None)

    meta = {
        'db_alias': 'core',
        'collection': 'Messages'
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "conversationId": str(self.conversation_id.id),
            "senderId": str(self.sender_id.id),
            "body": self.body,
            "messageType": self.message_type,
            "emotionFlag": self.emotion_flag if self.emotion_flag else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "modifiedAt": self.modified_at.isoformat() if self.modified_at else None,
            "deletedAt": self.deleted_at.isoformat() if self.deleted_at else None
        }
