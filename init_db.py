#!/usr/bin/env python3
"""
Database initialization script for Render deployment.
Run this script to initialize/create database tables before starting the app.
"""
import os
import sys

# Import database module to trigger init_db()
from database import init_db, USE_POSTGRES

def main():
    print(f"Database type: {'PostgreSQL' if USE_POSTGRES else 'SQLite'}")

    if not USE_POSTGRES:
        print("Warning: DATABASE_URL not set, using SQLite.")
        print("This script is intended for PostgreSQL initialization on Render.")

    print("Initializing database tables...")
    try:
        init_db()
        print("Database initialization completed successfully!")
        return 0
    except Exception as e:
        print(f"Error during initialization: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
