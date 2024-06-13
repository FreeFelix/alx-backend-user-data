#!/usr/bin/env python3
"""Flask application for user authentication and management.

This module defines a Flask web application that provides endpoints for user registration,
login, logout, profile retrieval, and password reset functionality.

Modules:
    auth (Auth): A custom authentication module for managing user authentication.

Functions:
    welcome(): Handles GET requests to the root URL, returning a welcome message.
    user(): Handles POST requests to /users for user registration.
    login(): Handles POST requests to /sessions for user login.
    logout(): Handles DELETE requests to /sessions for user logout.
    profile(): Handles GET requests to /profile for retrieving user profile information.
    get_reset_password_token(): Handles POST requests to /reset_password for generating a
    password reset token.
    update_password(): Handles PUT requests to /reset_password for updating the user's password.
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Handles GET requests to the root URL.

    Returns:
        str: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"}), 200

@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """Handles POST requests to /users for user registration.

    Returns:
        str: JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handles POST requests to /sessions for user login.

    Returns:
        str: JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response, 200
    else:
        abort(401)

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Handles DELETE requests to /sessions for user logout.

    Returns:
        str: Redirects to the root URL or returns an error message.
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Handles GET requests to /profile for retrieving user profile information.

    Returns:
        str: JSON response with the user's email or an error message.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Handles POST requests to /reset_password for generating a password reset token.

    Returns:
        str: JSON response with the email and reset token or an error message.
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200

@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Handles PUT requests to /reset_password for updating the user's password.

    Returns:
        str: JSON response with a success message or an error message.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}", "message": "Password updated"}), 200
    except Exception:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
