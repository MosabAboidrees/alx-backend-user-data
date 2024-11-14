#!/usr/bin/env python3
"""
Module for Session Authentication with Expiration
This module defines the SessionExpAuth class,
which adds expiration functionality to session authentication.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth
    and adds session expiration.

    Attributes:
        session_duration (int): Duration of session in seconds.
        Defaults to 0 (no expiration).
    """

    def __init__(self):
        """
        Initialize SessionExpAuth by setting the session_duration attribute.
        If SESSION_DURATION environment variable is set,
        it is used as the session duration.
        If it is not set or invalid, session_duration defaults to 0.
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session with an expiration date for the specified user ID.
        Args:
            user_id (str): ID of the user for whom to create a session.
        Returns:
            str: Session ID if created, or None if session creation fails.
        """
        # Call parent method to get session ID
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session data with user_id and creation time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()  # Record session creation time
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve user ID associated with a session ID,
        taking expiration into account.
        Args:
            session_id (str): Session ID to retrieve the user ID for.
        Returns:
            str: User ID if the session is valid and has not expired,
            otherwise None.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        # Check if session duration is set and handle expiration logic
        if self.session_duration <= 0:
            # No expiration, return user_id directly
            return session_data.get("user_id")

        created_at = session_data.get("created_at")
        if created_at is None:
            return None

        # Calculate expiration time and compare with current time
        if (created_at + timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None  # Session expired, return None

        return session_data.get("user_id")
