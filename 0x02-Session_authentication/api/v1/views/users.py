#!/usr/bin/env python3
""" Module of Users views """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/api/v1/users/me', methods=['GET'], strict_slashes=False)
def get_user_me():
    """ Retrieves the authenticated User object """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_dict())


@app_views.route(
    '/api/v1/users/<user_id>',
    methods=['GET'],
    strict_slashes=False)
def get_user(user_id):
    """ Get user by ID or authenticated user if ID is 'me' """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())
