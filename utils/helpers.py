
from datetime import datetime
from config import OPTIONS, WEATHER_MAP


def get_current_season() -> str:
    """Return the current meteorological season."""
    m = datetime.now().month
    if m in [12, 1, 2]:  return "Winter"
    if m in [3, 4, 5]:   return "Spring"
    if m in [6, 7, 8]:   return "Summer"
    return "Autumn"


def weather_icon_to_category(icon: str) -> str:
    """Convert OpenWeatherMap icon string to VELOUR weather category."""
    return WEATHER_MAP.get(icon, "Cloudy")


def get_option_index(key: str, value: str) -> int:
    """
    Get the index of a value in an OPTIONS list.
    Returns 0 (first item) if value not found — safe default for st.selectbox.
    """
    options = OPTIONS.get(key, [])
    return options.index(value) if value in options else 0


def format_user_id(uuid: str) -> str:
    """Return first 8 chars of UUID in uppercase for display."""
    return str(uuid)[:8].upper()


def profile_to_ml_format(profile: dict) -> dict:
    """
    Convert sidebar profile (lowercase keys) to ML model format (Title_Case keys).
    The sidebar stores keys like 'style_preference'.
    ML models expect 'Style_Preference'.
    """
    return {
        "Weather":           profile.get("weather",           "Sunny"),
        "Occasion":          profile.get("occasion",          "Casual"),
        "Style_Preference":  profile.get("style_preference",  "Classic"),
        "Body_Type":         profile.get("body_type") or "Athletic",  # None when gender is Male
        "Color_Preference":  profile.get("color_preference",  "Neutral"),
        "Fit_Preference":    profile.get("fit_preference",    "Regular"),
        "Fabric_Preference": profile.get("fabric_preference", "Cotton"),
        "Gender":            profile.get("gender",            "Female"),
        "Age_Group":         profile.get("age_group",         "26-35"),
        "Budget_Range":      profile.get("budget_range",      "Medium"),
    }


def get_rating_verdict(score: float) -> str:
    """Return a human-readable verdict for an outfit match score."""
    if score >= 9:   return "Exceptional ✨"
    if score >= 7.5: return "Great 👏"
    if score >= 6:   return "Good 👍"
    return "Needs Work 🔧"
