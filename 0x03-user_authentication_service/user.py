#!/usr/bin/env python3
"""Defines a Sqlalchemy model for a user database table."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    A class representing a user in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (int): Primary key identifying each user uniquely.
        email (str): Email address of the user.
        hashed_password (str): Hashed password for user authentication.

        session_id (str, optional): Unique session ID for
        user session management.

        reset_token (str, optional): Token used for
        password reset functionality.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
