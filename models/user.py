import mongoengine
from datetime import datetime



class User(mongoengine.Document):
    username = mongoengine.StringField(required=True, unique=True)
    email = mongoengine.StringField(required=True, unique=True)
    password = mongoengine.StringField(required=True, min_length=6)
    profilePicture = mongoengine.StringField(default=None)
    conversations = mongoengine.ListField(mongoengine.ReferenceField('Conversation'), default=[])
    contacts = mongoengine.DictField(
        default=lambda: {
            'accepted': [],
            'pending': [],
            'blocked': [],
            'asked': [],
        }
    )

    bio = mongoengine.StringField(default=None)
    created_at = mongoengine.DateTimeField(default=datetime.now)
    modified_at = mongoengine.DateTimeField(default=None)
    deleted_at = mongoengine.DateTimeField(default=None)

    meta = {
        'db_alias': 'core',
        'collection': 'Users'
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "profilePicture": self.profilePicture,
            "conversations": [str(conv.id) for conv in self.conversations] if self.conversations else [],
            "contacts": self.contacts,
            "bio": self.bio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "deleted_at": self.deleted_at.isoformart() if self.deleted_at else None
        }
