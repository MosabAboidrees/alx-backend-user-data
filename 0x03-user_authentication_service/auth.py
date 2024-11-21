#!/usr/bin/env python3
"""
Auth module
This module contains helper functions for password hashing
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


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
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a session for a user and return the session ID.
        Args:
            email (str): The email of the user to create a session for.
        Returns:
            Optional[str]: The session ID if the user exists, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve a user from the database based on the session ID.
        Args:
            session_id (Optional[str]): The session ID of the user.
        Returns:
            Optional[User]: The user object if the session ID is valid,
            None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session in the database based on the user ID.
        Args:
            user_id (int): The user ID of the session to destroy
        """
        try:
            # Find the user by ID
            user = self._db.find_user_by(id=user_id)
            # Set the session_id to None
            self._db.update_user(user.id, session_id=None)
        except Exception:
            # If no user is found or an error occurs, safely return
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user.
        Args:
            email (str): The email of the user requesting a password reset.
        Returns:
            str: The reset password token.
        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError(f"User with email {email} does not exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using a reset token.
        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to set.
        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password)
        self._db.update_user(user.id, reset_token=None)
        return None
