#!/usr/bin/env python3
"""
Module for authentication
This module provides the `Auth` class with methods
for managing authentication, including authorization checks,
session cookies, and retrieving the authorization header.
"""

from typing import List, TypeVar
from flask import request
import os


class Auth:
    """Authentication class to manage various aspects of user authentication,
    including path access control, header validation, and session management.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.
        Args:
            path (str): The path to check.
            excluded_paths (List[str]):
            List of paths that do not require authentication.
        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        # Exact match with an excluded path
        if path in excluded_paths:
            return False

        # Check for prefix or wildcard matches in excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.
        Args:
            request (Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            str: The Authorization header value if present, otherwise None.
        """
        if request is None:
            return None

        # Retrieve the 'Authorization' header from the request
        header = request.headers.get('Authorization')

        return header if header is not None else None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for retrieving the current authenticated user.
        This method should be overridden in subclasses with
        actual user-fetching logic.
        Args:
            request (Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            TypeVar('User'): Always returns None in this base class.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.
        Args:
            request (Request, optional): The Flask request object.
            Defaults to None.
        Returns:
            str: The session cookie value if present, otherwise None.
        """
        if request is None:
            return None

        # Retrieve session name from environment variables
        session_name = os.getenv('SESSION_NAME')
        # Get session cookie from request by session name
        return request.cookies.get(session_name)
