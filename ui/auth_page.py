# ─────────────────────────────────────────────
# ui/auth_page.py — Login & Sign Up screens
# ─────────────────────────────────────────────

import streamlit as st
from auth.supabase_auth import sign_in, sign_up, validate_signup_form
from database.db import load_profile


def render_auth_page():
    """
    Renders the login/signup screen.
    Sets st.session_state.logged_in and current_user on success.
    """
    st.markdown("""
    <div class="velour-header">
        <div class="velour-title">VELOUR</div>
        <div class="velour-subtitle">Personal Fashion Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        # Toggle between Login / Sign Up
        mode = st.radio(
            "", ["Login", "Sign Up"], horizontal=True,
            index=0 if st.session_state.get("auth_mode", "login") == "login" else 1,
            label_visibility="collapsed",
        )
        st.session_state.auth_mode = "login" if mode == "Login" else "signup"
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            _render_login()
        else:
            _render_signup()


def _render_login():
    st.markdown(
        '<div class="login-title">Welcome Back</div>'
        '<div class="login-sub">Sign in to your wardrobe</div>',
        unsafe_allow_html=True,
    )
    username = st.text_input("Username", placeholder="Enter your username", key="li_user")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass")

    if st.button("Sign In →", use_container_width=True):
        if not (username and password):
            st.warning("Please fill in all fields.")
            return

        result = sign_in(username.strip(), password)
        if result["success"]:
            _set_logged_in(result["user"])
        else:
            st.error(result["error"])


def _render_signup():
    st.markdown(
        '<div class="login-title">Create Account</div>'
        '<div class="login-sub">Join VELOUR today</div>',
        unsafe_allow_html=True,
    )
    new_user = st.text_input("Choose a Username", placeholder="e.g. anushka_styles", key="su_user")
    new_pass = st.text_input("Choose a Password", type="password", placeholder="Min 6 characters", key="su_pass")
    confirm  = st.text_input("Confirm Password",  type="password", placeholder="Repeat password",   key="su_conf")

    if st.button("Create Account →", use_container_width=True):
        error = validate_signup_form(new_user, new_pass, confirm)
        if error:
            st.error(error)
            return

        result = sign_up(new_user.strip(), new_pass)
        if result["success"]:
            _set_logged_in(result["user"])
        else:
            st.error(result["error"])


def _set_logged_in(user: dict):
    """Shared helper — set session state after successful login or signup."""
    st.session_state.logged_in    = True
    st.session_state.current_user = user

    # Restore previously saved profile preferences
    saved = load_profile(user["id"])
    st.session_state.user_profile = saved if saved else {}

    st.rerun()
