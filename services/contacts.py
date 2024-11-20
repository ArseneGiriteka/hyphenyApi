from bson import ObjectId

from models.user import User


def add_to_pending_contact(user_id: str, target_id: str):
    User.objects(id=ObjectId(user_id)).update_one(add_to_set__contacts__pending=target_id)

def remove_contact_from_pending(user_id: str, target_id: str):
    user = User.objects(id=ObjectId(user_id)).first()
    if user:
        # Remove target_id from contacts['asked'] if it exists
        if target_id in user.contacts.get('pending', []):
            user.contacts['pending'].remove(target_id)
            user.save()

def add_to_asked_contact(user_id: str, target_id: str):
    User.objects(id=ObjectId(user_id)).update_one(add_to_set__contacts__asked=target_id)

def remove_contact_from_asked(user_id: str, target_id: str):
    user = User.objects(id=ObjectId(user_id)).first()
    if user:
        if target_id in user.contacts.get('asked', []):
            user.contacts['asked'].remove(target_id)
            user.save()


def add_to_accepted_contact(user_id: str, target_id: str):
    User.objects(id=ObjectId(user_id)).update_one(add_to_set__contacts__accepted=target_id)

def remove_contact_from_accepted(user_id: str, target_id: str):
    user = User.objects(id=ObjectId(user_id)).first()
    if user:
        if target_id in user.contacts.get('accepted', []):
            user.contacts['accepted'].remove(target_id)
            user.save()

def add_to_blocked_contact(user_id: str, target_user: str):
    User.objects(id=ObjectId(user_id)).update_one(add_to_set__contacts__blocked=target_user)

def remove_contact_from_blocked(user_id: str, target_id: str):
    user = User.objects(id=ObjectId(user_id)).first()
    if user:
        # Remove target_id from contacts['asked'] if it exists
        if target_id in user.contacts.get('blocked', []):
            user.contacts['blocked'].remove(target_id)
            user.save()




def get_pending_contacts(user_id: str):
    user = User.objects.get(id=ObjectId(user_id))
    pending_contacts = user.contacts.get("pending", [])
    return [item for item in User.objects(id__in=pending_contacts)]