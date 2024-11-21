#!/usr/bin/env python3
"""
Auth module
This module contains helper functions for password hashing.
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
