# ─────────────────────────────────────────────
# ui/tabs/chat.py — Chat Advisor tab
# ─────────────────────────────────────────────

import streamlit as st
from ml.predictor import classify_intent, build_bot_reply
from utils.helpers import profile_to_ml_format


QUICK_PROMPTS = [
    "Suggest an outfit for today",
    "What are trending styles?",
    "Rate my current outfit",
    "Give me a style tip",
    "What to wear in this weather?",
]


def render_chat_tab(user: dict, models: dict):
    """Render the full chat tab."""
    col_chat, col_actions = st.columns([2, 1])

    with col_chat:
        _render_chat_history(user)
        _render_chat_input(user, models)

    with col_actions:
        _render_quick_actions(user, models)


# ── Private helpers ───────────────────────────

def _render_chat_history(user: dict):
    st.markdown('<div class="section-label">Chat with VELOUR</div>', unsafe_allow_html=True)

    html = '<div class="chat-container">'

    if not st.session_state.chat_history:
        html += (
            f'<div class="msg-bot"><div class="bot-avatar">V</div>'
            f'<div class="bubble">Welcome back, <strong>{user["username"]}</strong>! '
            f"Ask me to suggest an outfit, discover trends, rate your look, or manage your wardrobe 👗"
            f'</div></div>'
        )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            html += f'<div class="msg-user"><div class="bubble">{msg["text"]}</div></div>'
        else:
            html += f'<div class="msg-bot"><div class="bot-avatar">V</div><div class="bubble">{msg["text"]}</div></div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_chat_input(user: dict, models: dict):
    c1, c2 = st.columns([5, 1])
    with c1:
        user_input = st.text_input(
            "", placeholder="Ask me anything about fashion...",
            label_visibility="collapsed", key="chat_input",
        )
    with c2:
        send = st.button("Send →")

    if send and user_input.strip():
        _process_message(user_input.strip(), user, models)


def _render_quick_actions(user: dict, models: dict):
    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)

    for prompt in QUICK_PROMPTS:
        if st.button(prompt, key=f"qp_{prompt}"):
            _process_message(prompt, user, models)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑  Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


def _process_message(text: str, user: dict, models: dict):
    """Classify intent, build reply, append both to history, rerun."""
    intent     = classify_intent(text, models)   # ← NLP pipeline now used here
    ml_profile = profile_to_ml_format(st.session_state.get("user_profile", {}))
    reply      = build_bot_reply(intent, ml_profile, models, username=user["username"])

    st.session_state.chat_history.append({"role": "user", "text": text})
    st.session_state.chat_history.append({"role": "bot",  "text": reply})
    st.rerun()
