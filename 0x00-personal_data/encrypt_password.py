#!/usr/bin/env python3
"""
Module for password encryption and validation.
"""

import bcrypt


def hash_password(password: str) -> ByteString:
    """
    Hash a password with a salt using bcrypt.
    Args:
        password (str): The password to hash.
    Returns:
        ByteString: The hashed password as a byte string.
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


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
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
