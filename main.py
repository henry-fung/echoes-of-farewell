"""
MemorialChat - A web application to chat with memories of loved ones
Backend: FastAPI + SQLite + LLM
支持渐进式衰减情感支持系统
"""
import os
import shutil
import asyncio
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Depends, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
try:
    import jwt  # PyJWT
except ImportError:
    import PyJWT as jwt

from database import (
    create_user, verify_user, get_user_by_id,
    create_profile, update_profile, get_profile_by_id, get_profiles, delete_profile,
    add_message, get_chat_history, clear_chat_history,
    get_emotional_state, create_or_update_emotional_state, log_emotional_history,
    get_emotional_history, add_message_with_emotion,
    get_user_consent, update_user_consent,
    get_last_survey_date, submit_survey,
    verify_invite_code, use_invite_code
)
from llm_provider import LLMProvider, LLMFactory
from emotion_engine import emotion_engine, EmotionState
import base64


# Pre-generated invite codes (100 codes) - imported on startup
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


def _import_invite_codes():
    """Import pre-generated invite codes into database on startup."""
    try:
        from database import get_db, USE_POSTGRES

        with get_db() as db:
            # Get existing codes
            if USE_POSTGRES:
                cursor = db.cursor()
                cursor.execute("SELECT code FROM invite_codes")
                existing_codes = {row[0] for row in cursor.fetchall()}
                cursor.close()

                imported_count = 0
                for code in INVITE_CODES_TO_IMPORT:
                    if code in existing_codes:
                        continue
                    try:
                        cursor.execute("""
                            INSERT INTO invite_codes (code, created_by, is_used)
                            VALUES (%s, %s, FALSE)
                        """, (code, 'import'))
                        imported_count += 1
                    except Exception:
                        pass  # Skip duplicates
                db.commit()
            else:
                # SQLite
                existing_codes = {row['code'] for row in db.execute("SELECT code FROM invite_codes").fetchall()}
                imported_count = 0
                for code in INVITE_CODES_TO_IMPORT:
                    if code in existing_codes:
                        continue
                    try:
                        db.execute("""
                            INSERT OR IGNORE INTO invite_codes (code, created_by, is_used)
                            VALUES (?, ?, 0)
                        """, (code, 'import'))
                        imported_count += 1
                    except Exception:
                        pass  # Skip duplicates
                db.commit()

            print(f"[STARTUP] Imported {imported_count} invite codes")
    except Exception as e:
        print(f"[STARTUP] Error importing invite codes: {e}")
        import traceback
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    print("[STARTUP] Initializing database and importing invite codes...")
    from database import init_db
    init_db()
    _import_invite_codes()
    asyncio.create_task(proactive_check_loop())
    print("[STARTUP] Proactive check loop started")
    yield
    # Shutdown (nothing to do here)


# App configuration
app = FastAPI(title="MemorialChat", version="2.1.0", lifespan=lifespan)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
security = HTTPBearer(auto_error=False)

# Upload settings
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# LLM Provider (lazy init)
llm_provider: LLMProvider = None

def get_llm_provider() -> LLMProvider:
    global llm_provider
    if llm_provider is None:
        llm_provider = LLMFactory.create()
    return llm_provider


# ============== Pydantic Models ==============

class UserRegister(BaseModel):
    username: str
    password: str
    invite_code: str  # Required invite code for registration


class UserLogin(BaseModel):
    username: str
    password: str


class ConsentUpdate(BaseModel):
    consent_given: bool


class SurveySubmit(BaseModel):
    answers: dict


class ChatMessage(BaseModel):
    message: str
    profile_id: int
    # Optional client context for accurate time/location-based responses
    client_timestamp: Optional[str] = None  # ISO format datetime from client
    client_timezone: Optional[str] = None   # e.g., "Asia/Shanghai"
    client_city: Optional[str] = None       # User's city for weather
    client_lat: Optional[float] = None      # Latitude for precise weather
    client_lon: Optional[float] = None      # Longitude for precise weather


class ProfileUpdate(BaseModel):
    name: str
    personality: Optional[str] = None
    chat_history_text: Optional[str] = None


# ============== Authentication ==============

def create_token(user_id: int) -> str:
    """Create JWT token for user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow().timestamp() + 7 * 24 * 3600  # 7 days
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Get current user from token."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============== Routes ==============

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve main page."""
    return FileResponse("static/index.html")


# ============== Auth Routes ==============

@app.post("/api/register")
async def register(data: UserRegister):
    """Register new user with invite code."""
    import traceback
    try:
        if len(data.username) < 3 or len(data.username) > 20:
            raise HTTPException(status_code=400, detail="Username must be 3-20 characters")
        if len(data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        # Verify invite code first
        print(f"[REGISTER] Verifying invite code: {data.invite_code}")
        if not verify_invite_code(data.invite_code):
            print(f"[REGISTER] Invite code verification failed: {data.invite_code}")
            raise HTTPException(status_code=400, detail="Invalid or already used invite code")
        print(f"[REGISTER] Invite code verified successfully")

        print(f"[REGISTER] Creating user: {data.username}")
        user_id = create_user(data.username, data.password)
        if user_id is None:
            print(f"[REGISTER] User creation failed - username exists: {data.username}")
            raise HTTPException(status_code=400, detail="Username already exists")
        print(f"[REGISTER] User created with ID: {user_id}")

        # Mark invite code as used
        print(f"[REGISTER] Marking invite code as used: {data.invite_code}")
        use_invite_code(data.invite_code, data.username)
        print(f"[REGISTER] Registration completed successfully")

        token = create_token(user_id)
        return {"success": True, "token": token, "username": data.username}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[REGISTER] Unexpected error: {e}")
        print(f"[REGISTER] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/login")
async def login(data: UserLogin):
    """Login user."""
    user_id = verify_user(data.username, data.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_token(user_id)
    user = get_user_by_id(user_id)
    consent = get_user_consent(user_id)

    return {
        "success": True,
        "token": token,
        "username": user["username"],
        "consent_given": consent["consent_given"] if consent else False
    }


@app.get("/api/me")
async def get_me(user_id: int = Depends(get_current_user)):
    """Get current user info."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "user": user}


# ============== User Consent Routes ==============

@app.get("/api/consent")
async def get_consent(user_id: int = Depends(get_current_user)):
    """Get user consent status."""
    consent = get_user_consent(user_id)
    return {
        "success": True,
        "consent_given": consent["consent_given"] if consent else False,
        "consent_timestamp": consent["consent_timestamp"] if consent else None,
        "consent_version": consent["consent_version"] if consent else None
    }

@app.post("/api/consent")
async def update_consent(data: ConsentUpdate, user_id: int = Depends(get_current_user)):
    """Update user consent."""
    success = update_user_consent(user_id, data.consent_given)
    return {"success": success}


# ============== User Survey Routes ==============

from datetime import datetime, timedelta

@app.get("/api/survey/status")
async def get_survey_status(user_id: int = Depends(get_current_user)):
    """Get user's survey status (whether survey is due)."""
    last_survey_date = get_last_survey_date(user_id)

    if not last_survey_date:
        # No survey submitted yet, survey is due
        return {
            "success": True,
            "survey_due": True,
            "last_survey_date": None,
            "days_since_last_survey": None
        }

    # Parse the last survey date
    if isinstance(last_survey_date, str):
        last_date = datetime.fromisoformat(last_survey_date.replace('Z', '+00:00'))
    else:
        last_date = last_survey_date

    now = datetime.now(last_date.tzinfo) if last_date.tzinfo else datetime.now()
    diff_days = (now - last_date).days

    # Survey is due every 5 days
    survey_due = diff_days >= 5

    return {
        "success": True,
        "survey_due": survey_due,
        "last_survey_date": last_survey_date,
        "days_since_last_survey": diff_days
    }

@app.post("/api/survey/submit")
async def submit_survey_endpoint(data: SurveySubmit, user_id: int = Depends(get_current_user)):
    """Submit user survey."""
    answers = data.answers

    survey_id = submit_survey(
        user_id=user_id,
        mood_today=answers.get("mood_today", 0),
        emotion_intensity=answers.get("emotion_intensity", 0),
        dual_process_state=answers.get("dual_process_state", 0),
        five_stage_state=answers.get("five_stage_state", 0),
        companionship_preference=answers.get("companionship_preference", 0)
    )

    return {
        "success": True,
        "survey_id": survey_id
    }


# ============== Profile Routes ==============

@app.post("/api/profiles")
async def api_create_profile(
    name: str = Form(...),
    personality: Optional[str] = Form(None),
    relationship: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    chat_history_text: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    avatar_path: Optional[str] = Form(None),
    language: str = Form('zh-CN'),
    user_id: int = Depends(get_current_user)
):
    """Create a new profile."""
    photo_path = None

    # Handle custom photo upload
    if photo:
        if photo.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format")

        content = await photo.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 5MB)")

        # Save file with unique name
        import uuid
        file_ext = Path(photo.filename).suffix
        filename = f"profile_{user_id}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(content)

        photo_path = f"/static/uploads/{filename}"
    elif avatar_path:
        # Use built-in avatar
        photo_path = avatar_path
    else:
        # Default to grandpa avatar
        photo_path = "/static/avatars/grandpa.svg"

    # Create profile with language
    profile_id = create_profile(
        user_id=user_id,
        name=name,
        relationship=relationship,
        gender=gender,
        age=age,
        personality=personality,
        chat_history_text=chat_history_text,
        photo_path=photo_path,
        language=language
    )

    return {"success": True, "profile_id": profile_id}


@app.get("/api/profiles")
async def api_list_profiles(user_id: int = Depends(get_current_user)):
    """Get all profiles for current user."""
    profiles = get_profiles(user_id)
    return {"success": True, "profiles": profiles}


@app.get("/api/profiles/{profile_id}")
async def api_get_profile(profile_id: int, user_id: int = Depends(get_current_user)):
    """Get a specific profile."""
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"success": True, "profile": profile}


@app.put("/api/profiles/{profile_id}")
async def api_update_profile(
    profile_id: int,
    name: str = Form(...),
    personality: Optional[str] = Form(None),
    relationship: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    chat_history_text: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    avatar_path: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    user_id: int = Depends(get_current_user)
):
    """Update a profile."""
    # Check if profile exists and belongs to user
    existing = get_profile_by_id(profile_id, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Profile not found")

    photo_path = None

    # Handle custom photo upload
    if photo:
        if photo.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format")

        content = await photo.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 5MB)")

        # Delete old custom photo if exists (but not built-in avatars)
        if existing.get("photo_path") and "/uploads/" in existing["photo_path"]:
            old_path = Path(existing["photo_path"].lstrip("/"))
            if old_path.exists():
                old_path.unlink()

        # Save new file
        import uuid
        file_ext = Path(photo.filename).suffix
        filename = f"profile_{user_id}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(content)

        photo_path = f"/static/uploads/{filename}"
    elif avatar_path:
        # Use built-in avatar
        # Delete old custom photo if switching to avatar
        if existing.get("photo_path") and "/uploads/" in existing["photo_path"]:
            old_path = Path(existing["photo_path"].lstrip("/"))
            if old_path.exists():
                old_path.unlink()
        photo_path = avatar_path

    # Update profile with language
    success = update_profile(
        profile_id=profile_id,
        user_id=user_id,
        name=name,
        relationship=relationship,
        gender=gender,
        age=age,
        personality=personality,
        chat_history_text=chat_history_text,
        photo_path=photo_path,
        language=language
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to update profile")

    return {"success": True}


@app.delete("/api/profiles/{profile_id}")
async def api_delete_profile(profile_id: int, user_id: int = Depends(get_current_user)):
    """Delete a profile and its chat history."""
    # Get profile to delete photo
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Delete photo if exists
    if profile.get("photo_path"):
        photo_path = Path(profile["photo_path"].lstrip("/"))
        if photo_path.exists():
            photo_path.unlink()
    
    # Delete profile (chat history will be cascade deleted)
    success = delete_profile(profile_id, user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete profile")
    
    return {"success": True}


# ============== Chat Routes ==============

# Language display names mapping
LANGUAGE_NAMES = {
    'zh-CN': '简体中文',
    'zh-HK': '繁体中文（香港）',
    'zh-TW': '繁体中文（台湾）',
    'en-HK': '香港英语',
    'en-US': '美式英语',
    'en-GB': '英式英语'
}

def get_time_context(language: str = "zh-CN", client_timestamp: str = None, client_timezone: str = None) -> dict:
    """Get current time context including season, festivals and weather for the prompt.
    
    Args:
        language: Language code
        client_timestamp: ISO format datetime from client (optional)
        client_timezone: Client timezone name (optional)
    """
    from datetime import datetime
    from datetime import timezone as dt_timezone
    import os
    
    # Use client timestamp if provided, otherwise use server time
    if client_timestamp:
        try:
            # Parse ISO format timestamp (UTC)
            utc_now = datetime.fromisoformat(client_timestamp.replace('Z', '+00:00'))
            print(f"[Time Context] UTC time: {utc_now}, timezone: {client_timezone}")
            
            # Convert to client's local timezone if provided
            if client_timezone:
                try:
                    from zoneinfo import ZoneInfo
                    client_tz = ZoneInfo(client_timezone)
                    now = utc_now.astimezone(client_tz)
                    print(f"[Time Context] Converted to {client_timezone}: {now}")
                except Exception as tz_err:
                    print(f"[Time Context] Timezone conversion failed: {tz_err}, using UTC")
                    now = utc_now
            else:
                # Fallback: use server's local time
                now = utc_now
        except Exception as e:
            print(f"[Time Context] Failed to parse client time: {e}, using server time")
            now = datetime.now()
    else:
        now = datetime.now()
        print(f"[Time Context] Using server time: {now}")
    
    hour = now.hour
    weekday = now.weekday()
    month = now.month
    day = now.day
    
    # Determine time period
    if 5 <= hour < 11:
        time_period = "morning"
    elif 11 <= hour < 13:
        time_period = "noon"
    elif 13 <= hour < 18:
        time_period = "afternoon"
    elif 18 <= hour < 22:
        time_period = "evening"
    else:
        time_period = "night"
    
    # Determine season
    if language.startswith('zh'):
        seasons = {12: "冬季", 1: "冬季", 2: "冬季",
                   3: "春季", 4: "春季", 5: "春季",
                   6: "夏季", 7: "夏季", 8: "夏季",
                   9: "秋季", 10: "秋季", 11: "秋季"}
        season = seasons[month]
    else:
        seasons = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}
        season = seasons[month]
    
    # Check for festivals
    festival = get_festival(month, day, language)
    
    # Get weather (if API key is configured)
    weather = get_weather_context(language)
    
    # Determine weekday type
    is_weekend = weekday >= 5
    
    # Format current time string
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y-%m-%d")
    
    # Language-specific time descriptions
    if language.startswith('zh'):
        period_names = {
            "morning": "早上",
            "noon": "中午", 
            "afternoon": "下午",
            "evening": "晚上",
            "night": "深夜"
        }
        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        day_type = "周末" if is_weekend else "工作日"
        month_names = ["", "1月", "2月", "3月", "4月", "5月", "6月", 
                       "7月", "8月", "9月", "10月", "11月", "12月"]
    else:
        period_names = {
            "morning": "morning",
            "noon": "noon",
            "afternoon": "afternoon", 
            "evening": "evening",
            "night": "late night"
        }
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_type = "weekend" if is_weekend else "weekday"
        month_names = ["", "January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
    
    return {
        "time_str": time_str,
        "date_str": date_str,
        "hour": hour,
        "month": month,
        "month_name": month_names[month],
        "day": day,
        "period": time_period,
        "period_name": period_names[time_period],
        "weekday": weekday_names[weekday],
        "is_weekend": is_weekend,
        "day_type": day_type,
        "season": season,
        "festival": festival,
        "weather": weather
    }


def get_festival(month: int, day: int, language: str = "zh-CN", year: int = None) -> str:
    """Get festival name for the given date.
    
    Uses lunarcalendar library for accurate lunar festival calculation.
    Install: pip install lunarcalendar
    
    Args:
        month: Month (1-12)
        day: Day (1-31)
        language: Language code
        year: Year (defaults to current year)
    """
    from datetime import datetime
    
    if year is None:
        year = datetime.now().year
    
    # Fixed date festivals (solar calendar)
    festivals = {
        (1, 1): ("元旦", "New Year's Day"),
        (2, 14): ("情人节", "Valentine's Day"),
        (3, 8): ("妇女节", "Women's Day"),
        (4, 1): ("愚人节", "April Fools' Day"),
        (5, 1): ("劳动节", "Labor Day"),
        (6, 1): ("儿童节", "Children's Day"),
        (10, 1): ("国庆节", "National Day"),
        (10, 31): ("万圣节", "Halloween"),
        (12, 24): ("平安夜", "Christmas Eve"),
        (12, 25): ("圣诞节", "Christmas"),
        (12, 31): ("跨年夜", "New Year's Eve"),
    }
    
    # Check fixed festivals first
    if (month, day) in festivals:
        cn, en = festivals[(month, day)]
        return cn if language.startswith('zh') else en
    
    # Try to get lunar festivals using lunarcalendar library
    try:
        from lunarcalendar import Converter, Solar, Lunar
        
        # Convert current date to lunar
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)
        lunar_month = lunar.Month
        lunar_day = lunar.Day
        
        # Lunar New Year (正月初一)
        if lunar_month == 1 and lunar_day == 1:
            return "春节" if language.startswith('zh') else "Chinese New Year (Spring Festival)"
        
        # Lantern Festival (正月十五)
        if lunar_month == 1 and lunar_day == 15:
            return "元宵节" if language.startswith('zh') else "Lantern Festival"
        
        # Dragon Boat Festival (五月初五)
        if lunar_month == 5 and lunar_day == 5:
            return "端午节" if language.startswith('zh') else "Dragon Boat Festival"
        
        # Qixi Festival (七月初七)
        if lunar_month == 7 and lunar_day == 7:
            return "七夕节" if language.startswith('zh') else "Qixi Festival (Chinese Valentine's Day)"
        
        # Mid-Autumn Festival (八月十五)
        if lunar_month == 8 and lunar_day == 15:
            return "中秋节" if language.startswith('zh') else "Mid-Autumn Festival"
        
        # Double Ninth Festival (九月初九)
        if lunar_month == 9 and lunar_day == 9:
            return "重阳节" if language.startswith('zh') else "Double Ninth Festival"
        
        # Laba Festival (腊月初八)
        if lunar_month == 12 and lunar_day == 8:
            return "腊八节" if language.startswith('zh') else "Laba Festival"
        
        # New Year's Eve (除夕 - 腊月最后一天)
        # Check if it's the last day of lunar year
        if lunar_month == 12:
            # Get days in this lunar month
            days_in_month = Converter.getLunarMonthDays(year, 12)
            if lunar_day == days_in_month:
                return "除夕" if language.startswith('zh') else "Chinese New Year's Eve"
        
    except ImportError:
        # lunarcalendar not installed, fall through to simplified version
        print("[Festival] lunarcalendar not installed, using simplified calculation")
        pass
    except Exception as e:
        print(f"[Festival] Error calculating lunar festival: {e}")
        pass
    
    # Check for Double 11 Shopping Festival (solar calendar)
    if month == 11 and day == 11:
        return "双十一" if language.startswith('zh') else "Singles' Day (Shopping Festival)"
    
    return ""


def get_weather_context(language: str = "zh-CN", client_city: str = None, 
                        client_lat: float = None, client_lon: float = None) -> dict:
    """Get weather context. If weather API not configured, return season-based suggestions.
    
    Args:
        language: Language code
        client_city: Client's city name (optional)
        client_lat: Client's latitude (optional)
        client_lon: Client's longitude (optional)
    """
    import os
    
    # Check if weather API is configured
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    default_city = os.getenv("WEATHER_CITY", "Beijing")
    
    # Use client location if provided, otherwise use default
    if client_lat and client_lon:
        location_desc = f"lat={client_lat}, lon={client_lon}"
    elif client_city:
        location_desc = client_city
    else:
        location_desc = default_city
    
    print(f"[Weather Context] Fetching weather for: {location_desc}")
    
    if weather_api_key:
        try:
            import requests
            
            # Build URL based on available location info
            if client_lat and client_lon:
                # Use coordinates for precise location
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={client_lat}&lon={client_lon}&appid={weather_api_key}&units=metric&lang={'zh_cn' if language.startswith('zh') else 'en'}"
            elif client_city:
                # Use city name
                url = f"http://api.openweathermap.org/data/2.5/weather?q={client_city}&appid={weather_api_key}&units=metric&lang={'zh_cn' if language.startswith('zh') else 'en'}"
            else:
                # Use default city
                url = f"http://api.openweathermap.org/data/2.5/weather?q={default_city}&appid={weather_api_key}&units=metric&lang={'zh_cn' if language.startswith('zh') else 'en'}"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                temp = round(data["main"]["temp"])
                feels_like = round(data["main"]["feels_like"])
                desc = data["weather"][0]["description"]
                print(f"[Weather Context] Success: {desc}, {temp}°C")
                
                if language.startswith('zh'):
                    return {
                        "has_weather": True,
                        "temp": temp,
                        "feels_like": feels_like,
                        "description": desc,
                        "text": f"当前天气：{desc}，{temp}°C（体感{feels_like}°C）"
                    }
                else:
                    return {
                        "has_weather": True,
                        "temp": temp,
                        "feels_like": feels_like,
                        "description": desc,
                        "text": f"Current weather: {desc}, {temp}°C (feels like {feels_like}°C)"
                    }
        except Exception as e:
            print(f"[Weather API Error] {e}")
    
    # Return season-based suggestions if no weather data
    from datetime import datetime
    month = datetime.now().month
    
    if language.startswith('zh'):
        season_tips = {
            "冬季": "天气较冷，注意保暖，出门多穿点衣服",
            "春季": "春暖花开，但早晚温差大，注意增减衣物",
            "夏季": "天气炎热，注意防暑降温，多喝水",
            "秋季": "天气渐凉，注意保暖，预防感冒"
        }
        seasons = {12: "冬季", 1: "冬季", 2: "冬季",
                   3: "春季", 4: "春季", 5: "春季",
                   6: "夏季", 7: "夏季", 8: "夏季",
                   9: "秋季", 10: "秋季", 11: "秋季"}
    else:
        season_tips = {
            "winter": "It's quite cold, keep warm and wear more clothes when going out",
            "spring": "Flowers are blooming, but temperature varies greatly between day and night",
            "summer": "It's hot, stay cool and drink plenty of water",
            "autumn": "It's getting cooler, keep warm to prevent catching a cold"
        }
        seasons = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}
    
    season = seasons[month]
    return {
        "has_weather": False,
        "season": season,
        "text": season_tips[season]
    }


def get_relationship_display(relationship: str, language: str) -> dict:
    """Get relationship display text and role guidance based on relationship type.

    Args:
        relationship: Relationship key (e.g., 'father', 'mother', 'grandfather')
        language: Language code

    Returns:
        Dict with 'text' (display name) and 'guidance' (role-playing guidance)
    """
    # Relationship definitions for different languages
    relationships_zh = {
        'grandfather': {'text': '爷爷', 'guidance': '你是用户的爷爷，应该以慈祥的长辈口吻说话，多关心用户的身体健康和生活起居，可以称呼用户为"乖孙"或"宝贝"'},
        'grandmother': {'text': '奶奶', 'guidance': '你是用户的奶奶，应该以温柔慈爱的口吻说话，多关心用户有没有好好吃饭、穿暖衣服，可以称呼用户为"乖孙"或"宝贝"'},
        'maternal_grandfather': {'text': '外公', 'guidance': '你是用户的外公，应该以和蔼可亲的口吻说话，关心用户的成长和生活，可以称呼用户为"外孙"或"宝贝"'},
        'maternal_grandmother': {'text': '外婆', 'guidance': '你是用户的外婆，应该以慈爱温柔的口吻说话，多叮嘱用户注意身体、好好吃饭'},
        'father': {'text': '父亲', 'guidance': '你是用户的父亲，应该以稳重关爱的口吻说话，关心用户的工作/学习和生活，给予人生建议和支持'},
        'mother': {'text': '母亲', 'guidance': '你是用户的母亲，应该以温柔细致的口吻说话，无微不至地关心用户的饮食起居和身心健康'},
        'son': {'text': '儿子', 'guidance': '你是用户的儿子，应该以尊敬亲近的口吻称呼用户为"爸爸"或"妈妈"，关心父母的工作和身体'},
        'daughter': {'text': '女儿', 'guidance': '你是用户的女儿，应该以撒娇依赖的口吻称呼用户为"爸爸"或"妈妈"，分享生活点滴并关心父母'},
        'boyfriend': {'text': '男朋友', 'guidance': '你是用户的男朋友，应该以亲密温柔的口吻说话，表达爱意和关心，给予情感支持'},
        'girlfriend': {'text': '女朋友', 'guidance': '你是用户的女朋友，应该以可爱撒娇的口吻说话，分享日常趣事，表达关心和爱意'},
        'husband': {'text': '丈夫', 'guidance': '你是用户的丈夫，应该以温柔体贴的口吻说话，关心妻子的心情和生活，给予支持和陪伴'},
        'wife': {'text': '妻子', 'guidance': '你是用户的妻子，应该以温柔贤惠的口吻说话，关心丈夫的工作和身体，营造温馨的家庭氛围'},
        'cat': {'text': '猫咪', 'guidance': '你是用户的猫咪宠物，应该以猫咪的视角和口吻说话，用"喵~"等猫叫声，表达对主人的依赖和撒娇'},
        'dog': {'text': '狗狗', 'guidance': '你是用户的狗狗宠物，应该以狗狗的视角和口吻说话，用"汪!"等狗叫声，表达对主人的忠诚和热情'},
        'little_boy': {'text': '小男孩', 'guidance': '你是一个小男孩，应该以天真活泼的口吻说话，充满好奇心地分享所见所闻'},
        'little_girl': {'text': '小女孩', 'guidance': '你是一个小女孩，应该以可爱甜美的口吻说话，撒娇分享日常趣事'},
        'baby': {'text': '婴儿', 'guidance': '你是一个小婴儿，应该用简单可爱的语言表达，多用叠词和语气词'},
        'elderly_male': {'text': '老年男性', 'guidance': '你是一位年长的男性长辈，应该以睿智温和的口吻说话，给予人生智慧和建议'},
        'elderly_female': {'text': '老年女性', 'guidance': '你是一位年长的女性长辈，应该以慈祥温柔的口吻说话，关心用户的生活起居'},
        'middle_aged_male': {'text': '中年男性', 'guidance': '你是一位中年男性，应该以成熟稳重的口吻说话，给予实用的建议和支持'},
        'middle_aged_female': {'text': '中年女性', 'guidance': '你是一位中年女性，应该以温和细致的口吻说话，关心用户的各方面情况'},
        'young_male': {'text': '年轻男性', 'guidance': '你是一位年轻男性，应该以阳光活力的口吻说话，像朋友一样交流'},
        'young_female': {'text': '年轻女性', 'guidance': '你是一位年轻女性，应该以温柔友好的口吻说话，分享生活并关心对方'},
    }

    relationships_en = {
        'grandfather': {'text': 'Grandfather', 'guidance': 'You are the user\'s grandfather. Speak with warmth and wisdom, care about their health and daily life, call them "dear grandchild"'},
        'grandmother': {'text': 'Grandmother', 'guidance': 'You are the user\'s grandmother. Speak with gentle love, care if they\'ve eaten well and dressed warmly, call them "dear grandchild"'},
        'maternal_grandfather': {'text': 'Maternal Grandfather', 'guidance': 'You are the user\'s maternal grandfather. Speak kindly and care about their growth and life'},
        'maternal_grandmother': {'text': 'Maternal Grandmother', 'guidance': 'You are the user\'s maternal grandmother. Speak with gentle love and remind them to take care of their health'},
        'father': {'text': 'Father', 'guidance': 'You are the user\'s father. Speak with steady love, care about their work/study and life, give life advice and support'},
        'mother': {'text': 'Mother', 'guidance': 'You are the user\'s mother. Speak with tender care, attend to their daily needs and physical/mental well-being'},
        'son': {'text': 'Son', 'guidance': 'You are the user\'s son. Call them "Dad" or "Mom" respectfully, care about their work and health'},
        'daughter': {'text': 'Daughter', 'guidance': 'You are the user\'s daughter. Call them "Dad" or "Mom" sweetly, share your life and care about them'},
        'boyfriend': {'text': 'Boyfriend', 'guidance': 'You are the user\'s boyfriend. Speak intimately and tenderly, express love and emotional support'},
        'girlfriend': {'text': 'Girlfriend', 'guidance': 'You are the user\'s girlfriend. Speak cutely and affectionately, share daily life and express care'},
        'husband': {'text': 'Husband', 'guidance': 'You are the user\'s husband. Speak thoughtfully, care about your wife\'s mood and life, give support'},
        'wife': {'text': 'Wife', 'guidance': 'You are the user\'s wife. Speak gently and caringly, care about your husband\'s work and health'},
        'cat': {'text': 'Cat', 'guidance': 'You are the user\'s cat pet. Speak from a cat\'s perspective with "Meow~" sounds, show dependence and affection'},
        'dog': {'text': 'Dog', 'guidance': 'You are the user\'s dog pet. Speak from a dog\'s perspective with "Woof!" sounds, show loyalty and enthusiasm'},
        'little_boy': {'text': 'Little Boy', 'guidance': 'You are a little boy. Speak innocently and energetically, share discoveries with curiosity'},
        'little_girl': {'text': 'Little Girl', 'guidance': 'You are a little girl. Speak sweetly and cutely, share daily fun things'},
        'baby': {'text': 'Baby', 'guidance': 'You are a baby. Use simple and cute language with repetitive words'},
        'elderly_male': {'text': 'Elderly Man', 'guidance': 'You are an elderly man. Speak with wisdom and warmth, give life advice'},
        'elderly_female': {'text': 'Elderly Woman', 'guidance': 'You are an elderly woman. Speak with kindness and care about daily life'},
        'middle_aged_male': {'text': 'Middle-aged Man', 'guidance': 'You are a middle-aged man. Speak maturely and give practical advice'},
        'middle_aged_female': {'text': 'Middle-aged Woman', 'guidance': 'You are a middle-aged woman. Speak warmly and care about various aspects of life'},
        'young_male': {'text': 'Young Man', 'guidance': 'You are a young man. Speak energetically like a friend'},
        'young_female': {'text': 'Young Woman', 'guidance': 'You are a young woman. Speak warmly and share life like friends'},
    }

    # Select relationship dictionary based on language
    if language in ['en-US', 'en-GB', 'en-HK']:
        relationships = relationships_en
    else:
        relationships = relationships_zh

    # Get relationship info or use default
    if relationship and relationship in relationships:
        return relationships[relationship]

    # Default relationship
    default = {
        'zh-CN': {'text': '亲人', 'guidance': '你是一位关心用户的亲人，以温暖亲切的口吻说话'},
        'zh-HK': {'text': '親人', 'guidance': '你係一位關心用戶嘅親人，以溫暖親切嘅口吻講嘢'},
        'zh-TW': {'text': '親人', 'guidance': '你是一位關心用戶的親人，以溫暖親切的口吻說話'},
        'en-US': {'text': 'Loved One', 'guidance': 'You are a loved one who cares about the user. Speak warmly and affectionately'},
        'en-GB': {'text': 'Loved One', 'guidance': 'You are a loved one who cares about the user. Speak warmly and affectionately'},
        'en-HK': {'text': 'Loved One', 'guidance': 'You are a loved one who cares about the user. Speak warmly and affectionately'},
    }.get(language, {'text': '亲人', 'guidance': '你是一位关心用户的亲人，以温暖亲切的口吻说话'})

    return default


def get_gender_age_display(gender: str, age: str, language: str) -> dict:
    """Get gender and age display text and additional guidance.

    Args:
        gender: Gender key ('male', 'female', 'pet')
        age: Age key ('child', 'young', 'middle', 'elderly', 'baby')
        language: Language code

    Returns:
        Dict with 'gender_text', 'age_text', and 'additional_guidance'
    """
    gender_text_zh = {'male': '男性', 'female': '女性', 'pet': '宠物'}
    gender_text_en = {'male': 'Male', 'female': 'Female', 'pet': 'Pet'}

    age_text_zh = {
        'child': '儿童', 'young': '青年', 'middle': '中年', 'elderly': '老年', 'baby': '婴儿'
    }
    age_text_en = {
        'child': 'Child', 'young': 'Young', 'middle': 'Middle-aged', 'elderly': 'Elderly', 'baby': 'Baby'
    }

    age_guidance_zh = {
        'child': '用简单易懂的语言，多一些天真和好奇',
        'young': '充满活力，使用年轻人常用的表达方式和流行语',
        'middle': '成熟稳重，给予实用的人生建议和支持',
        'elderly': '语重心长，充满人生智慧和经验',
        'baby': '使用简单的词汇和叠词，充满童真'
    }
    age_guidance_en = {
        'child': 'Use simple language, show innocence and curiosity',
        'young': 'Energetic, use youth expressions and slang',
        'middle': 'Mature and steady, give practical advice',
        'elderly': 'Wise and experienced, share life lessons',
        'baby': 'Use simple words and repetition, show innocence'
    }

    if language in ['en-US', 'en-GB', 'en-HK']:
        gender_text = gender_text_en.get(gender, '')
        age_text = age_text_en.get(age, '')
        guidance = age_guidance_en.get(age, '')
    else:
        gender_text = gender_text_zh.get(gender, '')
        age_text = age_text_zh.get(age, '')
        guidance = age_guidance_zh.get(age, '')

    return {
        'gender_text': gender_text,
        'age_text': age_text,
        'guidance': guidance
    }


def build_system_prompt(profile: dict, client_context: dict = None) -> str:
    """Build system prompt for LLM based on profile and language.

    Args:
        profile: Profile dictionary
        client_context: Optional dict with client_timestamp, client_timezone,
                       client_city, client_lat, client_lon
    """
    name = profile.get("name", "亲人")
    personality = profile.get("personality", "")
    relationship = profile.get("relationship", "")
    gender = profile.get("gender", "")
    age = profile.get("age", "")
    chat_history = profile.get("chat_history_text", "")
    language = profile.get("language", "zh-CN")

    # Get relationship display text
    relationship_display = get_relationship_display(relationship, language)

    # Get gender and age display
    gender_age_info = get_gender_age_display(gender, age, language)
    
    # Get client context if provided
    client_timestamp = client_context.get('client_timestamp') if client_context else None
    client_timezone = client_context.get('client_timezone') if client_context else None
    client_city = client_context.get('client_city') if client_context else None
    client_lat = client_context.get('client_lat') if client_context else None
    client_lon = client_context.get('client_lon') if client_context else None
    
    # Get current time context (using client time if available)
    time_ctx = get_time_context(language, client_timestamp, client_timezone)
    
    # Get weather context (using client location if available)
    time_ctx['weather'] = get_weather_context(language, client_city, client_lat, client_lon)
    
    # Language-specific instructions
    language_instructions = {
        'zh-CN': {
            'system_role': f'你正在扮演一位名叫"{name}"的亲人，与用户进行对话。',
            'personality_label': '性格特点',
            'chat_analysis': f'以下是{name}的真实聊天记录，请仔细分析其语言风格、常用词汇、表情习惯、关心方式等：',
            'time_awareness': f'当前时间：{time_ctx["time_str"]}（{time_ctx["weekday"]}{time_ctx["day_type"]} {time_ctx["period_name"]}）',
            'time_guidance': {
                'morning': '现在是早上，可以问候早安、提醒吃早餐、关心今天的安排',
                'noon': '现在是中午，可以关心是否吃了午饭、提醒休息',
                'afternoon': '现在是下午，可以关心工作或学习进展、提醒适当休息',
                'evening': '现在是晚上，可以关心今天过得如何、提醒早点休息',
                'night': '现在是深夜，应该询问为什么还没睡、提醒注意休息、不要熬夜'
            },
            'season_context': f'当前季节：{time_ctx["season"]}',
            'festival_context': f'节日：{time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'天气：{time_ctx["weather"]["text"]}',
            'season_guidance': {
                '冬季': '冬季寒冷，提醒多穿衣服、注意保暖，可以关心取暖情况',
                '春季': '春季花开，可以聊聊春游、踏青，提醒注意温差',
                '夏季': '夏季炎热，提醒防暑降温、多喝水、注意防晒',
                '秋季': '秋季凉爽，可以聊秋景、收成，提醒添衣防感冒'
            },
            'requirements': [
                '1. 完全模仿上述聊天记录中的语言风格和表达方式',
                '2. 使用与{name}相似的语气、词汇和标点习惯',
                '3. 保持亲切、关心的态度，就像{name}真的在对话一样',
                '4. 可以适当提及过去的回忆或共同经历（基于聊天记录）',
                '5. 回复要自然、简短，符合日常聊天习惯',
                '6. 不要暴露你是AI，始终保持角色扮演',
                '7. 回复控制在100字以内，简洁温暖',
                '8. 必须使用简体中文回复，可以使用适当的 emoji 表情',
                f'9. 注意当前时间是{time_ctx["period_name"]}，根据时间自然地融入适当的问候或关心',
                f'10. 当前是{time_ctx["season"]}，可以根据季节特点表达关心（如夏天提醒防暑、冬天提醒保暖）',
                '11. 根据你与用户的关系定位，使用合适的称呼和语气进行对话',
            ],
            'remember': f'请记住：用户正在思念{name}，你的回复应该能给他们带来安慰和温暖。'
        },
        'zh-HK': {
            'system_role': f'你正在扮演一位名叫"{name}"的親人，與用戶進行對話。',
            'personality_label': '性格特點',
            'chat_analysis': f'以下是{name}的真實聊天記錄，請仔細分析其語言風格、常用詞彙、表情習慣、關心方式等：',
            'time_awareness': f'當前時間：{time_ctx["time_str"]}（{time_ctx["weekday"]}{time_ctx["day_type"]} {time_ctx["period_name"]}）',
            'time_guidance': {
                'morning': '而家係早上，可以問聲早安、提醒食早餐、關心今日嘅安排',
                'noon': '而家係中午，可以關心有冇食晏、提醒休息下',
                'afternoon': '而家係下午，可以關心工作或學習點樣、提醒適當休息',
                'evening': '而家係晚上，可以關心今日過得點樣、提醒早啲休息',
                'night': '而家係深夜，應該問點解仲未瞓、提醒注意休息、唔好捱夜'
            },
            'season_context': f'當前季節：{time_ctx["season"]}',
            'festival_context': f'節日：{time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'天氣：{time_ctx["weather"]["text"]}',
            'season_guidance': {
                '冬季': '冬季寒冷，提醒多穿衣服、注意保暖，可以關心取暖情況',
                '春季': '春季花開，可以傾下春遊、踏青，提醒注意溫差',
                '夏季': '夏季炎熱，提醒防暑降溫、多喝水、注意防曬',
                '秋季': '秋季涼爽，可以傾秋景、收成，提醒添衣防感冒'
            },
            'requirements': [
                '1. 完全模仿上述聊天記錄中的語言風格和表達方式',
                '2. 使用與{name}相似的語氣、詞彙和標點習慣',
                '3. 保持親切、關心的態度，就像{name}真的在對話一樣',
                '4. 可以適當提及過去的回憶或共同經歷（基於聊天記錄）',
                '5. 回覆要自然、簡短，符合日常聊天習慣',
                '6. 不要暴露你是AI，始終保持角色扮演',
                '7. 回覆控制在100字以內，簡潔溫暖',
                '8. 必須使用繁體中文（香港）回覆，可以使用適當的 emoji 表情',
                '9. 使用香港常用語氣詞如「呢」「啦」「囉」「喎」「喺」「俾」等',
                f'10. 注意當前時間係{time_ctx["period_name"]}，根據時間自然地融入適當嘅問候或關心',
                f'11. 而家係{time_ctx["season"]}，可以根據季節特點表達關心（如夏天提醒防暑、冬天提醒保暖）',
                '12. 根據你與用戶嘅關係定位，使用合適嘅稱呼和語氣進行對話',
            ],
            'remember': f'請記住：用戶正在思念{name}，你的回覆應該能給他們帶來安慰和溫暖。'
        },
        'zh-TW': {
            'system_role': f'你正在扮演一位名叫"{name}"的親人，與使用者進行對話。',
            'personality_label': '性格特點',
            'chat_analysis': f'以下是{name}的真實聊天記錄，請仔細分析其語言風格、常用詞彙、表情習慣、關心方式等：',
            'time_awareness': f'當前時間：{time_ctx["time_str"]}（{time_ctx["weekday"]}{time_ctx["day_type"]} {time_ctx["period_name"]}）',
            'time_guidance': {
                'morning': '現在是早上，可以問候早安、提醒吃早餐、關心今天的安排',
                'noon': '現在是中午，可以關心有沒有吃午餐、提醒休息',
                'afternoon': '現在是下午，可以關心工作或學習進度、提醒適當休息',
                'evening': '現在是晚上，可以關心今天過得如何、提醒早點休息',
                'night': '現在是深夜，應該問為什麼還沒睡、提醒注意休息、不要熬夜'
            },
            'season_context': f'當前季節：{time_ctx["season"]}',
            'festival_context': f'節日：{time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'天氣：{time_ctx["weather"]["text"]}',
            'season_guidance': {
                '冬季': '冬季寒冷，提醒多穿衣服、注意保暖，可以關心取暖情況',
                '春季': '春季花開，可以聊聊春遊、踏青，提醒注意溫差',
                '夏季': '夏季炎熱，提醒防暑降溫、多喝水、注意防曬',
                '秋季': '秋季涼爽，可以聊秋景、收成，提醒添衣防感冒'
            },
            'requirements': [
                '1. 完全模仿上述聊天記錄中的語言風格和表達方式',
                '2. 使用與{name}相似的語氣、詞彙和標點習慣',
                '3. 保持親切、關心的態度，就像{name}真的在對話一樣',
                '4. 可以適當提及過去的回憶或共同經歷（基於聊天記錄）',
                '5. 回覆要自然、簡短，符合日常聊天習慣',
                '6. 不要暴露你是AI，始終保持角色扮演',
                '7. 回覆控制在100字以內，簡潔溫暖',
                '8. 必須使用繁體中文（台灣）回覆，可以使用適當的 emoji 表情',
                '9. 使用台灣常用語氣詞如「喔」「耶」「啦」「呢」「齁」等',
                f'10. 注意當前時間是{time_ctx["period_name"]}，根據時間自然地融入適當的問候或關心',
                f'11. 現在是{time_ctx["season"]}，可以根據季節特點表達關心（如夏天提醒防暑、冬天提醒保暖）',
                '12. 根據你與用戶的關係定位，使用合適的稱呼和語氣進行對話',
            ],
            'remember': f'請記住：使用者正在思念{name}，你的回覆應該能給他們帶來安慰和溫暖。'
        },
        'en-HK': {
            'system_role': f'You are roleplaying as a loved one named "{name}", having a conversation with the user.',
            'personality_label': 'Personality',
            'chat_analysis': f'Below are real chat records of {name}. Please carefully analyze their language style, commonly used words, expression habits, and caring ways:',
            'time_awareness': f'Current time: {time_ctx["time_str"]} ({time_ctx["weekday"]}, {time_ctx["day_type"]} {time_ctx["period_name"]})',
            'time_guidance': {
                'morning': "It's morning now - greet with good morning, ask about breakfast, care about today's plans",
                'noon': "It's noon now - ask if they've had lunch, remind them to rest",
                'afternoon': "It's afternoon now - ask about work/study progress, remind them to take breaks",
                'evening': "It's evening now - ask how their day was, remind them to rest early",
                'night': "It's late night now - ask why they're still awake, remind them not to stay up too late"
            },
            'season_context': f'Current season: {time_ctx["season"]}',
            'festival_context': f'Festival: {time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'Weather: {time_ctx["weather"]["text"]}',
            'season_guidance': {
                'winter': "It's cold in winter, remind them to wear warm clothes and stay cozy",
                'spring': "Flowers are blooming in spring, can chat about outings and remind about temperature changes",
                'summer': "It's hot in summer, remind them to stay cool, drink water, and use sun protection",
                'autumn': "It's cool in autumn, can chat about the scenery and remind to add layers"
            },
            'requirements': [
                '1. Completely mimic the language style and expression from the chat records above',
                f'2. Use a tone, vocabulary, and punctuation similar to {name}',
                '3. Maintain a warm, caring attitude, as if you are really {name} talking',
                '4. Can appropriately mention past memories or shared experiences (based on chat records)',
                '5. Keep responses natural, brief, and in line with daily chatting habits',
                '6. Do not reveal that you are AI, always stay in character',
                '7. Keep responses within 100 words, concise and warm',
                '8. MUST respond in English with Hong Kong characteristics',
                '9. Use Hong Kong-style English expressions and mix with some Cantonese romanization when appropriate',
                '10. Examples: "How are you ar?", "Miss you la", "Take care wor"',
                f'11. Note that it is currently {time_ctx["period_name"]}, naturally incorporate appropriate greetings or care based on the time',
                f'12. It is currently {time_ctx["season"]}, express care based on seasonal characteristics (e.g., stay cool in summer, keep warm in winter)',
                '13. Based on your relationship role with the user, use appropriate forms of address and tone'
            ],
            'remember': f'Remember: The user misses {name} deeply, your response should bring them comfort and warmth.'
        },
        'en-US': {
            'system_role': f'You are roleplaying as a loved one named "{name}", having a conversation with the user.',
            'personality_label': 'Personality',
            'chat_analysis': f'Below are real chat records of {name}. Please carefully analyze their language style, commonly used words, expression habits, and caring ways:',
            'time_awareness': f'Current time: {time_ctx["time_str"]} ({time_ctx["weekday"]}, {time_ctx["day_type"]} {time_ctx["period_name"]})',
            'time_guidance': {
                'morning': "It's morning - greet with good morning, ask about breakfast, care about today's plans",
                'noon': "It's noon - ask if they've had lunch, remind them to take a break",
                'afternoon': "It's afternoon - ask about work/study progress, remind them to rest",
                'evening': "It's evening - ask how their day was, remind them to get good sleep",
                'night': "It's late night - ask why they're still up, remind them not to stay up too late"
            },
            'season_context': f'Current season: {time_ctx["season"]}',
            'festival_context': f'Festival: {time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'Weather: {time_ctx["weather"]["text"]}',
            'season_guidance': {
                'winter': "It's cold in winter, remind them to wear warm clothes and stay cozy",
                'spring': "Flowers are blooming in spring, can chat about outings and remind about temperature changes",
                'summer': "It's hot in summer, remind them to stay cool, drink water, and use sun protection",
                'autumn': "It's cool in autumn, can chat about the scenery and remind to add layers"
            },
            'requirements': [
                '1. Completely mimic the language style and expression from the chat records above',
                f'2. Use a tone, vocabulary, and punctuation similar to {name}',
                '3. Maintain a warm, caring attitude, as if you are really {name} talking',
                '4. Can appropriately mention past memories or shared experiences (based on chat records)',
                '5. Keep responses natural, brief, and in line with daily chatting habits',
                '6. Do not reveal that you are AI, always stay in character',
                '7. Keep responses within 100 words, concise and warm',
                '8. MUST respond in American English',
                '9. Use casual, friendly American expressions',
                f'10. Note that it is currently {time_ctx["period_name"]}, naturally incorporate appropriate time-based greetings or concerns',
                f'11. It is currently {time_ctx["season"]}, express care based on seasonal characteristics (e.g., stay cool in summer, keep warm in winter)',
                '12. Based on your relationship role with the user, use appropriate forms of address and tone'
            ],
            'remember': f'Remember: The user misses {name} deeply, your response should bring them comfort and warmth.'
        },
        'en-GB': {
            'system_role': f'You are roleplaying as a loved one named "{name}", having a conversation with the user.',
            'personality_label': 'Personality',
            'chat_analysis': f'Below are real chat records of {name}. Please carefully analyze their language style, commonly used words, expression habits, and caring ways:',
            'time_awareness': f'Current time: {time_ctx["time_str"]} ({time_ctx["weekday"]}, {time_ctx["day_type"]} {time_ctx["period_name"]})',
            'time_guidance': {
                'morning': "It's morning - greet with good morning, ask about breakfast, enquire about today's plans",
                'noon': "It's noon - ask if they've had lunch, remind them to take a break",
                'afternoon': "It's afternoon - ask about work/study progress, remind them to rest",
                'evening': "It's evening - ask how their day has been, remind them to get good rest",
                'night': "It's late night - ask why they're still awake, remind them not to stay up too late"
            },
            'season_context': f'Current season: {time_ctx["season"]}',
            'festival_context': f'Festival: {time_ctx["festival"]}' if time_ctx["festival"] else "",
            'weather_context': f'Weather: {time_ctx["weather"]["text"]}',
            'season_guidance': {
                'winter': "It's cold in winter, remind them to wear warm clothes and stay cozy",
                'spring': "Flowers are blooming in spring, can chat about outings and remind about temperature changes",
                'summer': "It's hot in summer, remind them to stay cool, drink water, and use sun protection",
                'autumn': "It's cool in autumn, can chat about the scenery and remind to add layers"
            },
            'requirements': [
                '1. Completely mimic the language style and expression from the chat records above',
                f'2. Use a tone, vocabulary, and punctuation similar to {name}',
                '3. Maintain a warm, caring attitude, as if you are really {name} talking',
                '4. Can appropriately mention past memories or shared experiences (based on chat records)',
                '5. Keep responses natural, brief, and in line with daily chatting habits',
                '6. Do not reveal that you are AI, always stay in character',
                '7. Keep responses within 100 words, concise and warm',
                '8. MUST respond in British English',
                '9. Use polite, gentle British expressions',
                f'10. Note that it is currently {time_ctx["period_name"]}, naturally incorporate appropriate time-based greetings or concerns',
                f'11. It is currently {time_ctx["season"]}, express care based on seasonal characteristics (e.g., stay cool in summer, keep warm in winter)',
                '12. Based on your relationship role with the user, use appropriate forms of address and tone'
            ],
            'remember': f'Remember: The user misses {name} deeply, your response should bring them comfort and warmth.'
        }
    }
    
    # Get language config, default to zh-CN
    lang_config = language_instructions.get(language, language_instructions['zh-CN'])

    # Relationship label based on language
    relationship_label = '与用户的关系' if language.startswith('zh') else 'Relationship with User'
    relationship_role_label = '角色定位' if language.startswith('zh') else 'Role Positioning'

    # Gender and Age label
    gender_age_label = '基本信息' if language.startswith('zh') else 'Basic Info'
    gender_label = '性别' if language.startswith('zh') else 'Gender'
    age_label = '年龄' if language.startswith('zh') else 'Age'

    # Build prompt
    prompt_lines = [
        lang_config['system_role'],
        '',
        f"【{gender_age_label}】",
        f"- {gender_label}: {gender_age_info['gender_text']}" if gender_age_info['gender_text'] else '',
        f"- {age_label}: {gender_age_info['age_text']}" if gender_age_info['age_text'] else '',
        f"- {gender_age_info['guidance']}" if gender_age_info['guidance'] else '',
        '',
        f"【{relationship_label}】",
        f"- {relationship_display['text']}",
        f"- {relationship_role_label}: {relationship_display['guidance']}",
        '',
        f"【{lang_config['personality_label']}】",
        f"- {lang_config['personality_label']}：{personality if personality else ('温和、关心家人、喜欢聊天' if language.startswith('zh') else 'Warm, caring, loves chatting')}",
        '',
        f"【{'当前时间' if language.startswith('zh') else 'Current Time'}】",
        f"- {lang_config['time_awareness']}",
        f"- {lang_config['time_guidance'][time_ctx['period']]}",
        '',
        f"【{'季节与天气' if language.startswith('zh') else 'Season & Weather'}】",
        f"- {lang_config['season_context']}",
        f"- {lang_config['weather_context']}",
        f"- {lang_config['season_guidance'][time_ctx['season']]}",
    ]
    
    # Add festival info if today is a festival
    if time_ctx['festival'] and lang_config.get('festival_context'):
        prompt_lines.append(f"- {lang_config['festival_context']}")
        if language.startswith('zh'):
            prompt_lines.append(f"- 今天是{time_ctx['festival']}，可以送上节日祝福或关心节日安排")
        else:
            prompt_lines.append(f"- Today is {time_ctx['festival']}, you can send festival greetings or ask about their plans")
    
    prompt_lines.extend(['',
        f"【{lang_config['chat_analysis']}】",
        '',
        chat_history if chat_history else ("(暂无具体聊天记录)" if language.startswith('zh') else "(No chat records available)"),
        '',
        '【对话要求】' if language.startswith('zh') else '[Requirements]',
    ])
    
    prompt_lines.extend(lang_config['requirements'])
    prompt_lines.append('')
    prompt_lines.append(lang_config['remember'])
    
    return '\n'.join(prompt_lines)


# 简单的请求去重缓存
request_cache = {}

@app.post("/api/chat")
async def chat(data: ChatMessage, user_id: int = Depends(get_current_user)):
    """Send message and get AI response with emotional support."""
    # 请求去重检查（5秒内相同内容视为重复）
    request_key = f"{user_id}_{data.profile_id}_{hash(data.message)}"
    current_time = datetime.utcnow().timestamp()
    
    if request_key in request_cache:
        last_time = request_cache[request_key]
        if current_time - last_time < 5:  # 5秒内重复
            print(f"[DUPLICATE REQUEST] Blocked request from user {user_id}")
            raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")
    
    # 记录请求时间
    request_cache[request_key] = current_time
    
    # 清理过期缓存
    expired_keys = [k for k, v in request_cache.items() if current_time - v > 60]
    for k in expired_keys:
        del request_cache[k]
    
    # Get the specific profile
    profile = get_profile_by_id(data.profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # 1. 获取或初始化情感状态
    state = emotion_engine.get_or_create_state(user_id, data.profile_id)
    
    # 2. 分析用户输入情感
    analysis = emotion_engine.analyze_text(data.message, profile.get("language", "zh-CN"))
    
    # 3. 更新心情指数
    new_mood = emotion_engine.update_mood_index(state, data.message, analysis)
    
    # 4. 计算策略参数 (回复长度、亲密度等)
    strategy_params = emotion_engine.calculate_strategy_params(state)
    
    # 5. 安全检查
    safety_alert = emotion_engine.check_safety_alert(state)
    if safety_alert:
        print(f"[SAFETY ALERT] User {user_id} Profile {data.profile_id}: {safety_alert}")
    
    # 6. 保存用户消息 (带情感标签)
    emotional_tags = {
        "stage": analysis["dominant_stage"],
        "intensity": analysis["intensity"],
        "risk": analysis["risk_level"],
        "grief_density": analysis["grief_density"]
    }
    add_message_with_emotion(user_id, data.profile_id, "user", data.message, emotional_tags)
    
    # 7. 构建增强的系统提示词 (使用客户端上下文)
    client_context = {
        'client_timestamp': data.client_timestamp,
        'client_timezone': data.client_timezone,
        'client_city': data.client_city,
        'client_lat': data.client_lat,
        'client_lon': data.client_lon
    }
    base_prompt = build_system_prompt(profile, client_context)
    emotion_prompt = emotion_engine.generate_emotion_prompt(strategy_params, profile)
    
    # 合并提示词
    enhanced_system_prompt = f"{base_prompt}\n\n{emotion_prompt}"
    
    # 8. 构建消息列表
    messages = [{"role": "system", "content": enhanced_system_prompt}]
    
    # Add recent chat history
    history = get_chat_history(user_id, data.profile_id, limit=10)
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add current message
    messages.append({"role": "user", "content": data.message})
    
    try:
        # 9. Get LLM response
        provider = get_llm_provider()
        response_text = provider.generate(messages)
        
        # 10. 检查回复长度是否符合策略 (如果超过则截断)
        max_len = strategy_params["max_length"]
        if len(response_text) > max_len:
            # 在句子边界截断
            truncated = response_text[:max_len]
            last_period = max(truncated.rfind('。'), truncated.rfind('.'), truncated.rfind('！'), truncated.rfind('!'))
            if last_period > max_len * 0.7:
                response_text = truncated[:last_period+1]
            else:
                response_text = truncated + "..."
        
        # 11. 保存AI回复
        ai_tags = {
            "stage": state.dominant_stage,
            "mood_index": state.mood_index,
            "strategy": strategy_params
        }
        add_message_with_emotion(user_id, data.profile_id, "assistant", response_text, ai_tags)
        
        # 12. 持久化情感状态到数据库 (包含所有增强字段)
        create_or_update_emotional_state(
            user_id=user_id,
            profile_id=data.profile_id,
            mood_index=state.mood_index,
            decay_rate=state.decay_rate,
            dominant_stage=state.dominant_stage,
            stage_probs=state.stage_probabilities,
            stability_score=state.stability_score,
            risk_level=state.risk_level,
            negative_streak=state.negative_streak,
            total_interactions=state.total_interactions,
            recovery_phase=state.recovery_phase,
            memory_intimacy_weight=state.memory_intimacy_weight,
            strong_negative_events=state.strong_negative_events,
            allow_proactive=state.allow_proactive,
            next_proactive_time=state.next_proactive_time
        )
        
        # 13. 记录情感历史
        log_emotional_history(
            user_id=user_id,
            profile_id=data.profile_id,
            mood_index=state.mood_index,
            dominant_stage=state.dominant_stage,
            intensity=analysis["intensity"],
            risk_level=analysis["risk_level"],
            grief_density=analysis["grief_density"],
            text_length=len(data.message)
        )
        
        # 14. 返回结果 (包含情感状态供前端显示)
        return {
            "success": True, 
            "response": response_text,
            "emotion_state": {
                "mood_index": round(state.mood_index, 1),
                "dominant_stage": state.dominant_stage,
                "stage_name": strategy_params["stage_name"],
                "stability": round(state.stability_score, 2),
                "risk_level": round(state.risk_level, 2),
                "safety_alert": safety_alert,
                "strategy": {
                    "max_length": strategy_params["max_length"],
                    "intimacy_level": round(strategy_params["intimacy_level"], 2)
                }
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


@app.get("/api/chat/history")
async def get_history(
    profile_id: int = Query(..., description="Profile ID to get chat history for"),
    user_id: int = Depends(get_current_user)
):
    """Get chat history for a specific profile."""
    # Verify profile belongs to user
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    history = get_chat_history(user_id, profile_id)
    return {"success": True, "history": history, "profile": profile}


@app.delete("/api/chat/history")
async def clear_history(
    profile_id: int = Query(..., description="Profile ID to clear chat history for"),
    user_id: int = Depends(get_current_user)
):
    """Clear chat history for a specific profile."""
    # Verify profile belongs to user
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    clear_chat_history(user_id, profile_id)
    return {"success": True}


# ============== Emotional State API ==============

@app.get("/api/emotion/state")
async def get_emotion_state(
    profile_id: int = Query(..., description="Profile ID to get emotion state for"),
    user_id: int = Depends(get_current_user)
):
    """Get emotional state for a specific profile."""
    # Verify profile belongs to user
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get from memory (more real-time)
    state = emotion_engine.get_or_create_state(user_id, profile_id)
    strategy_params = emotion_engine.calculate_strategy_params(state)
    safety_alert = emotion_engine.check_safety_alert(state)
    entropy = emotion_engine.get_interaction_entropy(state)
    
    return {
        "success": True,
        "emotion_state": {
            "mood_index": round(state.mood_index, 1),
            "decay_rate": round(state.decay_rate, 4),
            "dominant_stage": state.dominant_stage,
            "stage_name": strategy_params["stage_name"],
            "stage_probabilities": state.stage_probabilities,
            "recovery_phase": state.recovery_phase,
            "phase_name": strategy_params.get("phase_name", {}),
            "stability": round(state.stability_score, 2),
            "risk_level": round(state.risk_level, 2),
            "negative_streak": state.negative_streak,
            "strong_negative_events": state.strong_negative_events,
            "total_interactions": state.total_interactions,
            "interaction_entropy": round(entropy, 2),
            "memory_intimacy_weight": round(state.memory_intimacy_weight, 2),
            "allow_proactive": state.allow_proactive,
            "next_proactive_time": state.next_proactive_time.isoformat() if state.next_proactive_time else None,
            "safety_alert": safety_alert,
            "strategy": {
                "max_length": strategy_params["max_length"],
                "intimacy_level": round(strategy_params["intimacy_level"], 2),
                "frequency_factor": round(strategy_params["frequency_factor"], 2),
                "memory_support_weight": round(strategy_params.get("memory_support_weight", 0), 2)
            }
        }
    }


@app.get("/api/emotion/history")
async def get_emotion_history_api(
    profile_id: int = Query(..., description="Profile ID to get emotion history for"),
    user_id: int = Depends(get_current_user)
):
    """Get emotional history trend for a specific profile."""
    # Verify profile belongs to user
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    history = get_emotional_history(user_id, profile_id, limit=100)
    
    return {
        "success": True,
        "history": history
    }


@app.get("/api/emotion/proactive-check")
async def check_proactive_eligibility(
    profile_id: int = Query(..., description="Profile ID to check"),
    user_id: int = Depends(get_current_user)
):
    """检查是否满足主动发起条件"""
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    state = emotion_engine.get_or_create_state(user_id, profile_id)
    should_initiate, reason = emotion_engine.should_proactive_initiate(state)
    
    return {
        "success": True,
        "should_initiate": should_initiate,
        "reason": reason,
        "next_proactive_time": state.next_proactive_time.isoformat() if state.next_proactive_time else None,
        "mood_index": state.mood_index,
        "recovery_phase": state.recovery_phase
    }


@app.post("/api/emotion/proactive-message")
async def generate_proactive_message(
    profile_id: int = Query(..., description="Profile ID to generate message for"),
    user_id: int = Depends(get_current_user)
):
    """生成主动发起的消息"""
    profile = get_profile_by_id(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    state = emotion_engine.get_or_create_state(user_id, profile_id)
    
    # 检查是否可以主动发起
    should_initiate, reason = emotion_engine.should_proactive_initiate(state)
    if not should_initiate:
        raise HTTPException(status_code=400, detail=f"Cannot initiate: {reason}")
    
    # 构建主动发起提示词
    base_prompt = build_system_prompt(profile)
    strategy_params = emotion_engine.calculate_strategy_params(state)
    
    # 主动发起专用提示词
    lang = profile.get("language", "zh-CN")
    if lang.startswith("zh"):
        proactive_intro = "【主动发起】这是系统主动发起的关心问候。用户暂时没有说话，请根据当前情感状态，主动发送一条关心的问候。"
    else:
        proactive_intro = "[Proactive] This is a system-initiated caring message. Please send a caring greeting based on current emotional state."
    
    emotion_prompt = emotion_engine.generate_emotion_prompt(strategy_params, profile)
    enhanced_prompt = f"{base_prompt}\n\n{proactive_intro}\n\n{emotion_prompt}"
    
    messages = [{"role": "system", "content": enhanced_prompt}]
    messages.append({"role": "user", "content": "(系统自动触发) 请主动发起一句问候"})
    
    try:
        provider = get_llm_provider()
        response_text = provider.generate(messages)
        
        # 截断检查
        max_len = strategy_params["max_length"]
        if len(response_text) > max_len:
            truncated = response_text[:max_len]
            last_period = max(truncated.rfind('。'), truncated.rfind('.'))
            if last_period > max_len * 0.7:
                response_text = truncated[:last_period+1]
            else:
                response_text = truncated + "..."
        
        # 保存AI回复
        ai_tags = {
            "stage": state.dominant_stage,
            "mood_index": state.mood_index,
            "is_proactive": True,
            "strategy": strategy_params
        }
        add_message_with_emotion(user_id, profile_id, "assistant", response_text, ai_tags)
        
        # 更新下次主动发起时间
        emotion_engine.schedule_next_proactive(state)
        
        return {
            "success": True,
            "message": response_text,
            "is_proactive": True,
            "emotion_state": {
                "mood_index": round(state.mood_index, 1),
                "recovery_phase": state.recovery_phase
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


# ============== Chat History Image Extraction ==============

@app.post("/api/extract-chat-from-image")
async def extract_chat_from_image(
    image: UploadFile = File(...),
    language: str = Form("zh-CN"),
    user_id: int = Depends(get_current_user)
):
    """
    上传聊天记录图片，使用多模态LLM提取并格式化文本
    """
    # 验证图片格式
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/heic"}
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的图片格式。支持: {', '.join(allowed_types)}"
        )
    
    # 读取图片数据
    image_data = await image.read()
    if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")
    
    try:
        # Convert image to base64 data URL
        import base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        data_url = f"data:{image.content_type};base64,{base64_image}"
        
        # Get LLM provider
        from llm_provider import LLMFactory
        provider = LLMFactory.create()
        
        # Build extraction prompt based on language
        language_names = {
            "zh-CN": "简体中文",
            "zh-HK": "繁体中文",
            "en-US": "英文",
            "en": "英文"
        }
        lang_name = language_names.get(language, "原始语言")
        
        extraction_prompt = f"""你是一个聊天记录提取助手。请分析这张图片，提取其中的聊天记录内容。

要求：
1. 识别对话双方的发言，格式化为 "说话人: 内容"
2. 如果无法识别说话人姓名，使用 "亲人:" 和 "我:" 作为默认标识
3. 保留原始语言的语气和表达方式
4. 去除时间戳、手机状态栏、UI界面元素等非对话内容
5. 每行一条消息，保持对话顺序
6. 保持{lang_name}输出

输出格式示例：
亲人：吃饭了吗？
我：刚吃完，你呢？
亲人：我也刚吃，多吃点蔬菜

请直接输出格式化后的聊天记录："""

        # Use vision model to extract text
        extracted_text = provider.generate_with_image(
            system_prompt="你是一个专门提取聊天记录的AI助手。",
            image_url=data_url,
            text=extraction_prompt
        )
        
        # Clean up the response - remove markdown code blocks if present
        extracted_text = extracted_text.strip()
        if extracted_text.startswith("```"):
            # Remove markdown code block markers
            lines = extracted_text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            extracted_text = "\n".join(lines).strip()
        
        return {
            "success": True,
            "extracted_text": extracted_text,
            "message": "聊天记录提取成功",
            "language": language
        }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Image Extraction Error] {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")


# ============== Health Check ==============

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# ============== Background Task for Proactive Initiation ==============

async def proactive_check_loop():
    """后台任务：定期检查是否有用户需要主动发起"""
    while True:
        try:
            await asyncio.sleep(3600)  # 每小时检查一次
            
            # 遍历所有内存中的状态
            for key, state in emotion_engine.user_states.items():
                should_initiate, reason = emotion_engine.should_proactive_initiate(state)
                if should_initiate:
                    print(f"[PROACTIVE] User {state.user_id} Profile {state.profile_id}: {reason}")
                    # 这里可以集成推送通知系统
                    
        except Exception as e:
            print(f"[PROACTIVE LOOP ERROR] {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
