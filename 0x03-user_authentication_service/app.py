#!/usr/bin/env python3
"""Defines a Flask application for user authentication."""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)  # Create a Flask application instance
AUTH = Auth()  # Initialize Auth class for user authentication


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Handle GET requests to the root URL ("/")."""
    # Return a welcome message
    return jsonify({"message": "Welcome"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Handle POST requests to /users to register a new user."""
    try:
        # Extract email from form data
        email = request.form.get("email")
        # Extract password from form data
        password = request.form.get("password")
        # Register the user
        user = AUTH.register_user(email, password)
        # Return user creation message
        return jsonify({"email": email, "message": "User created"})
    except ValueError as e:
        # Return error message for existing email
        return jsonify({"message": "Email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Handle POST requests to /sessions to log in a user."""
    email = request.form.get("email")  # Extract email from form data
    password = request.form.get("password")  # Extract password from form data
    # Check if login credentials are valid
    if AUTH.valid_login(email, password):
        # Create a session for the user
        session_id = AUTH.create_session(email)
        if session_id:
            response = make_response(jsonify({"email": email,
                                              "message": "Logged in"}))
            # Set session ID as a cookie in the response
            response.set_cookie("session_id", session_id)
            return response
        else:
            # Return error message if session creation fails
            return jsonify({"message": "Unable to create session"}), 500
    else:
        # Return a 401 Unauthorized error if login credentials are invalid
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Handle DELETE requests to /sessions to log out a user."""
    # Get session ID from cookie
    session_id = request.cookies.get("session_id")
    # Find user with the given session ID
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # Destroy the session for the user
        AUTH.destroy_session(user.id)
        # Redirect user to the root URL
        return redirect("/")
    else:
        # Return a 403 Forbidden error if session
        # ID is invalid or user does not exist
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Handle GET requests to /profile to retrieve user profile information."""
    # Get session ID from cookie
    session_id = request.cookies.get("session_id")
    # Find user with the given session ID
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # Return user's email and 200 HTTP status if user exists
        return jsonify({"email": user.email}), 200
    else:
        # Return a 403 Forbidden error if session ID is invalid or
        # user does not exist
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password():
    """Handle POST requests to /reset_password to
    generate a reset password token.
    """
    email = request.form.get("email")  # Extract email from form data
    try:
        # Generate a reset password token for the user
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # Return a 403 Forbidden error if no user is found with the given email
        abort(403)
    # Return user's email and reset token with 200 HTTP status
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    # Start Flask application on port 5000
    app.run(host="0.0.0.0", port=5000)
