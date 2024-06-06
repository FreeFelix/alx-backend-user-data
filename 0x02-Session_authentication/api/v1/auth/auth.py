#!/usr/bin/env python3
"""
Auth class
"""

from tabnanny import check
from flask import request
from typing import TypeVar, List
from os import getenv
User = TypeVar('User')

class Auth:
    """
    Auth class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication.
        
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.
        
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.
        
        Args:
            request: The request object.
        
        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.
        
        Args:
            request: The request object.
        
        Returns:
            User: The user associated with the request, or None if not found.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.
        
        Args:
            request: The request object.
        
        Returns:
            str: The value of the session cookie, or None if not present.
        """
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookies.get(session_name, None)
