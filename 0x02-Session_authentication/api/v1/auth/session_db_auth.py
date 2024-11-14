#!/usr/bin/env python3
"""
SessionDBAuth module for session authentication stored in the database.
"""
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing session authentication
    with database storage.
    Inherits from SessionExpAuth to support session expiration.
    """

    def create_session(self, user_id=None):
        """
        Creates a session for a user and stores it in the database.
        Args:
            user_id (str): The ID of the user to create a session for.
        Returns:
            str: The session ID if created successfully, or None otherwise.
        """
        # Create a session ID using the superclass method
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a UserSession object and save it to the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Assuming a save method to persist data

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a session ID.
        Args:
            session_id (str): The session ID to look up.
        Returns:
            str: The user ID if the session is valid, or None otherwise.
        """
        if session_id is None:
            return None

        # Fetch the UserSession object from the database by session_id
        # Assuming find_by is a query method
        user_session = UserSession.find_by(session_id=session_id)
        if user_session is None:
            return None

        # Check for expiration
        if self.session_duration <= 0:
            return user_session.user_id
        # Determine session expiration time
        created_at = user_session.created_at
        duration = timedelta(seconds=self.session_duration)
        if created_at + duration < datetime.now():
            return None  # Session expired, return None

    def destroy_session(self, request=None):
        """
        Destroys a session by deleting
        the associated UserSession from the database.
        Args:
            request (Request): The Flask request object.
        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Find and delete the UserSession by session_id
        user_session = UserSession.find_by(session_id=session_id)
        if user_session is None:
            return False

        # using delete method to remove the record
        user_session.delete()
        return True
