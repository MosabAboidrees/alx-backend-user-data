#!/usr/bin/env python3
"""
Auth module
This module contains helper functions for password hashing
"""

import bcrypt


def _hash_password(password: str) -> bytes:
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


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Type[User]:
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
            raise ValueError(f"User {email} already exists")
        except Exception as e:
            # Continue if no user is found
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Create and save the user
        user = self._db.add_user(email, hashed_password.decode('utf-8'))
        return user
