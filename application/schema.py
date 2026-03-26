"""
schema.py

This module defines the database schema for the Project Workflow Manager Application.

It contains SQL statements used to create database tables if they do not already exist.
These ensure the required database structure exists before database interaction.

Additional table definitions will be added with future entity creation.
"""

USER_TABLE = """
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
"""
