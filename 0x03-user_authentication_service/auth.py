#!/usr/bin/env python3
"""Defines methods for password hashing and user authentication."""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.hashpw."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Class for user authentication."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get the user corresponding to the session ID."""
        if session_id is None:
            return None
        else:
            try:
                return self._db.find_user_by(session_id=session_id)
            except NoResultFound:
                return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the user with the given user_id."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate and return a reset password token."""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"No user found with email: {email}")
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update the password of the user corresponding to the reset token."""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("No user found with the given reset token")
        hashed_password = bcrypt.hashpw(new_password.encode(),
                                        bcrypt.gensalt())
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
