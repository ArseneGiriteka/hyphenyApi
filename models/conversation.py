from email.policy import default

import mongoengine
from datetime import datetime


class Conversation(mongoengine.Document):
    members = mongoengine.ListField(mongoengine.ReferenceField('User'), required=True, max_length=255)
    admins = mongoengine.ListField(mongoengine.ReferenceField('User'), required=True, max_length=10)
    messages = mongoengine.ListField(mongoengine.ReferenceField('Message'), default=[])
    last_message = mongoengine.StringField(default="", required=False)
    title = mongoengine.StringField(required=True, default="New Conversation")
    profilePicture = mongoengine.StringField(default=None)
    created_at = mongoengine.DateTimeField(default=datetime.now)
    modified_at = mongoengine.DateTimeField(default=None)
    deleted_at = mongoengine.DateTimeField(default=None)

    meta = {
        'db_alias': 'core',
        'collection': 'Conversations'
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "members": [str(member_id.id) for member_id in self.members] if self.members else [],
            "admins": [str(admin_id.id) for admin_id in self.admins] if self.admins else [],
            "messages": [str(msg_id.id) for msg_id in self.messages] if self.messages else [],
            "lastMessage": self.last_message if self.last_message and self.last_message != "" else "",
            "title": self.title,
            "profile": self.profilePicture,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }
