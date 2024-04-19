#!/usr/bin/env python3
"""creating a session authentication module"""

# Import necessary modules
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


# Define the SessionAuth class
class SessionAuth(Auth):
    """SessionAuth class
    This class provides methods for session authentication.
    """

    # Dictionary to store user IDs mapped to session IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session
        This method generates a new session ID and
        associates it with the provided user ID.
        """
        # Check if user_id is valid
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = uuid4()

        # Store the user ID with the session ID in the dictionary
        self.user_id_by_session_id[str(session_id)] = user_id

        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id
        This method returns the user ID associated
        with the provided session ID.
        """
        # Check if session_id is valid
        if session_id is None or not isinstance(session_id, str):
            return None

        # Return the user ID associated with the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a user instance
        This method returns the User instance associated
        with the current session.
        """
        # Get the session ID from the session cookie in the request
        session_id = self.session_cookie(request)
        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        # Return the User instance corresponding to the user ID
        return User.get(user_id)
