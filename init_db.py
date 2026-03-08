#!/usr/bin/env python3
"""
Database initialization script for Render deployment.
Run this script to initialize/create database tables and import invite codes.
"""
import os
import sys

# Import database module
from database import init_db, USE_POSTGRES, get_all_invite_codes


# Pre-generated invite codes to import (100 codes)
INVITE_CODES_TO_IMPORT = [
    "INV-7B27D1D4", "INV-9E14D1B4", "INV-FF35EDFE", "INV-5F8C913E", "INV-E85E9345",
    "INV-F4E06EEA", "INV-8F5CA6F4", "INV-52EB1924", "INV-CFA2633B", "INV-FD489E26",
    "INV-C9479AA2", "INV-35706BFC", "INV-FDCF145E", "INV-43EE87EF", "INV-6C223B16",
    "INV-A544E8A1", "INV-04357832", "INV-2D3ADE07", "INV-6A1B4B64", "INV-B748E5A5",
    "INV-1A2B3C4D", "INV-5E6F7A8B", "INV-9C0D1E2F", "INV-3A4B5C6D", "INV-7E8F9A0B",
    "INV-1C2D3E4F", "INV-5A6B7C8D", "INV-9E0F1A2B", "INV-3C4D5E6F", "INV-7A8B9C0D",
    "INV-1E2F3A4B", "INV-5C6D7E8F", "INV-9A0B1C2D", "INV-3E4F5A6B", "INV-7C8D9E0F",
    "INV-1A2B3C4E", "INV-5E6F7A8C", "INV-9C0D1E2G", "INV-3A4B5C6E", "INV-7E8F9A0C",
    "INV-1C2D3E4G", "INV-5A6B7C8E", "INV-9E0F1A2C", "INV-3C4D5E6G", "INV-7A8B9C0E",
    "INV-1E2F3A4C", "INV-5C6D7E8G", "INV-9A0B1C2E", "INV-3E4F5A6C", "INV-7C8D9E0G",
    "INV-1A2B3C4F", "INV-5E6F7A8D", "INV-9C0D1E2H", "INV-3A4B5C6F", "INV-7E8F9A0D",
    "INV-1C2D3E4H", "INV-5A6B7C8F", "INV-9E0F1A2D", "INV-3C4D5E6H", "INV-7A8B9C0F",
    "INV-1E2F3A4D", "INV-5C6D7E8H", "INV-9A0B1C2F", "INV-3E4F5A6D", "INV-7C8D9E0H",
    "INV-2B3C4D5E", "INV-6F7A8B9C", "INV-0D1E2F3A", "INV-4B5C6D7E", "INV-8F9A0B1C",
    "INV-2D3E4F5A", "INV-6B7C8D9E", "INV-0F1A2B3C", "INV-4D5E6F7A", "INV-8B9C0D1E",
    "INV-2F3A4B5C", "INV-6D7E8F9A", "INV-0B1C2D3E", "INV-4F5A6B7C", "INV-8D9E0F1A",
    "INV-2A3B4C5D", "INV-6E7F8A9B", "INV-0C1D2E3F", "INV-4A5B6C7D", "INV-8E9F0A1B",
    "INV-2C3D4E5F", "INV-6A7B8C9D", "INV-0E1F2A3B", "INV-4C5D6E7F", "INV-8A9B0C1D",
    "INV-2E3F4A5B", "INV-6C7D8E9F", "INV-0A1B2C3D", "INV-4E5F6A7B", "INV-8C9D0E1F",
    "INV-3B4C5D6E", "INV-7F8A9B0C", "INV-1D2E3F4A", "INV-5B6C7D8E", "INV-9F0A1B2C",
    "INV-3D4E5F6A", "INV-7B8C9D0E", "INV-1F2A3B4C", "INV-5D6E7F8A", "INV-9B0C1D2E",
]


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
                    # PostgreSQL
                    cursor = db.cursor()
                    cursor.execute("""
                        INSERT INTO invite_codes (code, created_by, is_used)
                        VALUES (%s, %s, 0)
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
