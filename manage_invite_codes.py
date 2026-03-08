#!/usr/bin/env python3
"""
Invite Code Management Script
Generate, add, and manage invite codes.
"""
import os
import sys
import csv
import secrets
from pathlib import Path
from datetime import datetime

# Import database module
from database import get_db, USE_POSTGRES

INVITE_CODES_FILE = Path("invite_codes.csv")


def generate_invite_code():
    """Generate a unique invite code."""
    return f"INV-{secrets.token_hex(4).upper()}"


def load_codes_from_csv():
    """Load all codes from CSV file."""
    if not INVITE_CODES_FILE.exists():
        return [], []

    codes = []
    used_codes = []
    try:
        with open(INVITE_CODES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['code'].strip()
                codes.append(code)
                if row.get('status') == 'used' or row.get('is_used') == '1':
                    used_codes.append(code)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return [], []

    return codes, used_codes


def save_codes_to_csv(codes_with_status):
    """Save codes to CSV file."""
    with open(INVITE_CODES_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['code', 'created_by', 'status', 'used_at'])
        for code_data in codes_with_status:
            writer.writerow(code_data)


def list_codes(show_used=False):
    """List all invite codes."""
    codes, used_codes = load_codes_from_csv()

    print(f"\n{'='*60}")
    print(f"Invite Codes Summary")
    print(f"{'='*60}")
    print(f"Total codes: {len(codes)}")
    print(f"Used codes: {len(used_codes)}")
    print(f"Available codes: {len(codes) - len(used_codes)}")
    print(f"{'='*60}\n")

    if show_used:
        print(f"{'Code':<20} {'Status':<10}")
        print("-" * 30)
        for code in codes:
            status = "USED" if code in used_codes else "AVAILABLE"
            print(f"{code:<20} {status:<10}")
    else:
        available = [c for c in codes if c not in used_codes]
        print(f"Available Codes ({len(available)}):")
        print("-" * 30)
        for code in available:
            print(code)
    print()


def generate_codes(count=10):
    """Generate new invite codes and add to CSV."""
    codes, used_codes = load_codes_from_csv()
    existing_codes = set(codes)

    new_codes = []
    for _ in range(count):
        while True:
            code = generate_invite_code()
            if code not in existing_codes:
                existing_codes.add(code)
                new_codes.append(code)
                break

    # Append to CSV
    file_exists = INVITE_CODES_FILE.exists()
    with open(INVITE_CODES_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['code', 'created_by', 'status', 'used_at'])
        for code in new_codes:
            writer.writerow([code, 'generated', 'available', ''])

    print(f"Generated {len(new_codes)} new invite codes:")
    for code in new_codes:
        print(f"  {code}")
    print()

    return new_codes


def sync_to_database():
    """Sync invite codes from CSV to database."""
    codes, _ = load_codes_from_csv()

    if not codes:
        print("No codes to sync!")
        return

    print(f"Syncing {len(codes)} invite codes to database...")

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("SELECT code, is_used FROM invite_codes")
            db_codes = {row[0]: row[1] for row in cursor.fetchall()}

            inserted = 0
            for code in codes:
                if code not in db_codes:
                    cursor.execute("""
                        INSERT INTO invite_codes (code, created_by, is_used)
                        VALUES (%s, %s, FALSE)
                        ON CONFLICT (code) DO NOTHING
                    """, (code, 'csv_import'))
                    inserted += 1

            db.commit()
            cursor.close()
        else:
            db_codes = {row['code']: row['is_used'] for row in db.execute("SELECT code, is_used FROM invite_codes").fetchall()}

            inserted = 0
            for code in codes:
                if code not in db_codes:
                    db.execute("""
                        INSERT OR IGNORE INTO invite_codes (code, created_by, is_used)
                        VALUES (?, ?, 0)
                    """, (code, 'csv_import'))
                    inserted += 1

            db.commit()

        print(f"Synced {inserted} new codes to database.")
        print(f"Database now has {len(db_codes) + inserted} invite codes.\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_invite_codes.py <command> [options]")
        print("\nCommands:")
        print("  list [--used]       - List all invite codes")
        print("  generate [count]    - Generate new invite codes (default: 10)")
        print("  sync                - Sync CSV codes to database")
        print("  stats               - Show statistics")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        show_used = "--used" in sys.argv
        list_codes(show_used)

    elif command == "generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        generate_codes(count)

    elif command == "sync":
        sync_to_database()

    elif command == "stats":
        codes, used_codes = load_codes_from_csv()
        print(f"\nTotal: {len(codes)} | Used: {len(used_codes)} | Available: {len(codes) - len(used_codes)}\n")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
