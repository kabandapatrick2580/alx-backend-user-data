#!/usr/bin/env python3
"""Module for basic authentication"""

from api.v1.auth.auth import Auth  # Importing the Auth class
from typing import TypeVar  # Importing TypeVar for type annotations
import base64  # Importing base64 module for encoding/decoding
from models.user import User  # Importing the User model
from flask import request  # Importing Flask's request module for handling requests


class BasicAuth(Auth):
    """Basic authentication class inheriting from Auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the Authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        header_parts = authorization_header.split(' ')
        return header_parts[1] if header_parts[0] == 'Basic' else None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string

        Args:
            base64_authorization_header (str): The Base64 string

        Returns:
            str: The decoded value of the Base64 string
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('utf-8')
            return message
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from a decoded Base64 string

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string

        Returns:
            tuple: A tuple containing user email and password
        """
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str) \
           or ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1]) if credentials else (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password

        Args:
            user_email (str): The user's email
            user_pwd (str): The user's password

        Returns:
            User: The User instance if found, else None
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request

        Args:
            request (object): The Flask request object (default None)

        Returns:
            User: The User instance if found, else None
        """
        try:
            header = self.authorization_header(request)
            base64_header = self.extract_base64_authorization_header(header)
            decoded_header = self.decode_base64_authorization_header(base64_header)
            user_credentials = self.extract_user_credentials(decoded_header)
            return self.user_object_from_credentials(user_credentials[0], user_credentials[1])
        except Exception:
            return None
