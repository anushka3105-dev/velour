
import hashlib
from datetime import datetime
from database.db import get_supabase


def hash_password(password: str) -> str:
    """SHA-256 hash a password. Never store plain text."""
    return hashlib.sha256(password.encode()).hexdigest()


def sign_up(username: str, password: str) -> dict:
    """
    Register a new user.
    Returns: {"success": True, "user": {...}}
          or {"success": False, "error": "..."}
    """
    supabase = get_supabase()
    try:
        # Check if username already taken
        existing = supabase.table("users") \
            .select("id") \
            .eq("username", username) \
            .execute()

        if existing.data:
            return {"success": False, "error": "Username already exists."}

        # Insert new user
        result = supabase.table("users").insert({
            "username":      username,
            "password_hash": hash_password(password),
            "created_at":    datetime.utcnow().isoformat(),
            "last_login":    datetime.utcnow().isoformat(),
        }).execute()

        user = result.data[0]

        # Create empty profile row for this user
        supabase.table("user_profiles").insert({"user_id": user["id"]}).execute()

        return {"success": True, "user": user}

    except Exception as e:
        return {"success": False, "error": str(e)}


def sign_in(username: str, password: str) -> dict:
    """
    Authenticate an existing user.
    Returns: {"success": True, "user": {...}}
          or {"success": False, "error": "..."}
    """
    supabase = get_supabase()
    try:
        result = supabase.table("users") \
            .select("*") \
            .eq("username", username) \
            .eq("password_hash", hash_password(password)) \
            .execute()

        if not result.data:
            return {"success": False, "error": "Invalid username or password."}

        user = result.data[0]

        # Update last login timestamp
        supabase.table("users") \
            .update({"last_login": datetime.utcnow().isoformat()}) \
            .eq("id", user["id"]) \
            .execute()

        return {"success": True, "user": user}

    except Exception as e:
        return {"success": False, "error": str(e)}


def validate_signup_form(username: str, password: str, confirm: str) -> str | None:
    """
    Validate signup form inputs.
    Returns an error string if invalid, None if valid.
    """
    if not (username and password and confirm):
        return "Please fill in all fields."
    if len(username) < 3:
        return "Username must be at least 3 characters."
    if len(password) < 6:
        return "Password must be at least 6 characters."
    if password != confirm:
        return "Passwords do not match."
    return None
