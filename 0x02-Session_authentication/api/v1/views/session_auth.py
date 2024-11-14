#!/usr/bin/env python3
""" Module of User views
This module defines routes for user authentication,
specifically login and logout functionality using session authentication.
"""

import os
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def session_auth():
    """
    POST /api/v1/auth_session/login
    Authenticates a user using email and password, then creates a session.
    Request form data:
      - email (str): User's email (required)
      - password (str): User's password (required)
    Returns:
      - JSON representation of the User object if authenticated successfully,
        with a session cookie set.
      - 400 if email or password is missing.
      - 404 if no user is found with the provided email.
      - 401 if the password is incorrect.
    """
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is provided
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    # Check if password is provided
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({"email": email})
    if not users or users == []:
        # Return 404 if no user found with this email
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password matches for any user with this email
    for user in users:
        if user.is_valid_password(password):
            # Import the auth instance for session management
            from api.v1.app import auth
            # Create session ID for authenticated user
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())  # JSON response with user data
            # Retrieve session name from environment
            session_name = os.getenv('SESSION_NAME')
            # Set session cookie in response
            resp.set_cookie(session_name, session_id)
            return resp

    # Return 401 if password is incorrect
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Logs out the authenticated user by destroying their session.
    Returns:
      - Empty JSON response with 200 status on successful logout.
      - 404 if the session could not be destroyed.
    """
    # Import the auth instance for session management
    from api.v1.app import auth

    # Attempt to destroy the current session
    if auth.destroy_session(request):
        return jsonify({}), 200  # Return empty JSON on successful logout

    # Return 404 if session destruction fails
    abort(404)
