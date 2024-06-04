#!/usr/bin/env python3
"""
Provides functions for encrypting passwords using bcrypt.

This module contains functions for generating a salted hash of a password
and checking if a given password matches a hashed password.

Example:
    hashed_password = hash_password("password123")
    is_valid = is_valid(hashed_password, "password123")
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a salted hash of the given password.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if the given password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
