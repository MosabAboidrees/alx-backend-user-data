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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
