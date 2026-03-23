"""
Database models and operations for MemorialChat
Supports both SQLite (development) and PostgreSQL (production)
Optimized for Neon PostgreSQL serverless database
"""
import os
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import json
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Detect database type from environment
DATABASE_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg2
else:
    import sqlite3


# Use persistent disk on Render for SQLite
DATABASE_FILE = os.getenv("SQLITE_DB_PATH", "memorial_chat.db")


# ============== Database Connection ==============

@contextmanager
def get_db():
    """Get database connection."""
    if USE_POSTGRES:
        # Parse DATABASE_URL for Neon compatibility
        parsed = urlparse(DATABASE_URL)

        # Extract SSL mode from query params
        query_params = parse_qs(parsed.query)
        ssl_mode = query_params.get('sslmode', ['require'])[0]

        # Build connection with SSL for Neon (psycopg2)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/'),
            user=parsed.username,
            password=parsed.password,
            sslmode=ssl_mode
        )
        try:
            yield conn
        finally:
            conn.close()
    else:
        # Ensure directory exists for SQLite database file
        db_dir = os.path.dirname(DATABASE_FILE)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()


def _row_to_dict(cursor, row, use_postgres: bool) -> Optional[Dict[str, Any]]:
    """Convert database row to dictionary."""
    if row is None:
        return None
    if use_postgres:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    else:
        return dict(row) if row else None


def _get_param_placeholder(idx: int) -> str:
    """Get parameter placeholder for the current database."""
    return "%s" if USE_POSTGRES else "?"


# ============== Schema Definitions ==============

TABLE_SCHEMAS = {
    'users': """
        id {pk} ,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """,
    'profiles': """
        id {pk} ,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        personality TEXT,
        relationship TEXT,
        gender TEXT,
        age TEXT,
        chat_history_text TEXT,
        photo_path TEXT,
        language TEXT DEFAULT 'zh-CN',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    """,
    'chat_messages': """
        id {pk} ,
        user_id INTEGER NOT NULL,
        profile_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        emotional_tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    """,
    'emotional_states': """
        id {pk} ,
        user_id INTEGER NOT NULL,
        profile_id INTEGER NOT NULL,
        mood_index REAL DEFAULT 80.0,
        base_decay_rate REAL DEFAULT 0.03,
        decay_rate REAL DEFAULT 0.03,
        recovery_phase TEXT DEFAULT 'acute',
        phase_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        dominant_stage TEXT DEFAULT 'denial',
        previous_stage TEXT DEFAULT 'denial',
        stage_dwell_count INTEGER DEFAULT 0,
        stage_denial REAL DEFAULT 0.2,
        stage_anger REAL DEFAULT 0.2,
        stage_bargaining REAL DEFAULT 0.2,
        stage_depression REAL DEFAULT 0.2,
        stage_acceptance REAL DEFAULT 0.2,
        stability_score REAL DEFAULT 0.5,
        risk_level REAL DEFAULT 0.0,
        negative_streak INTEGER DEFAULT 0,
        strong_negative_events INTEGER DEFAULT 0,
        total_interactions INTEGER DEFAULT 0,
        memory_intimacy_weight REAL DEFAULT 1.0,
        next_proactive_time TIMESTAMP,
        allow_proactive INTEGER DEFAULT 1,
        last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        -- 新增：连续情绪维度
        valence REAL DEFAULT 0.0,
        arousal REAL DEFAULT 0.5,
        -- 新增：行为指标
        behavior_counts TEXT,  -- JSON 格式存储行为计数
        extracted_keywords TEXT,  -- JSON 格式存储关键词列表
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
        UNIQUE(user_id, profile_id)
    """,
    'emotional_history': """
        id {pk} ,
        user_id INTEGER NOT NULL,
        profile_id INTEGER NOT NULL,
        mood_index REAL,
        dominant_stage TEXT,
        intensity REAL,
        risk_level REAL,
        grief_density REAL,
        text_length INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        -- 新增：连续情绪维度
        valence REAL DEFAULT 0.0,
        arousal REAL DEFAULT 0.5,
        -- 新增：行为指标
        behavior_counts TEXT,
        extracted_keywords TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
    """,
    'user_consents': """
        id {pk} ,
        user_id INTEGER NOT NULL UNIQUE,
        consent_given INTEGER DEFAULT 0,
        consent_timestamp TIMESTAMP,
        consent_version TEXT DEFAULT '1.0',
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    """,
    'user_surveys': """
        id {pk} ,
        user_id INTEGER NOT NULL,
        mood_today INTEGER,
        emotion_intensity INTEGER,
        dual_process_state INTEGER,
        five_stage_state INTEGER,
        companionship_preference INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    """,
    'invite_codes': """
        id {pk} ,
        code TEXT UNIQUE NOT NULL,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        used_by TEXT,
        used_at TIMESTAMP,
        is_used INTEGER DEFAULT 0
    """
}


def init_db():
    """Initialize the database with all tables."""
    tables = list(TABLE_SCHEMAS.keys())

    if USE_POSTGRES:
        with get_db() as db:
            cursor = db.cursor()
            for table in tables:
                schema = TABLE_SCHEMAS[table].format(pk="SERIAL PRIMARY KEY")
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
            db.commit()
            cursor.close()
    else:
        with get_db() as db:
            for table in tables:
                schema = TABLE_SCHEMAS[table].format(pk="INTEGER PRIMARY KEY AUTOINCREMENT")
                db.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
            db.commit()


# ============== Helper Functions ==============

def hash_password(password: str, salt: Optional[str] = None) -> tuple:
    """Hash password with salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return password_hash, salt


def _execute(db, query: str, params: tuple = ()):
    """Execute a query and return cursor/row."""
    if USE_POSTGRES:
        cursor = db.cursor()
        cursor.execute(query, params)
        return cursor
    else:
        return db.execute(query, params)


def _commit(db):
    """Commit transaction."""
    if USE_POSTGRES:
        db.commit()


def _fetch_one_dict(cursor, row):
    """Convert row to dictionary."""
    if row is None:
        return None
    if USE_POSTGRES:
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    else:
        return dict(row) if row else None


# ============== User Operations ==============

def register_user_with_invite_code(username: str, password: str, invite_code: str) -> Optional[int]:
    """Register user and mark invite code as used in a single transaction.

    Returns user_id if successful, None otherwise.
    Raises ValueError if invite code is invalid or already used.
    """
    password_hash, salt = hash_password(password)
    invite_code = invite_code.upper()

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()

            # 1. Check if invite code exists and is unused
            cursor.execute(
                "SELECT is_used FROM invite_codes WHERE code = %s FOR UPDATE",
                (invite_code,)
            )
            row = cursor.fetchone()

            if row is None:
                cursor.close()
                raise ValueError("Invalid invite code")
            if row[0] is True or row[0] == 1:
                cursor.close()
                raise ValueError("Invite code already used")

            # 2. Create user
            cursor.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s) RETURNING id",
                (username, password_hash, salt)
            )
            user_id = cursor.fetchone()[0]

            # 3. Mark invite code as used
            cursor.execute(
                "UPDATE invite_codes SET is_used = 1, used_by = %s, used_at = CURRENT_TIMESTAMP WHERE code = %s",
                (username, invite_code)
            )

            # 4. Commit transaction
            db.commit()
            cursor.close()
            return user_id
        else:
            # 1. Check if invite code exists and is unused
            row = db.execute(
                "SELECT is_used FROM invite_codes WHERE code = ?",
                (invite_code,)
            ).fetchone()

            if row is None:
                raise ValueError("Invalid invite code")
            if row['is_used'] == 1:
                raise ValueError("Invite code already used")

            # 2. Create user
            cursor = db.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt)
            )
            user_id = cursor.lastrowid

            # 3. Mark invite code as used
            db.execute(
                "UPDATE invite_codes SET is_used = 1, used_by = ?, used_at = CURRENT_TIMESTAMP WHERE code = ?",
                (username, invite_code)
            )

            # 4. Commit transaction
            db.commit()
            return user_id


def create_user(username: str, password: str) -> Optional[int]:
    """Create a new user. Returns user_id or None if username exists."""
    password_hash, salt = hash_password(password)

    with get_db() as db:
        try:
            if USE_POSTGRES:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s) RETURNING id",
                    (username, password_hash, salt)
                )
                db.commit()
                user_id = cursor.fetchone()[0]
                cursor.close()
                return user_id
            else:
                cursor = db.execute(
                    "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                    (username, password_hash, salt)
                )
                db.commit()
                return cursor.lastrowid
        except Exception:
            return None


def verify_user(username: str, password: str) -> Optional[int]:
    """Verify user credentials. Returns user_id if valid, None otherwise."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, password_hash, salt FROM users WHERE username = %s",
                (username,)
            )
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                return None
            db_password_hash, salt = row[1], row[2]
            user_id = row[0]
            cursor.close()
        else:
            row = db.execute(
                "SELECT id, password_hash, salt FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if row is None:
                return None
            db_password_hash, salt = row['password_hash'], row['salt']
            user_id = row['id']

        password_hash, _ = hash_password(password, salt)
        return user_id if password_hash == db_password_hash else None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, username, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                return None
            return {'id': row[0], 'username': row[1], 'created_at': row[2]}
        else:
            row = db.execute(
                "SELECT id, username, created_at FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
            return dict(row) if row else None


# ============== Profile Operations ==============

def create_profile(
    user_id: int,
    name: str,
    personality: Optional[str] = None,
    relationship: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[str] = None,
    chat_history_text: Optional[str] = None,
    photo_path: Optional[str] = None,
    language: str = 'zh-CN'
) -> int:
    """Create a new profile for user."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO profiles (user_id, name, relationship, gender, age, personality, chat_history_text, photo_path, language)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (user_id, name, relationship, gender, age, personality, chat_history_text, photo_path, language))
            db.commit()
            profile_id = cursor.fetchone()[0]
            cursor.close()
            return profile_id
        else:
            cursor = db.execute("""
                INSERT INTO profiles (user_id, name, relationship, gender, age, personality, chat_history_text, photo_path, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, relationship, gender, age, personality, chat_history_text, photo_path, language))
            db.commit()
            return cursor.lastrowid


def update_profile(
    profile_id: int,
    user_id: int,
    name: str,
    personality: Optional[str] = None,
    relationship: Optional[str] = None,
    gender: Optional[str] = None,
    age: Optional[str] = None,
    chat_history_text: Optional[str] = None,
    photo_path: Optional[str] = None,
    language: Optional[str] = None
) -> bool:
    """Update a profile."""
    with get_db() as db:
        if USE_POSTGRES:
            if language:
                cursor = db.cursor()
                cursor.execute("""
                    UPDATE profiles
                    SET name = %s, relationship = %s, gender = %s, age = %s, personality = %s, chat_history_text = %s,
                        photo_path = COALESCE(%s, photo_path),
                        language = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND user_id = %s
                """, (name, relationship, gender, age, personality, chat_history_text, photo_path, language, profile_id, user_id))
                db.commit()
                affected = cursor.rowcount
                cursor.close()
                return affected > 0
            else:
                cursor = db.cursor()
                cursor.execute("""
                    UPDATE profiles
                    SET name = %s, relationship = %s, gender = %s, age = %s, personality = %s, chat_history_text = %s,
                        photo_path = COALESCE(%s, photo_path),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND user_id = %s
                """, (name, relationship, gender, age, personality, chat_history_text, photo_path, profile_id, user_id))
                db.commit()
                affected = cursor.rowcount
                cursor.close()
                return affected > 0
        else:
            if language:
                cursor = db.execute("""
                    UPDATE profiles
                    SET name = ?, relationship = ?, gender = ?, age = ?, personality = ?, chat_history_text = ?,
                        photo_path = COALESCE(?, photo_path),
                        language = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ? AND user_id = ?
                """, (name, relationship, gender, age, personality, chat_history_text, photo_path, language, profile_id, user_id))
            else:
                cursor = db.execute("""
                    UPDATE profiles
                    SET name = ?, relationship = ?, gender = ?, age = ?, personality = ?, chat_history_text = ?,
                        photo_path = COALESCE(?, photo_path),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ? AND user_id = ?
                """, (name, relationship, gender, age, personality, chat_history_text, photo_path, profile_id, user_id))
            db.commit()
            return cursor.rowcount > 0


def get_profile_by_id(profile_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific profile by id and user_id."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM profiles WHERE id = %s AND user_id = %s",
                (profile_id, user_id)
            )
            row = cursor.fetchone()
            result = _fetch_one_dict(cursor, row)
            cursor.close()
            return result
        else:
            row = db.execute(
                "SELECT * FROM profiles WHERE id = ? AND user_id = ?",
                (profile_id, user_id)
            ).fetchone()
            return dict(row) if row else None


def get_profiles(user_id: int) -> List[Dict[str, Any]]:
    """Get all profiles for a user."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM profiles WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute(
                "SELECT * FROM profiles WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ).fetchall()
            return [dict(row) for row in rows]


def delete_profile(profile_id: int, user_id: int) -> bool:
    """Delete a specific profile."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM profiles WHERE id = %s AND user_id = %s",
                (profile_id, user_id)
            )
            db.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        else:
            cursor = db.execute(
                "DELETE FROM profiles WHERE id = ? AND user_id = ?",
                (profile_id, user_id)
            )
            db.commit()
            return cursor.rowcount > 0


# ============== User Consent Operations ==============

def get_user_consent(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user consent status."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM user_consents WHERE user_id = %s",
                (user_id,)
            )
            row = cursor.fetchone()
            result = _fetch_one_dict(cursor, row)
            cursor.close()
            return result
        else:
            row = db.execute(
                "SELECT * FROM user_consents WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            return dict(row) if row else None


def update_user_consent(user_id: int, consent_given: bool) -> bool:
    """Update or create user consent record."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            # Check if record exists
            cursor.execute("SELECT id FROM user_consents WHERE user_id = %s", (user_id,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE user_consents
                    SET consent_given = %s, consent_timestamp = CURRENT_TIMESTAMP, consent_version = '1.0'
                    WHERE user_id = %s
                """, (1 if consent_given else 0, user_id))
            else:
                cursor.execute("""
                    INSERT INTO user_consents (user_id, consent_given, consent_timestamp, consent_version)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, '1.0')
                """, (user_id, 1 if consent_given else 0))

            db.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        else:
            existing = db.execute(
                "SELECT id FROM user_consents WHERE user_id = ?",
                (user_id,)
            ).fetchone()

            if existing:
                cursor = db.execute("""
                    UPDATE user_consents
                    SET consent_given = ?, consent_timestamp = CURRENT_TIMESTAMP, consent_version = '1.0'
                    WHERE user_id = ?
                """, (1 if consent_given else 0, user_id))
            else:
                cursor = db.execute("""
                    INSERT INTO user_consents (user_id, consent_given, consent_timestamp, consent_version)
                    VALUES (?, ?, CURRENT_TIMESTAMP, '1.0')
                """, (user_id, 1 if consent_given else 0))

            db.commit()
            return cursor.rowcount > 0


# ============== User Survey Operations ==============

def get_last_survey_date(user_id: int) -> Optional[str]:
    """Get user's last survey submission date."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT created_at FROM user_surveys WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            return row[0] if row else None
        else:
            row = db.execute(
                "SELECT created_at FROM user_surveys WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            ).fetchone()
            return row['created_at'] if row else None


def submit_survey(
    user_id: int,
    mood_today: int,
    emotion_intensity: int,
    dual_process_state: int,
    five_stage_state: int,
    companionship_preference: int
) -> int:
    """Submit a new survey response."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO user_surveys
                (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference))
            db.commit()
            survey_id = cursor.fetchone()[0]
            cursor.close()
            return survey_id
        else:
            cursor = db.execute("""
                INSERT INTO user_surveys
                (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference))
            db.commit()
            return cursor.lastrowid


# ============== Chat Operations ==============

def add_message(user_id: int, profile_id: int, role: str, content: str) -> int:
    """Add a chat message."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO chat_messages (user_id, profile_id, role, content) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, profile_id, role, content)
            )
            db.commit()
            msg_id = cursor.fetchone()[0]
            cursor.close()
            return msg_id
        else:
            cursor = db.execute(
                "INSERT INTO chat_messages (user_id, profile_id, role, content) VALUES (?, ?, ?, ?)",
                (user_id, profile_id, role, content)
            )
            db.commit()
            return cursor.lastrowid


def add_message_with_emotion(
    user_id: int,
    profile_id: int,
    role: str,
    content: str,
    emotional_tags: Optional[Dict] = None
) -> int:
    """Add a chat message with emotional tags."""
    with get_db() as db:
        tags_json = json.dumps(emotional_tags, ensure_ascii=False) if emotional_tags else None
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO chat_messages (user_id, profile_id, role, content, emotional_tags) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (user_id, profile_id, role, content, tags_json)
            )
            db.commit()
            msg_id = cursor.fetchone()[0]
            cursor.close()
            return msg_id
        else:
            cursor = db.execute(
                "INSERT INTO chat_messages (user_id, profile_id, role, content, emotional_tags) VALUES (?, ?, ?, ?, ?)",
                (user_id, profile_id, role, content, tags_json)
            )
            db.commit()
            return cursor.lastrowid


def get_chat_history(user_id: int, profile_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Get chat history for a specific profile."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, role, content, created_at
                FROM chat_messages
                WHERE user_id = %s AND profile_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (user_id, profile_id, limit))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute("""
                SELECT id, role, content, created_at
                FROM chat_messages
                WHERE user_id = ? AND profile_id = ?
                ORDER BY created_at ASC
                LIMIT ?
            """, (user_id, profile_id, limit)).fetchall()
            return [dict(row) for row in rows]


def clear_chat_history(user_id: int, profile_id: int) -> bool:
    """Clear chat history for a specific profile."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM chat_messages WHERE user_id = %s AND profile_id = %s",
                (user_id, profile_id)
            )
            db.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        else:
            cursor = db.execute(
                "DELETE FROM chat_messages WHERE user_id = ? AND profile_id = ?",
                (user_id, profile_id)
            )
            db.commit()
            return cursor.rowcount > 0


def delete_message(user_id: int, profile_id: int, message_id: int) -> bool:
    """Delete a specific message."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM chat_messages WHERE id = %s AND user_id = %s AND profile_id = %s",
                (message_id, user_id, profile_id)
            )
            db.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        else:
            cursor = db.execute(
                "DELETE FROM chat_messages WHERE id = ? AND user_id = ? AND profile_id = ?",
                (message_id, user_id, profile_id)
            )
            db.commit()
            return cursor.rowcount > 0


# ============== Emotional State Operations ==============

def get_emotional_state(user_id: int, profile_id: int) -> Optional[Dict[str, Any]]:
    """Get emotional state for a user-profile pair."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM emotional_states WHERE user_id = %s AND profile_id = %s",
                (user_id, profile_id)
            )
            row = cursor.fetchone()
            result = _fetch_one_dict(cursor, row)
            cursor.close()
            return result
        else:
            row = db.execute(
                "SELECT * FROM emotional_states WHERE user_id = ? AND profile_id = ?",
                (user_id, profile_id)
            ).fetchone()
            return dict(row) if row else None


def create_or_update_emotional_state(
    user_id: int,
    profile_id: int,
    mood_index: float = 80.0,
    decay_rate: float = 0.03,
    dominant_stage: str = "denial",
    stage_probs: Dict[str, float] = None,
    stability_score: float = 0.5,
    risk_level: float = 0.0,
    negative_streak: int = 0,
    total_interactions: int = 0,
    recovery_phase: str = "acute",
    memory_intimacy_weight: float = 1.0,
    strong_negative_events: int = 0,
    allow_proactive: bool = True,
    next_proactive_time: Optional[datetime] = None,
    valence: float = 0.0,
    arousal: float = 0.5,
    behavior_counts: Dict[str, int] = None,
    extracted_keywords: List[str] = None
) -> bool:
    """Create or update emotional state."""
    if stage_probs is None:
        stage_probs = {"denial": 0.2, "anger": 0.2, "bargaining": 0.2,
                       "depression": 0.2, "acceptance": 0.2}
    if behavior_counts is None:
        behavior_counts = {"dependency": 0, "remembrance": 0, "future_oriented": 0, "self_disclosure": 0}
    if extracted_keywords is None:
        extracted_keywords = []

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()

            # Check if exists
            cursor.execute(
                "SELECT id FROM emotional_states WHERE user_id = %s AND profile_id = %s",
                (user_id, profile_id)
            )
            existing = cursor.fetchone()

            if existing:
                sql = (
                    "UPDATE emotional_states SET "
                    "mood_index = %s, decay_rate = %s, dominant_stage = %s, "
                    "recovery_phase = %s, memory_intimacy_weight = %s, "
                    "strong_negative_events = %s, allow_proactive = %s, "
                    "stage_denial = %s, stage_anger = %s, "
                    "stage_bargaining = %s, stage_depression = %s, "
                    "stage_acceptance = %s, stability_score = %s, "
                    "risk_level = %s, negative_streak = %s, "
                    "total_interactions = %s, "
                    "valence = %s, arousal = %s, "
                    "behavior_counts = %s, extracted_keywords = %s, "
                    "last_interaction = CURRENT_TIMESTAMP, "
                    "updated_at = CURRENT_TIMESTAMP"
                )
                params = [
                    mood_index, decay_rate, dominant_stage, recovery_phase,
                    memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                    stage_probs.get("denial", 0.2), stage_probs.get("anger", 0.2),
                    stage_probs.get("bargaining", 0.2), stage_probs.get("depression", 0.2),
                    stage_probs.get("acceptance", 0.2),
                    stability_score, risk_level, negative_streak, total_interactions,
                    valence, arousal,
                    json.dumps(behavior_counts), json.dumps(extracted_keywords)
                ]

                if next_proactive_time:
                    sql += ", next_proactive_time = %s"
                    params.append(next_proactive_time)

                sql += " WHERE user_id = %s AND profile_id = %s"
                params.extend([user_id, profile_id])

                cursor.execute(sql, params)
            else:
                # Build INSERT SQL dynamically based on whether next_proactive_time is provided
                base_columns = (
                    "user_id, profile_id, mood_index, decay_rate, dominant_stage, "
                    "recovery_phase, memory_intimacy_weight, strong_negative_events, allow_proactive, "
                    "stage_denial, stage_anger, stage_bargaining, stage_depression, stage_acceptance, "
                    "stability_score, risk_level, negative_streak, total_interactions, "
                    "valence, arousal, behavior_counts, extracted_keywords"
                )
                base_values = (
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
                )
                params = [
                    user_id, profile_id, mood_index, decay_rate, dominant_stage,
                    recovery_phase, memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                    stage_probs.get("denial", 0.2), stage_probs.get("anger", 0.2),
                    stage_probs.get("bargaining", 0.2), stage_probs.get("depression", 0.2),
                    stage_probs.get("acceptance", 0.2),
                    stability_score, risk_level, negative_streak, total_interactions,
                    valence, arousal,
                    json.dumps(behavior_counts), json.dumps(extracted_keywords)
                ]

                if next_proactive_time:
                    sql = f"""
                        INSERT INTO emotional_states (
                            {base_columns}, next_proactive_time
                        ) VALUES ({base_values}, %s)
                    """
                    params.append(next_proactive_time)
                else:
                    sql = f"""
                        INSERT INTO emotional_states (
                            {base_columns}
                        ) VALUES ({base_values})
                    """

                cursor.execute(sql, params)

            db.commit()
            cursor.close()
            return True
        else:
            existing = db.execute(
                "SELECT id FROM emotional_states WHERE user_id = ? AND profile_id = ?",
                (user_id, profile_id)
            ).fetchone()

            if existing:
                sql = """
                    UPDATE emotional_states SET
                        mood_index = ?, decay_rate = ?, dominant_stage = ?,
                        recovery_phase = ?, memory_intimacy_weight = ?,
                        strong_negative_events = ?, allow_proactive = ?,
                        stage_denial = ?, stage_anger = ?,
                        stage_bargaining = ?, stage_depression = ?,
                        stage_acceptance = ?, stability_score = ?,
                        risk_level = ?, negative_streak = ?,
                        total_interactions = ?,
                        valence = ?, arousal = ?,
                        behavior_counts = ?, extracted_keywords = ?,
                        last_interaction = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                """
                params = [
                    mood_index, decay_rate, dominant_stage, recovery_phase,
                    memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                    stage_probs.get("denial", 0.2), stage_probs.get("anger", 0.2),
                    stage_probs.get("bargaining", 0.2), stage_probs.get("depression", 0.2),
                    stage_probs.get("acceptance", 0.2),
                    stability_score, risk_level, negative_streak, total_interactions,
                    valence, arousal,
                    json.dumps(behavior_counts), json.dumps(extracted_keywords)
                ]

                if next_proactive_time:
                    sql += ", next_proactive_time = ?"
                    params.append(next_proactive_time)

                sql += " WHERE user_id = ? AND profile_id = ?"
                params.extend([user_id, profile_id])

                db.execute(sql, params)
            else:
                db.execute("""
                    INSERT INTO emotional_states (
                        user_id, profile_id, mood_index, decay_rate, dominant_stage,
                        recovery_phase, memory_intimacy_weight, strong_negative_events, allow_proactive,
                        stage_denial, stage_anger, stage_bargaining, stage_depression, stage_acceptance,
                        stability_score, risk_level, negative_streak, total_interactions,
                        valence, arousal, behavior_counts, extracted_keywords,
                        next_proactive_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, profile_id, mood_index, decay_rate, dominant_stage,
                    recovery_phase, memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                    stage_probs.get("denial", 0.2), stage_probs.get("anger", 0.2),
                    stage_probs.get("bargaining", 0.2), stage_probs.get("depression", 0.2),
                    stage_probs.get("acceptance", 0.2),
                    stability_score, risk_level, negative_streak, total_interactions,
                    valence, arousal,
                    json.dumps(behavior_counts), json.dumps(extracted_keywords),
                    next_proactive_time
                ))

            db.commit()
            return True


def log_emotional_history(
    user_id: int,
    profile_id: int,
    mood_index: float,
    dominant_stage: str,
    intensity: float,
    risk_level: float,
    grief_density: float,
    text_length: int,
    valence: float = 0.0,
    arousal: float = 0.5,
    behavior_counts: Dict[str, int] = None,
    extracted_keywords: List[str] = None
) -> int:
    """Log emotional history entry."""
    if behavior_counts is None:
        behavior_counts = {}
    if extracted_keywords is None:
        extracted_keywords = []

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO emotional_history
                (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length,
                 valence, arousal, behavior_counts, extracted_keywords)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length,
                  valence, arousal, json.dumps(behavior_counts), json.dumps(extracted_keywords)))
            db.commit()
            entry_id = cursor.fetchone()[0]
            cursor.close()
            return entry_id
        else:
            cursor = db.execute("""
                INSERT INTO emotional_history
                (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length,
                 valence, arousal, behavior_counts, extracted_keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length,
                  valence, arousal, json.dumps(behavior_counts), json.dumps(extracted_keywords)))
            db.commit()
            return cursor.lastrowid


def get_emotional_history(user_id: int, profile_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Get emotional history for a profile."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                SELECT * FROM emotional_history
                WHERE user_id = %s AND profile_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (user_id, profile_id, limit))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute("""
                SELECT * FROM emotional_history
                WHERE user_id = ? AND profile_id = ?
                ORDER BY created_at ASC
                LIMIT ?
            """, (user_id, profile_id, limit)).fetchall()
            return [dict(row) for row in rows]


def get_monthly_emotion_stats(user_id: int, profile_id: int, months: int = 6) -> List[Dict[str, Any]]:
    """
    获取按月统计的情绪数据
    Args:
        user_id: 用户 ID
        profile_id: 档案 ID
        months: 统计最近几个月的数据，默认 6 个月
    Returns:
        按月统计的情绪数据列表，包含每月的心情指数、各阶段占比等
    """
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            # PostgreSQL 使用 date_trunc 函数按月份分组
            cursor.execute("""
                SELECT
                    date_trunc('month', created_at) as month,
                    COUNT(*) as interaction_count,
                    AVG(mood_index) as avg_mood_index,
                    AVG(valence) as avg_valence,
                    AVG(arousal) as avg_arousal,
                    AVG(risk_level) as avg_risk_level,
                    AVG(grief_density) as avg_grief_density,
                    MODE() WITHIN GROUP (ORDER BY dominant_stage) as dominant_stage,
                    -- 计算各阶段占比
                    COUNT(*) FILTER (WHERE dominant_stage = 'denial') * 100.0 / COUNT(*) as denial_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'anger') * 100.0 / COUNT(*) as anger_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'bargaining') * 100.0 / COUNT(*) as bargaining_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'depression') * 100.0 / COUNT(*) as depression_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'acceptance') * 100.0 / COUNT(*) as acceptance_ratio
                FROM emotional_history
                WHERE user_id = %s AND profile_id = %s
                GROUP BY date_trunc('month', created_at)
                ORDER BY month DESC
                LIMIT %s
            """, (user_id, profile_id, months))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            # SQLite 使用 strftime 函数按月份分组
            cursor = db.execute("""
                SELECT
                    strftime('%Y-%m', created_at) as month,
                    COUNT(*) as interaction_count,
                    AVG(mood_index) as avg_mood_index,
                    AVG(valence) as avg_valence,
                    AVG(arousal) as avg_arousal,
                    AVG(risk_level) as avg_risk_level,
                    AVG(grief_density) as avg_grief_density,
                    -- SQLite 不支持 MODE()，使用子查询获取主导阶段
                    (SELECT dominant_stage FROM emotional_history e2
                     WHERE strftime('%Y-%m', e2.created_at) = strftime('%Y-%m', emotional_history.created_at)
                     GROUP BY dominant_stage ORDER BY COUNT(*) DESC LIMIT 1) as dominant_stage,
                    -- 计算各阶段占比（使用 CASE WHEN）
                    SUM(CASE WHEN dominant_stage = 'denial' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as denial_ratio,
                    SUM(CASE WHEN dominant_stage = 'anger' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as anger_ratio,
                    SUM(CASE WHEN dominant_stage = 'bargaining' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as bargaining_ratio,
                    SUM(CASE WHEN dominant_stage = 'depression' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as depression_ratio,
                    SUM(CASE WHEN dominant_stage = 'acceptance' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as acceptance_ratio
                FROM emotional_history
                WHERE user_id = ? AND profile_id = ?
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY month DESC
                LIMIT ?
            """, (user_id, profile_id, months))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


def get_period_emotion_stats(user_id: int, profile_id: int, period_days: int = 30) -> Dict[str, Any]:
    """
    获取按 10 天周期统计的情绪数据（30 天项目周期）
    Args:
        user_id: 用户 ID
        profile_id: 档案 ID
        period_days: 项目周期天数，默认 30 天
    Returns:
        按 10 天周期统计的情绪数据，包含三个周期（1-10 天、11-20 天、21-30 天）的心情指数、
        各阶段占比等
    """
    with get_db() as db:
        # 获取用户的 phase_start_time 作为参考点
        if USE_POSTGRES:
            cursor = db.cursor()
            # 首先获取用户的 phase_start_time
            cursor.execute("""
                SELECT phase_start_time FROM emotional_states
                WHERE user_id = %s AND profile_id = %s
                ORDER BY created_at DESC LIMIT 1
            """, (user_id, profile_id))
            start_row = cursor.fetchone()
            if not start_row:
                return {"periods": [], "message": "未找到情感状态数据"}
            
            # PostgreSQL 版本：使用 CASE WHEN 按天数区间分组
            cursor.execute("""
                WITH period_data AS (
                    SELECT
                        CASE
                            WHEN EXTRACT(EPOCH FROM (created_at - %s)) / 86400 <= 10 THEN 1
                            WHEN EXTRACT(EPOCH FROM (created_at - %s)) / 86400 <= 20 THEN 2
                            ELSE 3
                        END as period_num,
                        mood_index,
                        valence,
                        arousal,
                        risk_level,
                        grief_density,
                        dominant_stage
                    FROM emotional_history
                    WHERE user_id = %s AND profile_id = %s
                    AND created_at >= %s
                    AND EXTRACT(EPOCH FROM (created_at - %s)) / 86400 <= %s
                )
                SELECT
                    period_num,
                    COUNT(*) as interaction_count,
                    AVG(mood_index) as avg_mood_index,
                    AVG(valence) as avg_valence,
                    AVG(arousal) as avg_arousal,
                    AVG(risk_level) as avg_risk_level,
                    AVG(grief_density) as avg_grief_density,
                    MODE() WITHIN GROUP (ORDER BY dominant_stage) as dominant_stage,
                    COUNT(*) FILTER (WHERE dominant_stage = 'denial') * 100.0 / COUNT(*) as denial_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'anger') * 100.0 / COUNT(*) as anger_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'bargaining') * 100.0 / COUNT(*) as bargaining_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'depression') * 100.0 / COUNT(*) as depression_ratio,
                    COUNT(*) FILTER (WHERE dominant_stage = 'acceptance') * 100.0 / COUNT(*) as acceptance_ratio
                FROM period_data
                GROUP BY period_num
                ORDER BY period_num ASC
            """, (start_row[0], start_row[0], user_id, profile_id, start_row[0], start_row[0], period_days))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = {"periods": [dict(zip(columns, row)) for row in rows]}
            cursor.close()
            return result
        else:
            # SQLite 版本
            cursor = db.execute("""
                SELECT
                    CASE
                        WHEN (julianday(created_at) - julianday(?)) <= 10 THEN 1
                        WHEN (julianday(created_at) - julianday(?)) <= 20 THEN 2
                        ELSE 3
                    END as period_num,
                    COUNT(*) as interaction_count,
                    AVG(mood_index) as avg_mood_index,
                    AVG(valence) as avg_valence,
                    AVG(arousal) as avg_arousal,
                    AVG(risk_level) as avg_risk_level,
                    AVG(grief_density) as avg_grief_density,
                    SUM(CASE WHEN dominant_stage = 'denial' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as denial_ratio,
                    SUM(CASE WHEN dominant_stage = 'anger' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as anger_ratio,
                    SUM(CASE WHEN dominant_stage = 'bargaining' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as bargaining_ratio,
                    SUM(CASE WHEN dominant_stage = 'depression' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as depression_ratio,
                    SUM(CASE WHEN dominant_stage = 'acceptance' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as acceptance_ratio
                FROM emotional_history
                WHERE user_id = ? AND profile_id = ?
                AND julianday(created_at) >= julianday(?)
                AND (julianday(created_at) - julianday(?)) <= ?
                GROUP BY period_num
                ORDER BY period_num ASC
            """, (start_row[0], start_row[0], user_id, profile_id, start_row[0], start_row[0], period_days))
            rows = cursor.fetchall()
            # 获取主导阶段（SQLite 不支持聚合模式，需要单独查询）
            periods = []
            for row in rows:
                period_dict = dict(row)
                period_num = period_dict['period_num']
                # 查询该时期的主导阶段
                cursor.execute("""
                    SELECT dominant_stage FROM emotional_history
                    WHERE user_id = ? AND profile_id = ?
                    AND CASE
                        WHEN (julianday(created_at) - julianday(?)) <= 10 THEN 1
                        WHEN (julianday(created_at) - julianday(?)) <= 20 THEN 2
                        ELSE 3
                    END = ?
                    GROUP BY dominant_stage ORDER BY COUNT(*) DESC LIMIT 1
                """, (user_id, profile_id, start_row[0], start_row[0], period_num))
                stage_row = cursor.fetchone()
                period_dict['dominant_stage'] = stage_row[0] if stage_row else 'unknown'
                periods.append(period_dict)
            return {"periods": periods}


def get_risk_profiles() -> List[Dict[str, Any]]:
    """Get all profiles with high risk level (for monitoring)."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("""
                SELECT es.*, p.name as profile_name, u.username
                FROM emotional_states es
                JOIN profiles p ON es.profile_id = p.id
                JOIN users u ON es.user_id = u.id
                WHERE es.risk_level > 0.3 OR es.dominant_stage = 'depression'
                ORDER BY es.risk_level DESC
            """)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute("""
                SELECT es.*, p.name as profile_name, u.username
                FROM emotional_states es
                JOIN profiles p ON es.profile_id = p.id
                JOIN users u ON es.user_id = u.id
                WHERE es.risk_level > 0.3 OR es.dominant_stage = 'depression'
                ORDER BY es.risk_level DESC
            """).fetchall()
            return [dict(row) for row in rows]


# ============== Invite Code Operations ==============

def generate_invite_code(created_by: Optional[str] = None) -> str:
    """Generate a new unique invite code."""
    code = "INV-" + secrets.token_hex(4).upper()

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO invite_codes (code, created_by) VALUES (%s, %s)",
                (code, created_by)
            )
            db.commit()
            cursor.close()
            return code
        else:
            try:
                db.execute(
                    "INSERT INTO invite_codes (code, created_by) VALUES (?, ?)",
                    (code, created_by)
                )
                db.commit()
                return code
            except sqlite3.IntegrityError:
                return generate_invite_code(created_by)


def generate_multiple_invite_codes(count: int, created_by: Optional[str] = None) -> List[str]:
    """Generate multiple invite codes at once."""
    codes = []
    for _ in range(count):
        codes.append(generate_invite_code(created_by))
    return codes


def verify_invite_code(code: str) -> bool:
    """Verify if an invite code is valid and unused."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT is_used FROM invite_codes WHERE code = %s",
                (code.upper(),)
            )
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                return False
            # PostgreSQL returns bool (False/True), SQLite returns int (0/1)
            return row[0] is False or row[0] == 0
        else:
            row = db.execute(
                "SELECT is_used FROM invite_codes WHERE code = ?",
                (code.upper(),)
            ).fetchone()
            if row is None:
                return False
            return row['is_used'] == 0


def use_invite_code(code: str, username: str) -> bool:
    """Mark an invite code as used."""
    code = code.upper()

    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()

            # Check if code exists and is unused
            cursor.execute(
                "SELECT is_used FROM invite_codes WHERE code = %s",
                (code,)
            )
            row = cursor.fetchone()

            # PostgreSQL returns bool (False/True), SQLite returns int (0/1)
            if row is None or (row[0] is True or row[0] == 1):
                cursor.close()
                return False

            # Mark as used
            cursor.execute(
                "UPDATE invite_codes SET is_used = 1, used_by = %s, used_at = CURRENT_TIMESTAMP WHERE code = %s",
                (username, code)
            )
            db.commit()
            cursor.close()
            return True
        else:
            row = db.execute(
                "SELECT is_used FROM invite_codes WHERE code = ?",
                (code,)
            ).fetchone()

            if row is None or row['is_used'] == 1:
                return False

            db.execute(
                "UPDATE invite_codes SET is_used = 1, used_by = ?, used_at = CURRENT_TIMESTAMP WHERE code = ?",
                (username, code)
            )
            db.commit()
            return True


def get_invite_code_info(code: str) -> Optional[Dict[str, Any]]:
    """Get information about an invite code."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM invite_codes WHERE code = %s",
                (code.upper(),)
            )
            row = cursor.fetchone()
            result = _fetch_one_dict(cursor, row)
            cursor.close()
            return result
        else:
            row = db.execute(
                "SELECT * FROM invite_codes WHERE code = ?",
                (code.upper(),)
            ).fetchone()
            return dict(row) if row else None


def get_all_invite_codes() -> List[Dict[str, Any]]:
    """Get all invite codes."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM invite_codes ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute(
                "SELECT * FROM invite_codes ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]


def get_unused_invite_codes() -> List[Dict[str, Any]]:
    """Get all unused invite codes."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM invite_codes WHERE is_used = 0 ORDER BY created_at DESC")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            return result
        else:
            rows = db.execute(
                "SELECT * FROM invite_codes WHERE is_used = 0 ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]


def delete_invite_code(code: str) -> bool:
    """Delete an invite code."""
    with get_db() as db:
        if USE_POSTGRES:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM invite_codes WHERE code = %s",
                (code.upper(),)
            )
            db.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        else:
            cursor = db.execute(
                "DELETE FROM invite_codes WHERE code = ?",
                (code.upper(),)
            )
            db.commit()
            return cursor.rowcount > 0


# Initialize database on import
init_db()
