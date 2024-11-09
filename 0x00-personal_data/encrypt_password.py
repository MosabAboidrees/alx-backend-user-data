#!/usr/bin/env python3
"""
Module for password encryption and validation.
"""

import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """
    Hash a password with a salt using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        ByteString: The hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: ByteString, password: str) -> bool:
    """
    Validate a password against a hashed password.
    Args:
        hashed_password (ByteString): The hashed password.
        password (str): The password to validate.
    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
