#!/usr/bin/env python3
"""
SessionAuth
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from uuid import uuid4
from models.user import User

class SessionAuth(Auth):
    """
    SessionAuth class for handling session-based authentication.
    """
    # Dictionary to store the mapping of session IDs to user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.
        
        Args:
            user_id (str): The user ID for which to create a session ID.
        
        Returns:
            str: The created session ID, or None if the user_id is invalid.
        """
        if not user_id or type(user_id) != str:
            return
        session_id = str(uuid4())
        # Store the session ID with the associated user ID
        SessionAuth.user_id_by_session_id[user_id] = session_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a session ID.
        
        Args:
            session_id (str): The session ID for which to retrieve the user ID.
        
        Returns:
            str: The user ID associated with the given session ID, or None if invalid.
        """
        if not session_id or type(session_id) != str:
            return
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the session cookie in the request.
        
        Args:
            request: The request object containing the session cookie.
        
        Returns:
            User: The user instance associated with the session ID, or None if not found.
        """
        if request:
            session_cookie = self.session_cookie(request)
            if session_cookie:
                user_id = self.user_id_for_session_id(session_cookie)
                return User.get(user_id)
