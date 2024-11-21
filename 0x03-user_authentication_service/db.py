#!/usr/bin/env python3
"""
DB module
This module defines the DB class for interacting with the database
and includes methods to add users to the users table.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """
    DB class for database operations.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.
        Creates a new SQLite database and initializes the users table.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        Returns:
            Session: SQLAlchemy session object
            for interacting with the database.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Args:
            email (str): The email of the new user.
            hashed_password (str): The hashed password of the new user.
        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """_summary_

        Returns:
            User: _description_
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user


    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the attributes
                      to update and their new values.
        Returns:
            None: Updates the user and commits changes to the database.
        Raises:
            ValueError: If any argument does not correspond to a user attribute.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist on User")
            setattr(user, key, value)

        self._session.commit()
        return None
