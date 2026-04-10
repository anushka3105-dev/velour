# ─────────────────────────────────────────────
# ui/sidebar.py — Sidebar: profile, weather, logout
# ─────────────────────────────────────────────

import streamlit as st
from database.db import save_profile
from utils.weather import fetch_weather
from utils.helpers import get_option_index, format_user_id, weather_icon_to_category
from config import OPTIONS


def render_sidebar(user: dict):
    """
    Renders the full sidebar for a logged-in user.
    Updates st.session_state.user_profile on every interaction.
    """
    with st.sidebar:
        _render_logo(user)
        _render_profile_form(user)
        _render_weather_section()
        _render_logout_button()


# ── Private helpers ───────────────────────────

def _render_logo(user: dict):
    st.markdown(f"""
    <div style='text-align:center; padding:1.2rem 0 0.8rem;'>
        <div style='font-family:"Cormorant Garamond",serif; font-size:1.9rem; letter-spacing:0.3em; color:#E8C99A;'>VELOUR</div>
        <div style='font-size:0.62rem; letter-spacing:0.22em; color:#C4874A; text-transform:uppercase; margin-top:2px;'>Fashion Intelligence</div>
    </div>
    <hr style='border-color:#4A2C17; margin:0.5rem 0 1rem;'>
    <div style='text-align:center; margin-bottom:1rem;'>
        <span class='user-badge'>👤 {user['username']}</span>
        <div style='font-size:0.65rem; color:#D4A574; margin-top:0.5rem; letter-spacing:0.06em;'>
            ID: {format_user_id(user['id'])}
        </div>
    </div>
    <hr style='border-color:#4A2C17; margin:0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)


def _render_profile_form(user: dict):
    st.markdown('<div class="section-label">Your Profile</div>', unsafe_allow_html=True)

    saved = st.session_state.get("user_profile", {})

    # ── Gender — rendered first because it controls body type visibility ──
    gender = st.selectbox(
        "Gender",
        OPTIONS["gender"],
        index=get_option_index("gender", saved.get("gender")),
    )

    # ── Body Type — hidden for Male, shown for Female / Non-binary ────────
    # When gender is Male, body_type is set to None and the widget is skipped.
    # Streamlit reruns the script on every widget change, so switching gender
    # immediately adds or removes the body type selectbox.
    if gender == "Male":
        body_type = None   # not applicable — excluded from profile
    else:
        body_type = st.selectbox(
            "Body Type",
            OPTIONS["body_type"],
            index=get_option_index("body_type", saved.get("body_type")),
        )

    age_group  = st.selectbox("Age Group",         OPTIONS["age_group"],        index=get_option_index("age_group",        saved.get("age_group")))
    weather    = st.selectbox("Current Weather",   OPTIONS["weather"],          index=get_option_index("weather",          saved.get("weather")))
    occasion   = st.selectbox("Occasion",          OPTIONS["occasion"],         index=get_option_index("occasion",         saved.get("occasion")))
    style_pref = st.selectbox("Style Preference",  OPTIONS["style_preference"], index=get_option_index("style_preference", saved.get("style_preference")))
    color_pref = st.selectbox("Colour Preference", OPTIONS["color_preference"], index=get_option_index("color_preference", saved.get("color_preference")))
    budget     = st.selectbox("Budget Range",      OPTIONS["budget_range"],     index=get_option_index("budget_range",     saved.get("budget_range")))
    fabric     = st.selectbox("Fabric Preference", OPTIONS["fabric_preference"],index=get_option_index("fabric_preference",saved.get("fabric_preference")))
    fit        = st.selectbox("Fit Preference",    OPTIONS["fit_preference"],   index=get_option_index("fit_preference",   saved.get("fit_preference")))

    # Always keep session state in sync with current selections
    st.session_state.user_profile = {
        "gender": gender, "age_group": age_group, "body_type": body_type,
        "weather": weather, "occasion": occasion, "style_preference": style_pref,
        "color_preference": color_pref, "budget_range": budget,
        "fabric_preference": fabric, "fit_preference": fit,
    }

    if st.button("💾  Save Profile"):
        ok = save_profile(user["id"], st.session_state.user_profile)
        if ok:
            st.success("Profile saved!")
        else:
            st.error("Could not save. Check Supabase connection.")


def _render_weather_section():
    st.markdown('<hr style="border-color:#4A2C17; margin:1rem 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Weather API</div>', unsafe_allow_html=True)

    city    = st.text_input("City", placeholder="e.g. Mumbai")
    api_key = st.text_input("OpenWeatherMap Key", type="password", placeholder="Paste your key")

    if st.button("🌤  Get Weather"):
        if city and api_key:
            result = fetch_weather(city, api_key)
            if result and "error" not in result:
                st.session_state["weather_data"] = result
                # Auto-update weather in profile
                st.session_state.user_profile["weather"] = weather_icon_to_category(result["icon"])
                st.rerun()
            elif result and "error" in result:
                st.error(result["error"])
            else:
                st.error("Could not fetch weather.")
        else:
            st.warning("Enter city and API key.")


def _render_logout_button():
    st.markdown('<hr style="border-color:#4A2C17; margin:1rem 0;">', unsafe_allow_html=True)
    if st.button("🚪  Log Out"):
        for key in ["logged_in", "current_user", "chat_history", "user_profile", "weather_data"]:
            st.session_state.pop(key, None)
        st.session_state.logged_in = False
        st.rerun()
