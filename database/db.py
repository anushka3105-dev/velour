

from datetime import datetime
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

_supabase_client: Client | None = None

def get_supabase() -> Client:
    """Return the shared Supabase client (singleton pattern)."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def load_profile(user_id: str) -> dict:
    """Fetch saved preferences for a user. Returns {} if none found."""
    try:
        r = get_supabase().table("user_profiles") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()
        return r.data[0] if r.data else {}
    except Exception:
        return {}


def save_profile(user_id: str, profile: dict) -> bool:
    """
    Upsert user preferences — update if row exists, insert if not.
    Returns True on success, False on failure.
    """
    try:
        supabase = get_supabase()
        existing = supabase.table("user_profiles") \
            .select("id") \
            .eq("user_id", user_id) \
            .execute()

        payload = {
            **profile,
            "user_id":    user_id,
            "updated_at": datetime.utcnow().isoformat(),
        }

        if existing.data:
            supabase.table("user_profiles") \
                .update(payload) \
                .eq("user_id", user_id) \
                .execute()
        else:
            supabase.table("user_profiles").insert(payload).execute()

        return True
    except Exception:
        return False


def load_wardrobe(user_id: str) -> list:
    """Fetch all wardrobe items for a user, newest first."""
    try:
        r = get_supabase().table("wardrobe") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("added_at", desc=True) \
            .execute()
        return r.data or []
    except Exception:
        return []


def add_wardrobe_item(user_id: str, item: dict) -> bool:
    """Insert a new wardrobe item linked to a user."""
    try:
        get_supabase().table("wardrobe").insert({
            **item,
            "user_id":  user_id,
            "added_at": datetime.utcnow().isoformat(),
        }).execute()
        return True
    except Exception:
        return False


def delete_wardrobe_item(item_id: str) -> bool:
    """Delete a wardrobe item by its UUID."""
    try:
        get_supabase().table("wardrobe") \
            .delete() \
            .eq("id", item_id) \
            .execute()
        return True
    except Exception:
        return False
