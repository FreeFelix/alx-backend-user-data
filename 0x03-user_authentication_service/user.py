#!/usr/bin/env python3
"""User module defining the User model.

This module defines the User class which represents the users table in the database.

Modules:
    sqlalchemy.ext.declarative: Tools for declarative class definitions.
    sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    """
    User class representing a user in the database.

    Attributes:
        id (int): The user's ID, primary key.
        email (str): The user's email address.
        hashed_password (str): The user's hashed password.
        session_id (str, optional): The user's session ID.
        reset_token (str, optional): The user's reset token for password recovery.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the user.
        """
        return f"User(id={self.id}, email={self.email})"
