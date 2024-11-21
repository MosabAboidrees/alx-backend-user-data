#!/usr/bin/env python3
"""
Auth module
This module contains helper functions for password hashing
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFoung
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt's hashpw function.
    Args:
        password (str): The plain text password to hash.
    Returns:
        bytes: A salted hash of the input password.
    """
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """Summary
    Raises:
        ValueError: description
    Returns:
        str: description
    """
    uu_id = uuid4()
    return str(uu_id)


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with an email and password.
        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.
        Returns:
            User: The newly created User object.
        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            # Check if user already exists
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        else:
            # if user already exists, throw error
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user credentials.
        Args:
            email (str): The email of the user to validate.
            password (str): The plain text password of the user.
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()

        if bcrypt.checkpw(encoded_password, user_password):
            return True

        return False
