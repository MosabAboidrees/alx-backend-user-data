#!/usr/bin/env python3
"""
Basic Flask app
This module defines a basic Flask application with a single route.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    Handle GET request to the root route.
    Returns:
        JSON: A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
