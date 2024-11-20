from models.user import User
from werkzeug.security import generate_password_hash

from services.userSearchService import does_username_exist, does_email_exist


def register(username: str, email: str, password: str):
    username = username.strip()
    email = email.strip()
    password = password.strip()

    if does_username_exist(username):
        print("username Already exist")
        return "User Already exist"

    if does_email_exist(email):
        print("email account already exist")
        return "email account already exist"

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    user.save()
    return "user successfully registered"