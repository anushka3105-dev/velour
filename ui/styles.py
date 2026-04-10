# ─────────────────────────────────────────────
# ui/styles.py — All CSS injected into Streamlit
# ─────────────────────────────────────────────

import streamlit as st

BROWN_BEIGE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

:root {
    --espresso:   #2C1A0E;
    --dark-brown: #4A2C17;
    --mid-brown:  #7B4A2D;
    --warm-brown: #A0622A;
    --caramel:    #C4874A;
    --tan:        #D4A574;
    --sand:       #E8C99A;
    --cream:      #F5E6D0;
    --linen:      #FAF0E6;
    --white-warm: #FFFDF8;
}

* { font-family: 'Jost', sans-serif; }

.stApp {
    background: linear-gradient(160deg, var(--linen) 0%, var(--cream) 50%, var(--sand) 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--espresso) 0%, var(--dark-brown) 60%, var(--mid-brown) 100%) !important;
    border-right: 1px solid var(--caramel);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--tan) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--dark-brown) !important;
    border: 1px solid var(--caramel) !important;
    color: var(--cream) !important;
}

/* ── Typography ── */
.velour-header { text-align:center; padding:2.5rem 0 1.5rem; border-bottom:1px solid var(--tan); margin-bottom:2rem; }
.velour-title  { font-family:'Cormorant Garamond',serif; font-size:4rem; font-weight:300; letter-spacing:0.35em; color:var(--espresso); margin:0; line-height:1; }
.velour-subtitle { font-size:0.72rem; letter-spacing:0.25em; text-transform:uppercase; color:var(--warm-brown); margin-top:0.4rem; }
.section-label { font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--warm-brown); border-bottom:1px solid var(--sand); padding-bottom:0.4rem; margin-bottom:1rem; }
.login-title   { font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--espresso); text-align:center; letter-spacing:0.2em; margin-bottom:0.3rem; }
.login-sub     { text-align:center; font-size:0.72rem; letter-spacing:0.15em; text-transform:uppercase; color:var(--warm-brown); margin-bottom:2rem; }

/* ── Badges ── */
.user-badge    { background:linear-gradient(135deg,var(--caramel),var(--warm-brown)); color:var(--white-warm); padding:0.4rem 1rem; border-radius:20px; font-size:0.75rem; letter-spacing:0.08em; display:inline-block; }
.rating-badge  { display:inline-block; background:linear-gradient(135deg,var(--caramel),var(--warm-brown)); color:var(--white-warm); padding:0.2rem 0.7rem; border-radius:20px; font-size:0.75rem; font-weight:500; letter-spacing:0.05em; }
.trend-chip    { display:inline-block; background:var(--cream); border:1px solid var(--tan); color:var(--dark-brown); padding:0.25rem 0.8rem; border-radius:20px; font-size:0.75rem; margin:0.2rem; letter-spacing:0.04em; }

/* ── Cards ── */
.outfit-card   { background:var(--white-warm); border:1px solid var(--sand); border-left:4px solid var(--caramel); border-radius:2px; padding:1.2rem 1.4rem; margin:0.8rem 0; box-shadow:0 2px 12px rgba(44,26,14,0.07); }
.outfit-card h4 { font-family:'Cormorant Garamond',serif; font-size:1.25rem; color:var(--dark-brown); margin:0 0 0.4rem; font-weight:400; }
.outfit-card p  { color:var(--mid-brown); font-size:0.83rem; margin:0.2rem 0; }
.weather-card  { background:linear-gradient(135deg,var(--dark-brown),var(--mid-brown)); border-radius:4px; padding:1rem 1.2rem; color:var(--cream); margin-bottom:1rem; }
.weather-card .temp { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:300; }
.weather-card .city { font-size:0.75rem; letter-spacing:0.15em; text-transform:uppercase; opacity:0.8; }
.weather-card .desc { font-size:0.82rem; opacity:0.9; margin-top:0.2rem; }

/* ── Chat ── */
.chat-container { background:var(--white-warm); border:1px solid var(--sand); border-radius:2px; padding:1.5rem; height:420px; overflow-y:auto; margin-bottom:1rem; box-shadow:inset 0 2px 8px rgba(44,26,14,0.05); }
.msg-user       { display:flex; justify-content:flex-end; margin:0.6rem 0; }
.msg-user .bubble { background:var(--mid-brown); color:var(--cream); padding:0.65rem 1rem; border-radius:12px 12px 2px 12px; max-width:72%; font-size:0.88rem; line-height:1.5; }
.msg-bot        { display:flex; justify-content:flex-start; margin:0.6rem 0; align-items:flex-start; gap:0.5rem; }
.bot-avatar     { width:28px; height:28px; background:var(--caramel); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.75rem; flex-shrink:0; margin-top:2px; }
.msg-bot .bubble { background:var(--cream); border:1px solid var(--sand); color:var(--espresso); padding:0.65rem 1rem; border-radius:2px 12px 12px 12px; max-width:78%; font-size:0.88rem; line-height:1.6; }

/* ── Wardrobe ── */
.wardrobe-item { background:var(--white-warm); border:1px solid var(--sand); padding:0.8rem 1rem; border-radius:2px; margin:0.4rem 0; display:flex; align-items:center; gap:0.8rem; font-size:0.85rem; color:var(--espresso); }
.wardrobe-icon { width:32px; height:32px; background:var(--sand); border-radius:2px; display:flex; align-items:center; justify-content:center; font-size:1rem; }

/* ── Buttons ── */
.stButton > button { background:var(--mid-brown) !important; color:var(--cream) !important; border:none !important; border-radius:2px !important; font-family:'Jost',sans-serif !important; font-size:0.78rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:0.5rem 1.4rem !important; transition:all 0.2s ease !important; }
.stButton > button:hover { background:var(--dark-brown) !important; transform:translateY(-1px); box-shadow:0 4px 12px rgba(44,26,14,0.2) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input { background:var(--white-warm) !important; border:1px solid var(--sand) !important; border-radius:2px !important; color:var(--espresso) !important; font-family:'Jost',sans-serif !important; }
.stTextInput > div > div > input:focus { border-color:var(--caramel) !important; box-shadow:0 0 0 2px rgba(196,135,74,0.15) !important; }
.stSelectbox > div > div { background:var(--white-warm) !important; border:1px solid var(--sand) !important; border-radius:2px !important; color:var(--espresso) !important; }

/* ── Metrics ── */
[data-testid="metric-container"] { background:var(--white-warm); border:1px solid var(--sand); border-radius:2px; padding:0.8rem; }
[data-testid="metric-container"] label { color:var(--warm-brown) !important; font-size:0.72rem !important; letter-spacing:0.1em; text-transform:uppercase; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:var(--dark-brown) !important; font-family:'Cormorant Garamond',serif !important; font-size:1.8rem !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background:transparent; border-bottom:1px solid var(--sand); gap:0; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--warm-brown) !important; font-size:0.75rem !important; letter-spacing:0.15em !important; text-transform:uppercase !important; border-bottom:2px solid transparent !important; padding:0.6rem 1.4rem !important; }
.stTabs [aria-selected="true"] { color:var(--espresso) !important; border-bottom:2px solid var(--caramel) !important; }

/* ── Misc ── */
hr { border:none; border-top:1px solid var(--sand); margin:1.2rem 0; }
.chat-container::-webkit-scrollbar { width:4px; }
.chat-container::-webkit-scrollbar-track { background:var(--linen); }
.chat-container::-webkit-scrollbar-thumb { background:var(--tan); border-radius:2px; }
</style>
"""


def inject_styles():
    """Call this once at the top of app.py to apply all styles."""
    st.markdown(BROWN_BEIGE_CSS, unsafe_allow_html=True)
