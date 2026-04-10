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

PROJECT_TABLE = """
CREATE TABLE IF NOT EXISTS Projects (
    projID INTEGER PRIMARY KEY AUTOINCREMENT,
    projTitle TEXT NOT NULL UNIQUE,
    projDueDate TEXT NOT NULL,
    projManagerID INTEGER NOT NULL,
    projDescription TEXT,
    FOREIGN KEY (projManagerID) REFERENCES Users(id)
);
"""

PHASE_TABLE = """
CREATE TABLE IF NOT EXISTS Phases (
    phaseID INTEGER PRIMARY KEY AUTOINCREMENT,
    projID INTEGER NOT NULL,
    phaseTitle TEXT NOT NULL,
    phaseDueDate TEXT NOT NULL,
    phaseDescription TEXT,
    FOREIGN KEY (projID) REFERENCES Projects(projID),
    UNIQUE (projID, phaseTitle)
);
"""