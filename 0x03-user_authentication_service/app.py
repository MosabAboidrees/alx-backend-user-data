#!/usr/bin/env python3
"""
Basic Flask app
This module defines a basic Flask application with a single route.
"""

from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
