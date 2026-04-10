

import streamlit as st

from ui.styles import inject_styles
from ui.auth_page import render_auth_page
from ui.sidebar import render_sidebar
from ui.tabs.chat import render_chat_tab
from ui.tabs.wardrobe import render_wardrobe_tab
from ui.tabs.trends import render_trends_tab
from ui.tabs.rating import render_rating_tab
from ml.models import load_and_train_models
from utils.helpers import format_user_id


st.set_page_config(
    page_title="VELOUR | Fashion Advisor",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

for key, default in [
    ("logged_in",    False),
    ("current_user", None),
    ("chat_history", []),
    ("user_profile", {}),
    ("auth_mode",    "login"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

models = load_and_train_models()

if not st.session_state.logged_in or st.session_state.current_user is None:
    render_auth_page()
    st.stop()   # ← prevents rest of script running before login

user = st.session_state.current_user

# Sidebar
render_sidebar(user)

# Header
st.markdown(f"""
<div class="velour-header">
    <div class="velour-title">VELOUR</div>
    <div class="velour-subtitle">Your Personal Fashion Intelligence Advisor</div>
    <div style='margin-top:0.8rem;'>
        <span class='user-badge'>👤 {user['username']} &nbsp;·&nbsp; ID: {format_user_id(user['id'])}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Weather banner — shown only after weather is fetched
if "weather_data" in st.session_state:
    wd = st.session_state["weather_data"]
    st.markdown(f"""
    <div class="weather-card">
        <div class="city">📍 {wd['city']}</div>
        <div class="temp">{wd['temp']}°C</div>
        <div class="desc">{wd['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab_chat, tab_wardrobe, tab_trends, tab_rating = st.tabs([
    "💬  Chat Advisor",
    "👗  Wardrobe",
    "✨  Trends",
    "⭐  Outfit Rating",
])

with tab_chat:
    render_chat_tab(user, models)

with tab_wardrobe:
    render_wardrobe_tab(user)

with tab_trends:
    render_trends_tab(user, models)

with tab_rating:
    render_rating_tab(models)
