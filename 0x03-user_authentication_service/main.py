#!/usr/bin/env python3
"""Main Module."""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.

    Args:
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Returns:
        None
    """
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
        )
    assert (
        response.status_code == 200,
        f"Failed to register user: {response.text}"
    )


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.

    Args:
        email (str): The email of the user attempting to log in.
        password (str): The wrong password of the user attempting to log in.

    Returns:
        None
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
        )
    assert (
        response.status_code == 401,
        "Expected status code 401 for wrong password"
    )


def log_in(email: str, password: str) -> str:
    """
    Log in a user.

    Args:
        email (str): The email of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        str: The email of the logged-in user.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
        )
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    return response.json()["email"]


def profile_unlogged() -> None:
    """
    Access user profile without logging in.

    Returns:
        None
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert (
        response.status_code == 403,
        "Expected status code 403 for unlogged profile access"
    )


def profile_logged(session_id: str) -> None:
    """
    Access user profile after logging in.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None
    """
    response = requests.get(
        f"{BASE_URL}/profile",
        cookies={"session_id": session_id}
        )
    assert (
        response.status_code == 200,
        f"Failed to access profile: {response.text}"
    )


def log_out(session_id: str) -> None:
    """
    Log out a user.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None
    """
    response = requests.delete(
        f"{BASE_URL}/sessions",
        cookies={"session_id": session_id}
        )
    assert (
        response.status_code == 200,
        f"Failed to log out: {response.text}"
    )


def reset_password_token(email: str) -> str:
    """
    Get a reset password token for a user.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset password token.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
        )
    assert (
        response.status_code == 200,
        f"Failed to get reset password token: {response.text}"
    )
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update a user's password using a reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset password token.
        new_password (str): The new password for the user.

    Returns:
        None
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email,
              "reset_token": reset_token,
              "new_password": new_password}
              )
    assert (
        response.status_code == 200,
        f"Failed to update password: {response.text}"
    )


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    # Testing the authentication flow
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
