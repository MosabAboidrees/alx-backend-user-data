#!/usr/bin/env python3
"""
Basic Flask app
This module defines a basic Flask application with a single route.
"""

from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Handle GET request to the root route.
    Returns:
        JSON: A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """
    Handle POST request to register a new user.
    Expects:
        Form data with "email" and "password".
    Returns:
        JSON: A success or error message with the registered email.
    Raises:
        400: If the user is already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Handle POST request to log in a user.
    Expects:
        Form data with "email" and "password".
    Returns:
        JSON: A success message and sets the session ID as a cookie.
    Raises:
        401: If the login information is incorrect.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        # create a new session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Handle DELETE request to log out a user.
    Expects:
        The session ID as a cookie with key "session_id".
    Returns:
        Redirect to GET / if the session is destroyed.
    Raises:
        403: If the session ID is invalid or the user does not exist.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/", code=302)


@app.route("/profile", methods=["GET"])
def profile():
    """
    Handle GET request to retrieve the user's profile.
    Expects:
        The session ID as a cookie with key "session_id".
    Returns:
        JSON: The user's email if the session is valid.
    Raises:
        403: If the session ID is invalid or the user does not exist.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """
    Handle POST request to generate a reset password token.
    Expects:
        Form data with "email".
    Returns:
        JSON: The reset token and the user's email.
    Raises:
        403: If the email is not registered.
    """
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """
    Handle PUT request to update a user's password using a reset token.
    Expects:
        Form data with "email", "reset_token", and "new_password".
    Returns:
        JSON: A success message if the password is updated.
    Raises:
        403: If the reset token is invalid.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
