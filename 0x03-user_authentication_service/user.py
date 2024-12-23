#!/usr/bin/env python3
"""
User model for a user authentication service.
This module defines the User class as a SQLAlchemy model
for a database table named users.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User class representing the users table in the database.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        email (str): User's email address, non-nullable.
        hashed_password (str): User's hashed password, non-nullable.
        session_id (str): Session ID for user, nullable.
        reset_token (str): Reset token for user, nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
