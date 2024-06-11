#!/usr/bin/env python3
"""Database module for managing user data.

This module defines the DB class and helper functions for interacting with the
user database using SQLAlchemy.

Modules:
    sqlalchemy: A SQL toolkit and Object-Relational Mapping (ORM) library.
    user (Base, User): Models representing the database schema for users.
    typing: A module that provides runtime support for type hints.

Classes:
    DB: A class for managing the user database, including adding, finding, and updating users.

Functions:
    _session: A property that initializes and returns the database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

class DB:
    """
    DB class for managing the user database.

    Methods:
        add_user(email: str, hashed_password: str) -> User:
            Adds a new user to the database.
        find_user_by(**kwargs) -> User:
            Finds a user in the database by specified criteria.
        update_user(user_id: int, **kwargs) -> None:
            Updates user attributes in the database.
    """

    def __init__(self):
        """
        Initializes the database engine and creates all tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        Initializes and returns the database session.

        Returns:
            Session: The SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object, or None if email or hashed_password is missing.
        """
        if not email or not hashed_password:
            return None
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database by specified criteria.

        Args:
            **kwargs: Arbitrary keyword arguments specifying user attributes.

        Returns:
            User: The found User object.

        Raises:
            InvalidRequestError: If no criteria are specified or invalid fields are provided.
            NoResultFound: If no user is found matching the criteria.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates user attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments specifying user attributes to update.

        Raises:
            ValueError: If any of the provided fields are invalid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in VALID_FIELDS:
                raise ValueError
            setattr(user, k, v)
        session.commit()
