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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        Find a user by arbitrary keyword arguments.
        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.
        Returns:
            User: The first user found matching the criteria.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query parameters are invalid.
        """
        try:
            # Query the first user matching the criteria
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except AttributeError as e:
            raise InvalidRequestError from e
