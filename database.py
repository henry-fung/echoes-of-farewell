"""
Database models and operations for MemorialChat
"""
import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import json

DATABASE_FILE = "memorial_chat.db"


def init_db():
    """Initialize the database with all tables."""
    with get_db() as db:
        # Users table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Profiles table (multiple per user)
        db.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            )
        """)
        
        # Chat messages table (linked to profile)
        db.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                profile_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                emotional_tags TEXT,  -- JSON: 情感标签
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        """)
        
        # Emotional state tracking table (增强版)
        db.execute("""
            CREATE TABLE IF NOT EXISTS emotional_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                UNIQUE(user_id, profile_id)
            )
        """)
        
        # Emotional history log table
        db.execute("""
            CREATE TABLE IF NOT EXISTS emotional_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                profile_id INTEGER NOT NULL,
                mood_index REAL,
                dominant_stage TEXT,
                intensity REAL,
                risk_level REAL,
                grief_density REAL,
                text_length INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        """)

        db.commit()

    # Add relationship column if not exists (migration for existing databases)
    with get_db() as db:
        try:
            db.execute("ALTER TABLE profiles ADD COLUMN relationship TEXT")
            db.commit()
        except sqlite3.OperationalError:
            pass

    # Add gender and age columns if not exists (migration for existing databases)
    with get_db() as db:
        try:
            db.execute("ALTER TABLE profiles ADD COLUMN gender TEXT")
            db.commit()
        except sqlite3.OperationalError:
            pass

    with get_db() as db:
        try:
            db.execute("ALTER TABLE profiles ADD COLUMN age TEXT")
            db.commit()
        except sqlite3.OperationalError:
            pass

    # Add user_consents table if not exists (migration for existing databases)
    with get_db() as db:
        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS user_consents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    consent_given INTEGER DEFAULT 0,
                    consent_timestamp TIMESTAMP,
                    consent_version TEXT DEFAULT '1.0',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            db.commit()
        except sqlite3.OperationalError:
            pass

    # Add user_surveys table if not exists
    with get_db() as db:
        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS user_surveys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    mood_today INTEGER,
                    emotion_intensity INTEGER,
                    dual_process_state INTEGER,
                    five_stage_state INTEGER,
                    companionship_preference INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            db.commit()
        except sqlite3.OperationalError:
            pass

    # Add invite_codes table for invitation system
    with get_db() as db:
        try:
            db.execute("""
                CREATE TABLE IF NOT EXISTS invite_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used_by TEXT,
                    used_at TIMESTAMP,
                    is_used INTEGER DEFAULT 0
                )
            """)
            db.commit()
        except sqlite3.OperationalError:
            pass


@contextmanager
def get_db():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


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


# ============== User Operations ==============

def create_user(username: str, password: str) -> Optional[int]:
    """Create a new user. Returns user_id or None if username exists."""
    password_hash, salt = hash_password(password)
    
    with get_db() as db:
        try:
            cursor = db.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt)
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None


def verify_user(username: str, password: str) -> Optional[int]:
    """Verify user credentials. Returns user_id if valid, None otherwise."""
    with get_db() as db:
        row = db.execute(
            "SELECT id, password_hash, salt FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        
        if row is None:
            return None
        
        password_hash, _ = hash_password(password, row['salt'])
        if password_hash == row['password_hash']:
            return row['id']
        return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    with get_db() as db:
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
        row = db.execute(
            "SELECT * FROM profiles WHERE id = ? AND user_id = ?",
            (profile_id, user_id)
        ).fetchone()
        return dict(row) if row else None


# ============== User Consent Operations ==============

def get_user_consent(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user consent status."""
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM user_consents WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None

def update_user_consent(user_id: int, consent_given: bool) -> bool:
    """Update or create user consent record."""
    with get_db() as db:
        # Check if record exists
        existing = db.execute(
            "SELECT id FROM user_consents WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if existing:
            # Update existing record
            cursor = db.execute("""
                UPDATE user_consents
                SET consent_given = ?, consent_timestamp = CURRENT_TIMESTAMP, consent_version = '1.0'
                WHERE user_id = ?
            """, (1 if consent_given else 0, user_id))
        else:
            # Insert new record
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
        cursor = db.execute("""
            INSERT INTO user_surveys
            (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, mood_today, emotion_intensity, dual_process_state, five_stage_state, companionship_preference))
        db.commit()
        return cursor.lastrowid


def get_profiles(user_id: int) -> List[Dict[str, Any]]:
    """Get all profiles for a user."""
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM profiles WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def delete_profile(profile_id: int, user_id: int) -> bool:
    """Delete a specific profile."""
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM profiles WHERE id = ? AND user_id = ?",
            (profile_id, user_id)
        )
        db.commit()
        return cursor.rowcount > 0


# ============== Chat Operations ==============

def add_message(user_id: int, profile_id: int, role: str, content: str) -> int:
    """Add a chat message."""
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO chat_messages (user_id, profile_id, role, content) VALUES (?, ?, ?, ?)",
            (user_id, profile_id, role, content)
        )
        db.commit()
        return cursor.lastrowid


def get_chat_history(user_id: int, profile_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Get chat history for a specific profile, ordered by time."""
    with get_db() as db:
        rows = db.execute(
            """SELECT id, role, content, created_at 
               FROM chat_messages 
               WHERE user_id = ? AND profile_id = ?
               ORDER BY created_at DESC 
               LIMIT ?""",
            (user_id, profile_id, limit)
        ).fetchall()
        return [dict(row) for row in reversed(rows)]


def clear_chat_history(user_id: int, profile_id: int) -> bool:
    """Clear chat history for a specific profile."""
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM chat_messages WHERE user_id = ? AND profile_id = ?",
            (user_id, profile_id)
        )
        db.commit()
        return cursor.rowcount > 0


def delete_message(user_id: int, profile_id: int, message_id: int) -> bool:
    """Delete a specific message."""
    with get_db() as db:
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
        row = db.execute(
            """SELECT * FROM emotional_states 
               WHERE user_id = ? AND profile_id = ?""",
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
    next_proactive_time: Optional[datetime] = None
) -> bool:
    """Create or update emotional state (增强版)."""
    if stage_probs is None:
        stage_probs = {"denial": 0.2, "anger": 0.2, "bargaining": 0.2, 
                      "depression": 0.2, "acceptance": 0.2}
    
    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM emotional_states WHERE user_id = ? AND profile_id = ?",
            (user_id, profile_id)
        ).fetchone()
        
        if existing:
            sql = """
                UPDATE emotional_states SET
                    mood_index = ?,
                    decay_rate = ?,
                    dominant_stage = ?,
                    recovery_phase = ?,
                    memory_intimacy_weight = ?,
                    strong_negative_events = ?,
                    allow_proactive = ?,
                    stage_denial = ?,
                    stage_anger = ?,
                    stage_bargaining = ?,
                    stage_depression = ?,
                    stage_acceptance = ?,
                    stability_score = ?,
                    risk_level = ?,
                    negative_streak = ?,
                    total_interactions = ?,
                    last_interaction = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
            """
            params = [
                mood_index, decay_rate, dominant_stage, recovery_phase,
                memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                stage_probs.get("denial", 0.2),
                stage_probs.get("anger", 0.2),
                stage_probs.get("bargaining", 0.2),
                stage_probs.get("depression", 0.2),
                stage_probs.get("acceptance", 0.2),
                stability_score, risk_level, negative_streak, total_interactions
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
                    next_proactive_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, profile_id, mood_index, decay_rate, dominant_stage,
                recovery_phase, memory_intimacy_weight, strong_negative_events, 1 if allow_proactive else 0,
                stage_probs.get("denial", 0.2),
                stage_probs.get("anger", 0.2),
                stage_probs.get("bargaining", 0.2),
                stage_probs.get("depression", 0.2),
                stage_probs.get("acceptance", 0.2),
                stability_score, risk_level, negative_streak, total_interactions,
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
    text_length: int
) -> int:
    """Log emotional history entry."""
    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO emotional_history 
            (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, profile_id, mood_index, dominant_stage, intensity, risk_level, grief_density, text_length))
        db.commit()
        return cursor.lastrowid


def get_emotional_history(user_id: int, profile_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Get emotional history for a profile."""
    with get_db() as db:
        rows = db.execute(
            """SELECT * FROM emotional_history 
               WHERE user_id = ? AND profile_id = ?
               ORDER BY created_at DESC LIMIT ?""",
            (user_id, profile_id, limit)
        ).fetchall()
        return [dict(row) for row in reversed(rows)]


def get_risk_profiles() -> List[Dict[str, Any]]:
    """Get all profiles with high risk level (for monitoring)."""
    with get_db() as db:
        rows = db.execute(
            """SELECT es.*, p.name as profile_name, u.username 
               FROM emotional_states es
               JOIN profiles p ON es.profile_id = p.id
               JOIN users u ON es.user_id = u.id
               WHERE es.risk_level > 0.3 OR es.dominant_stage = 'depression'
               ORDER BY es.risk_level DESC"""
        ).fetchall()
        return [dict(row) for row in rows]


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
        cursor = db.execute(
            "INSERT INTO chat_messages (user_id, profile_id, role, content, emotional_tags) VALUES (?, ?, ?, ?, ?)",
            (user_id, profile_id, role, content, tags_json)
        )
        db.commit()
        return cursor.lastrowid


# ============== Invite Code Operations ==============

def generate_invite_code(created_by: Optional[str] = None) -> str:
    """Generate a new unique invite code.

    Args:
        created_by: Optional username of who created this code

    Returns:
        The generated invite code (format: INV-XXXXXXXX)
    """
    code = "INV-" + secrets.token_hex(4).upper()  # 8 characters after INV-

    with get_db() as db:
        try:
            db.execute(
                "INSERT INTO invite_codes (code, created_by) VALUES (?, ?)",
                (code, created_by)
            )
            db.commit()
            return code
        except sqlite3.IntegrityError:
            # Code already exists (very rare), generate again
            return generate_invite_code(created_by)


def generate_multiple_invite_codes(count: int, created_by: Optional[str] = None) -> List[str]:
    """Generate multiple invite codes at once.

    Args:
        count: Number of codes to generate
        created_by: Optional username of who created these codes

    Returns:
        List of generated invite codes
    """
    codes = []
    for _ in range(count):
        codes.append(generate_invite_code(created_by))
    return codes


def verify_invite_code(code: str) -> bool:
    """Verify if an invite code is valid and unused.

    Args:
        code: The invite code to verify

    Returns:
        True if the code is valid and unused, False otherwise
    """
    with get_db() as db:
        row = db.execute(
            "SELECT is_used FROM invite_codes WHERE code = ?",
            (code.upper(),)
        ).fetchone()

        if row is None:
            return False  # Code doesn't exist

        return row['is_used'] == 0  # True if not used


def use_invite_code(code: str, username: str) -> bool:
    """Mark an invite code as used.

    Args:
        code: The invite code that was used
        username: The username who used the code

    Returns:
        True if successfully marked as used, False if code was already used or invalid
    """
    code = code.upper()

    with get_db() as db:
        # Check if code exists and is unused
        row = db.execute(
            "SELECT is_used FROM invite_codes WHERE code = ?",
            (code,)
        ).fetchone()

        if row is None or row['is_used'] == 1:
            return False  # Code doesn't exist or already used

        # Mark as used
        db.execute(
            "UPDATE invite_codes SET is_used = 1, used_by = ?, used_at = CURRENT_TIMESTAMP WHERE code = ?",
            (username, code)
        )
        db.commit()
        return True


def get_invite_code_info(code: str) -> Optional[Dict[str, Any]]:
    """Get information about an invite code.

    Args:
        code: The invite code to look up

    Returns:
        Dict with code info or None if not found
    """
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM invite_codes WHERE code = ?",
            (code.upper(),)
        ).fetchone()
        return dict(row) if row else None


def get_all_invite_codes() -> List[Dict[str, Any]]:
    """Get all invite codes (for admin purposes).

    Returns:
        List of all invite codes with their usage status
    """
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM invite_codes ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_unused_invite_codes() -> List[Dict[str, Any]]:
    """Get all unused invite codes.

    Returns:
        List of unused invite codes
    """
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM invite_codes WHERE is_used = 0 ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def delete_invite_code(code: str) -> bool:
    """Delete an invite code.

    Args:
        code: The invite code to delete

    Returns:
        True if deleted, False if not found
    """
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM invite_codes WHERE code = ?",
            (code.upper(),)
        )
        db.commit()
        return cursor.rowcount > 0


# Initialize database on import
init_db()
