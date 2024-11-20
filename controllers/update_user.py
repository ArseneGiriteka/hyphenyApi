from bson import ObjectId
from werkzeug.security import generate_password_hash

from models.user import User
from services.userSearchService import does_username_exist, does_email_exist


def update_user(user_id: str, username: str, email: str, password: str):
    print(f"user_id: {user_id}")
    print(f"username: {username}")
    print(f"email: {email}")
    print(f"password: {password}")
    user = User.objects(id=ObjectId(user_id)).first()

    if user:
        user.username = username.strip() if username != "" and not does_username_exist(username.strip()) else user.username
        user.email = email.strip() if email != "" and not does_email_exist(email.strip()) else user.email
        if password != "" and not len(password.strip()) < 6:
            user.password = generate_password_hash(password.strip())

        user.save()
        return {
            "message": "ok updated",
            "data": user.to_dict()
        }, 200
    return {
        "message": "failed user_not_found",
        "data": None
    }, 400
