#!/usr/bin/env python3
"""
This script creates a new user with a basic authentication setup.
"""

import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User


def create_user(email: str, clear_password: str) -> User:
    """
    Creates a new user with the provided email and password.

    Args:
        email (str): The user's email address.
        clear_password (str): The user's cleartext password.

    Returns:
        User: The newly created user object.
    """

    user = User()
    user.email = email
    user.password = clear_password
    print(f"New user: {user.id}")
    user.save()
    return user


if __name__ == "__main__":
    user_email = "bob@hbtn.io"
    user_clear_pwd = "H0lbertonSchool98!"

    user = create_user(user_email, user_clear_pwd)

    basic_clear = f"{user_email}:{user_clear_pwd}"
    basic_encoded = base64.b64encode(
        basic_clear.encode('utf-8')).decode("utf-8")
    print(f"Basic Base64: {basic_encoded}")
