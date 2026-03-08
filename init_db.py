#!/usr/bin/env python3
"""
Database initialization script for Render deployment.
Run this script to initialize/create database tables and import invite codes.
"""
import os
import sys
import csv
from pathlib import Path

# Import database module
from database import init_db, USE_POSTGRES, get_all_invite_codes

# Invite codes CSV file
INVITE_CODES_FILE = Path("invite_codes.csv")


def load_invite_codes_from_csv():
    """Load invite codes from CSV file."""
    if not INVITE_CODES_FILE.exists():
        print(f"[WARNING] Invite codes file not found: {INVITE_CODES_FILE}")
        return []

    codes = []
    try:
        with open(INVITE_CODES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codes.append(row['code'].strip())
    except Exception as e:
        print(f"[ERROR] Failed to load invite codes from CSV: {e}")
        return []

    return codes


INVITE_CODES_TO_IMPORT = load_invite_codes_from_csv()


def import_invite_codes_direct():
    """Directly insert invite codes into PostgreSQL/SQLite."""
    from database import get_db, DATABASE_URL

    print(f"Database type: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")
    print(f"Importing {len(INVITE_CODES_TO_IMPORT)} invite codes...")

    with get_db() as db:
        # Get existing codes
        if DATABASE_URL:
            cursor = db.cursor()
            cursor.execute("SELECT code FROM invite_codes")
            existing_codes = {row[0] for row in cursor.fetchall()}
            cursor.close()
        else:
            import sqlite3
            existing_codes = {row['code'] for row in db.execute("SELECT code FROM invite_codes").fetchall()}

        print(f"Existing codes in database: {len(existing_codes)}")

        imported_count = 0
        skipped_count = 0

        for code in INVITE_CODES_TO_IMPORT:
            if code in existing_codes:
                skipped_count += 1
                continue

            try:
                if DATABASE_URL:
                    # PostgreSQL (Neon)
                    cursor = db.cursor()
                    cursor.execute("""
                        INSERT INTO invite_codes (code, created_by, is_used)
                        VALUES (%s, %s, FALSE)
                        ON CONFLICT (code) DO NOTHING
                    """, (code, 'import'))
                    cursor.close()
                else:
                    # SQLite
                    db.execute("""
                        INSERT OR IGNORE INTO invite_codes (code, created_by, is_used)
                        VALUES (?, ?, 0)
                    """, (code, 'import'))

                imported_count += 1
            except Exception as e:
                print(f"  Failed to import {code}: {e}")

        db.commit()

    print(f"Imported: {imported_count}, Skipped (already existed): {skipped_count}")
    return imported_count


def main():
    print("=" * 50)
    print("Database Initialization Script")
    print("=" * 50)

    if not os.getenv("DATABASE_URL"):
        print("WARNING: DATABASE_URL not set! Using SQLite (local file).")
        print("On Render, DATABASE_URL should be automatically set.")

    print("\n1. Creating database tables...")
    try:
        init_db()
        print("   Database tables created successfully!")
    except Exception as e:
        print(f"   ERROR creating tables: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n2. Importing invite codes...")
    try:
        imported = import_invite_codes_direct()
        print(f"   Invite codes import completed! ({imported} new codes)")
    except Exception as e:
        print(f"   ERROR importing invite codes: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 50)
    print("Database initialization completed successfully!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
