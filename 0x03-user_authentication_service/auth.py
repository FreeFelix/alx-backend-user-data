#!/usr/bin/env python3
"""Authentication module for managing user authentication and sessions.

This module defines the Auth class and helper functions for password hashing,
UUID generation, and interaction with the user authentication database.

Modules:
    db (DB): A custom database module for managing user data.
    user (User): A user model representing the users in the database.
    bcrypt: A library for hashing passwords.
    uuid4: A function for generating UUIDs.
    sqlalchemy.orm.exc.NoResultFound: An exception for handling no result found errors in SQLAlchemy.

Functions:
    _hash_password(password: str) -> str: Hashes a password using bcrypt.
    _generate_uuid() -> str: Generates a UUID string.
"""

from db import DB
from typing import TypeVar
from user import User
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def _generate_uuid() -> str:
    """
    Generates a UUID string.

    Returns:
        str: The generated UUID.
    """
    return str(uuid4())

class Auth:
    """
    Auth class to interact with the authentication database.

    Methods:
        register_user(email: str, password: str) -> User:
            Registers a new user with the given email and password.
        valid_login(email: str, password: str) -> bool:
            Validates the login credentials of a user.
        create_session(email: str) -> str:
            Creates a session for a user and returns the session ID.
        get_user_from_session_id(session_id: str) -> str:
            Retrieves the user email associated with the given session ID.
        destroy_session(user_id: int) -> None:
            Destroys the session associated with the given user ID.
        get_reset_password_token(email: str) -> str:
            Generates a password reset token for a user.
        update_password(reset_token: str, password: str) -> None:
            Updates the user's password using the given reset token.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User: The registered user.

        Raises:
            ValueError: If the user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials of a user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))

    def create_session(self, email: str) -> str:
        """
        Creates a session for a user and returns the session ID.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Retrieves the user email associated with the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The email of the user associated with the session ID, or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session associated with the given user ID.

        Args:
            user_id (int): The ID of the user whose session should be destroyed.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If no user with the given email is found.
        """
       email = request.form.get('email')
    if not email:
        abort(400, description="Email is required")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the user's password using the given reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id, hashed_password=_hash_password(password), reset_token=None)
        except NoResultFound:
            raise ValueError
