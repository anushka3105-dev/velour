

import streamlit as st
from config import TRENDS_BY_SEASON
from ml.predictor import get_outfit_suggestion, compute_outfit_rating
from utils.helpers import get_current_season, profile_to_ml_format


def render_trends_tab(user: dict, models: dict):
    """Render the trends discovery tab."""
    st.markdown('<div class="section-label">Fashion Trends</div>', unsafe_allow_html=True)

    _render_season_cards()
    _render_personalised_match(user, models)


def _render_season_cards():
    season = get_current_season()
    # Current season first, then the rest
    ordered = [season] + [s for s in ["Spring", "Summer", "Autumn", "Winter"] if s != season]
    cols    = st.columns(2)

    for i, s in enumerate(ordered):
        with cols[i % 2]:
            is_current = (s == season)
            border     = "border-left: 4px solid #C4874A;" if is_current else "border-left: 4px solid #D4A574;"
            badge      = (
                '<span style="background:#C4874A; color:#FFFDF8; padding:0.15rem 0.5rem; '
                'border-radius:10px; font-size:0.65rem; margin-left:0.5rem;">CURRENT</span>'
                if is_current else ""
            )
            chips = " ".join(
                f'<span class="trend-chip">{t}</span>'
                for t in TRENDS_BY_SEASON[s]
            )
            st.markdown(f"""
            <div class="outfit-card" style="{border}">
                <h4>{s} 2024 {badge}</h4>
                <div style="margin-top:0.6rem;">{chips}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_personalised_match(user: dict, models: dict):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Personalised Trend Match</div>', unsafe_allow_html=True)

    ml_profile = profile_to_ml_format(st.session_state.get("user_profile", {}))
    outfit, desc = get_outfit_suggestion(
        ml_profile["Weather"],
        ml_profile["Occasion"],
        ml_profile["Style_Preference"],
    )
    score = compute_outfit_rating(ml_profile, models)

    st.markdown(f"""
    <div class="outfit-card">
        <h4>Curated for {user['username']} — {ml_profile['Style_Preference']} × {ml_profile['Occasion']}</h4>
        <p>🎨 <strong>{outfit}</strong></p>
        <p style="margin-top:0.4rem;">{desc}</p>
        <div style="margin-top:0.6rem;">
            <span class="rating-badge">Trend Match: {score}/10</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
