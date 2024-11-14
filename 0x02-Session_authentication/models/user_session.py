#!/usr/bin/env python3
"""
UserSession model to store session information in the database.
"""
import os
import json
import uuid
from datetime import datetime
from models.base import Base


class UserSession(Base):
    """
    UserSession model that stores session-related information for users.
    Attributes:
        user_id (str): ID of the user for whom the session is created.
        session_id (str): Unique session ID for the user's session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize UserSession with user_id and session_id.
        Args:
            args (list): Additional positional arguments.
            kwargs (dict): Dictionary with "user_id" and "session_id" keys.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
        # Set creation time to now if not provided
        self.created_at = kwargs.get("created_at", datetime.now())

    def delete(self):
        """
        Delete this session entry from the database (or file-based storage).
        """
        # Implement deletion logic based on how data is stored
        # Example: remove from a file-based storage
        # by loading, filtering, and rewriting data
        # Placeholder example if sessions are stored in a JSON file:
        file_path = 'sessions.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                sessions = json.load(file)

            # Filter out the current session by session_id
            sessions = [
                s for s in sessions if s.get('session_id') != self.session_id]

            # Write back the updated sessions list
            with open(file_path, 'w') as file:
                json.dump(sessions, file)
