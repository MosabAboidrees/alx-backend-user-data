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
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def _generate_uuid() -> str:
    """Summary
    Raises:
        ValueError: description
    Returns:
        str: description
    """
    id = uuid4()
    return str(id)


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
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
            self._db.find_user_by(email=email)
        except NoResultFound:

        # Add user to database
            return self._db.add_user(email, _hash_password(password))
        else:
            # if user already exists, throw error
            raise ValueError('User {} already exists'.format(email))
