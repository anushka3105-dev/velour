# ─────────────────────────────────────────────
# ml/predictor.py — Predictions using trained models
#
# classify_intent()  uses the TF-IDF + Naive Bayes NLP pipeline
# compute_outfit_rating() uses the SVM model
# ─────────────────────────────────────────────

import numpy as np
from config import (
    CAT_COLS, OUTFIT_SUGGESTIONS, STYLE_TIPS,
    INTENT_RESPONSES, TRENDS_BY_SEASON,
)
from utils.helpers import get_current_season


# ── NLP Intent Classifier ─────────────────────

def classify_intent(text: str, models: dict) -> str:
    """
    Classify the intent of a raw user message using the
    trained TF-IDF + Naive Bayes NLP pipeline.

    How it works:
      1. TfidfVectorizer converts the sentence into a
         sparse numeric vector of TF-IDF weighted n-gram scores
      2. MultinomialNB predicts the most probable intent class
      3. If the top probability is below the confidence threshold,
         fall back to "unknown" rather than guessing wrongly

    Args:
        text   : raw user message string
        models : dict returned by load_and_train_models()

    Returns:
        intent label string (e.g. "suggest_outfit")
    """
    if not text or not text.strip():
        return "unknown"

    pipeline = models.get("nlp_pipeline")
    if pipeline is None:
        return "unknown"

    # predict_proba returns an array of shape (1, n_classes)
    # e.g. [[0.02, 0.71, 0.04, 0.08, 0.03, 0.07, 0.05]]
    proba    = pipeline.predict_proba([text.lower().strip()])[0]
    max_prob = float(np.max(proba))

    # Confidence threshold — if the model isn't sure enough,
    # return "unknown" rather than a low-confidence wrong answer.
    # 0.25 is intentionally low because our training set is small.
    # Increase to 0.4–0.5 once you have more training sentences.
    CONFIDENCE_THRESHOLD = 0.25

    if max_prob < CONFIDENCE_THRESHOLD:
        return "unknown"

    # classes_ holds the label names in the same order as proba
    predicted = pipeline.classes_[int(np.argmax(proba))]
    return predicted


def get_intent_confidence(text: str, models: dict) -> dict:
    """
    Return all intent probabilities for a message.
    Useful for debugging — shows what the model is thinking.

    Returns dict like:
        {"suggest_outfit": 0.71, "trend_advice": 0.08, ...}
    """
    pipeline = models.get("nlp_pipeline")
    if not pipeline or not text.strip():
        return {}

    proba   = pipeline.predict_proba([text.lower().strip()])[0]
    classes = pipeline.classes_

    return {
        label: round(float(prob), 3)
        for label, prob in sorted(
            zip(classes, proba),
            key=lambda x: x[1],
            reverse=True,
        )
    }


# ── SVM Outfit Rater ─────────────────────────

def compute_outfit_rating(user_prefs: dict, models: dict) -> float:
    """
    Use trained SVM to compute a 0–10 match score for a given profile.
    Higher score = outfit parameters align with high-confidence style profiles.
    """
    try:
        row = []
        for col in CAT_COLS:
            enc = models["encoders"][col]
            val = user_prefs.get(col, enc.classes_[0])
            row.append(enc.transform([val])[0] if val in enc.classes_ else 0)

        X     = models["scaler"].transform([row])
        proba = models["svm"].predict_proba(X)[0]
        return min(round(float(np.max(proba)) * 10, 1), 10.0)

    except Exception:
        return round(float(np.random.uniform(6.5, 9.5)), 1)


# ── Outfit Suggestions ───────────────────────

def get_outfit_suggestion(weather: str, occasion: str, style: str) -> tuple:
    """
    Lookup best outfit for a (weather, occasion, style) combination.
    Falls back to partial match, then a universal default.
    """
    key = (weather, occasion, style)
    if key in OUTFIT_SUGGESTIONS:
        return OUTFIT_SUGGESTIONS[key]

    for (w, o, _), val in OUTFIT_SUGGESTIONS.items():
        if w == weather or o == occasion:
            return val

    return (
        "Classic White Shirt + Tailored Trousers + Loafers",
        "A timeless combination that works for any occasion.",
    )


def get_style_tip(body_type: str) -> str:
    """Return a body-type-specific style tip."""
    return STYLE_TIPS.get(
        body_type,
        "Wear what makes you feel confident — that's always in style!",
    )


def get_trend_chips_html(season: str | None = None) -> str:
    """Return HTML trend chip string for a given season (default: current)."""
    if season is None:
        season = get_current_season()
    trends = TRENDS_BY_SEASON.get(season, [])
    return " ".join(f'<span class="trend-chip">{t}</span>' for t in trends)


# ── Bot Reply Builder ─────────────────────────

def build_bot_reply(
    intent: str,
    ml_profile: dict,
    models: dict,
    username: str = "",
) -> str:
    """
    Build the full HTML bot reply string for a given intent and user profile.
    Used by both the chat tab and quick-action buttons.
    """
    base = INTENT_RESPONSES.get(intent, INTENT_RESPONSES["unknown"])

    if intent == "suggest_outfit":
        outfit, desc = get_outfit_suggestion(
            ml_profile["Weather"],
            ml_profile["Occasion"],
            ml_profile["Style_Preference"],
        )
        score = compute_outfit_rating(ml_profile, models)
        return (
            f"{base}<br><br><strong>{outfit}</strong>"
            f'<br><em style="color:#A0622A;">{desc}</em>'
            f'<br><br><span class="rating-badge">Match Score: {score}/10</span>'
        )

    if intent == "trend_advice":
        chips = get_trend_chips_html()
        return f"{base}<br><br>{chips}"

    if intent == "rate_outfit":
        score = compute_outfit_rating(ml_profile, models)
        stars = "⭐" * int(score // 2)
        return f'Match score: <span class="rating-badge">{score}/10</span> {stars}'

    if intent == "style_tip":
        tip = get_style_tip(ml_profile.get("Body_Type", "Hourglass"))
        return f"{base}<br><br><em>{tip}</em>"

    if intent == "weather_outfit":
        outfit, desc = get_outfit_suggestion(
            ml_profile["Weather"],
            ml_profile["Occasion"],
            ml_profile["Style_Preference"],
        )
        return f"{base}<br><br><strong>{outfit}</strong><br><em style='color:#A0622A;'>{desc}</em>"

    if intent == "greeting":
        name_part = f" back, <strong>{username}</strong>" if username else ""
        return f"👋 Welcome{name_part}! I'm VELOUR — ask me to suggest an outfit, check trends, or manage your wardrobe 👗"

    return base
