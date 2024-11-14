#!/usr/bin/env python3
"""
Route module for the API
This module initializes the Flask app and sets up routes,
error handlers, and authentication for the API.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)  # Register blueprint for API views
# Enable CORS for the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None  # Placeholder for authentication handler

# Determine authentication type based on environment variable
AUTH_TYPE = os.getenv("AUTH_TYPE")

# Load appropriate authentication class based on AUTH_TYPE
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()  # Use session authentication with expiration
elif AUTH_TYPE == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    # Use session authentication stored in the database
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Function executed before each request.
    Sets the current user for the request if authentication is enabled,
    and aborts with appropriate error codes if access is unauthorized
    or forbidden. If `auth` is not set, all requests pass through
    without authentication checks.
    """
    if auth is None:
        # No authentication configured, so skip checks
        pass
    else:
        # Set current user in request object for use in API views
        setattr(request, "current_user", auth.current_user(request))

        # Define routes that do not require authentication
        excluded_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/',
                         '/api/v1/forbidden/',
                         '/api/v1/auth_session/login/']

        # Check if the request path requires authentication
        if auth.require_auth(request.path, excluded_list):
            cookie = auth.session_cookie(request)
            # Abort with 401 if neither header nor session cookie is present
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            # Abort with 403 if current user could not be authenticated
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Error handler for 404 Not Found.
    Args:
        error: The error object (typically unused).
    Returns:
        JSON response with a 404 status code and an error message.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Error handler for 401 Unauthorized.
    Args:
        error: The error object (typically unused).
    Returns:
        JSON response with a 401 status code and an error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Error handler for 403 Forbidden.
    Args:
        error: The error object (typically unused).
    Returns:
        JSON response with a 403 status code and an error message.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    # Retrieve host and port from environment variables,
    # with defaults if not set
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Start the Flask application
    app.run(host=host, port=port)
