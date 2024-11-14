#!/usr/bin/env python3
""" Module of User views
This module defines routes for managing User resources,
including retrieving, creating, updating, and deleting users.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Retrieves a list of all users in JSON format.

    Return:
      - JSON list of all User objects
    """
    # Retrieve all User objects and convert to JSON format
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Retrieves a specific user based on user_id.

    Path parameter:
      - user_id: The ID of the User to retrieve
    Return:
      - JSON representation of the User object if found
      - 404 error if the User ID doesn't exist
    """
    if user_id is None:
        # Abort with 404 if no user_id is provided
        abort(404)
    if user_id == "me":
        # Return current user's info if "me" is provided as user_id
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    # Fetch the user by ID
    user = User.get(user_id)
    if user is None:
        abort(404)  # Abort with 404 if user not found
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Deletes a specific user based on user_id.

    Path parameter:
      - user_id: The ID of the User to delete
    Return:
      - Empty JSON object if deletion is successful
      - 404 error if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)  # Abort with 404 if no user_id is provided
    # Fetch the user by ID
    user = User.get(user_id)
    if user is None:
        abort(404)  # Abort with 404 if user not found
    # Delete the user
    user.remove()
    return jsonify({}), 200  # Return empty JSON on successful deletion


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    Creates a new user based on provided JSON data.

    JSON body:
      - email: The user's email (required)
      - password: The user's password (required)
      - last_name: The user's last name (optional)
      - first_name: The user's first name (optional)
    Return:
      - JSON representation of the new User object
      - 400 error if creation fails or required fields are missing
    """
    rj = None  # Request JSON object
    error_msg = None  # Error message placeholder

    try:
        # Parse JSON body from request
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"  # JSON is invalid
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"  # Email is required
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"  # Password is required

    if error_msg is None:
        try:
            # Create and save new User object
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201  # Return created user
        except Exception as e:
            # Error during user creation
            error_msg = f"Can't create User: {e}"

    # Return error message if creation failed
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Updates an existing user based on provided user_id and JSON data.
    Path parameter:
      - user_id: The ID of the User to update
    JSON body:
      - last_name: The user's new last name (optional)
      - first_name: The user's new first name (optional)
    Return:
      - JSON representation of the updated User object
      - 404 error if the User ID doesn't exist
      - 400 error if update fails due to bad format
    """
    if user_id is None:
        abort(404)  # Abort with 404 if no user_id is provided
    # Fetch the user by ID
    user = User.get(user_id)
    if user is None:
        abort(404)  # Abort with 404 if user not found

    rj = None  # Request JSON object
    try:
        # Parse JSON body from request
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400  # Invalid JSON format

    # Update fields if provided in the JSON request
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')

    # Save updated user
    user.save()
    return jsonify(user.to_json()), 200  # Return updated user in JSON format
