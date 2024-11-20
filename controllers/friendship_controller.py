from pyexpat.errors import messages

from bson import ObjectId

from controllers.conversation_controller import create_private_conversation
from models.user import User
from services.contacts import add_to_asked_contact, add_to_pending_contact, remove_contact_from_asked, \
    remove_contact_from_pending, add_to_accepted_contact
from services.userSearchService import does_user_id_exist


def ask_friendship(user_id: str, target_id: str):
    if not (user_id and target_id):
        return {
            "message": "you must provide users id's",
        }, 403

    if not (does_user_id_exist(user_id) and does_user_id_exist(target_id)):
        return {
            "message": "User provided does not exist"
        }, 404

    add_to_asked_contact(user_id, target_id)
    add_to_pending_contact(target_id, user_id)

    return {
        "message": "friendship added successfully"
    }, 200

def accept_friendship(user_id: str, target_id: str):
    if not (user_id and target_id):
        return {
            "message": "You must provide both user_asked and active_user"
        }, 403

    if not (does_user_id_exist(user_id) and does_user_id_exist(target_id)):
        return {
            "message": "User provided does not exist"
        }, 404

    remove_contact_from_asked(target_id, user_id)
    remove_contact_from_pending(user_id, target_id)

    add_to_accepted_contact(user_id, target_id)
    add_to_accepted_contact(target_id, user_id)

    create_private_conversation([user_id, target_id])

    return {
        "message": "friendship accepted"
    }, 200