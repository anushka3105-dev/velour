import streamlit as st
import pandas as pd
import numpy as np
import os
import hashlib
import requests
from datetime import datetime
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# SUPABASE CONFIG  ← PASTE YOUR KEYS HERE
# ─────────────────────────────────────────────
SUPABASE_URL = "https://your-project-id.supabase.co"   # ← your project URL
SUPABASE_KEY = "your-anon-public-key-here"              # ← your anon/public key
# ─────────────────────────────────────────────

from supabase import create_client, Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VELOUR | Fashion Advisor",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# BROWN & BEIGE THEME CSS
# ─────────────────────────────────────────────
st.markdown("""
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
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--espresso) 0%, var(--dark-brown) 60%, var(--mid-brown) 100%) !important;
    border-right: 1px solid var(--caramel);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color: var(--tan) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: var(--dark-brown) !important; border: 1px solid var(--caramel) !important; color: var(--cream) !important; }
.velour-header { text-align:center; padding:2.5rem 0 1.5rem; border-bottom:1px solid var(--tan); margin-bottom:2rem; }
.velour-title { font-family:'Cormorant Garamond',serif; font-size:4rem; font-weight:300; letter-spacing:0.35em; color:var(--espresso); margin:0; line-height:1; }
.velour-subtitle { font-size:0.72rem; letter-spacing:0.25em; text-transform:uppercase; color:var(--warm-brown); margin-top:0.4rem; }
.section-label { font-size:0.68rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--warm-brown); border-bottom:1px solid var(--sand); padding-bottom:0.4rem; margin-bottom:1rem; }
.chat-container { background:var(--white-warm); border:1px solid var(--sand); border-radius:2px; padding:1.5rem; height:420px; overflow-y:auto; margin-bottom:1rem; box-shadow:inset 0 2px 8px rgba(44,26,14,0.05); }
.msg-user { display:flex; justify-content:flex-end; margin:0.6rem 0; }
.msg-user .bubble { background:var(--mid-brown); color:var(--cream); padding:0.65rem 1rem; border-radius:12px 12px 2px 12px; max-width:72%; font-size:0.88rem; line-height:1.5; }
.msg-bot { display:flex; justify-content:flex-start; margin:0.6rem 0; align-items:flex-start; gap:0.5rem; }
.bot-avatar { width:28px; height:28px; background:var(--caramel); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.75rem; flex-shrink:0; margin-top:2px; }
.msg-bot .bubble { background:var(--cream); border:1px solid var(--sand); color:var(--espresso); padding:0.65rem 1rem; border-radius:2px 12px 12px 12px; max-width:78%; font-size:0.88rem; line-height:1.6; }
.outfit-card { background:var(--white-warm); border:1px solid var(--sand); border-left:4px solid var(--caramel); border-radius:2px; padding:1.2rem 1.4rem; margin:0.8rem 0; box-shadow:0 2px 12px rgba(44,26,14,0.07); }
.outfit-card h4 { font-family:'Cormorant Garamond',serif; font-size:1.25rem; color:var(--dark-brown); margin:0 0 0.4rem; font-weight:400; }
.outfit-card p { color:var(--mid-brown); font-size:0.83rem; margin:0.2rem 0; }
.rating-badge { display:inline-block; background:linear-gradient(135deg,var(--caramel),var(--warm-brown)); color:var(--white-warm); padding:0.2rem 0.7rem; border-radius:20px; font-size:0.75rem; font-weight:500; letter-spacing:0.05em; }
.trend-chip { display:inline-block; background:var(--cream); border:1px solid var(--tan); color:var(--dark-brown); padding:0.25rem 0.8rem; border-radius:20px; font-size:0.75rem; margin:0.2rem; letter-spacing:0.04em; }
.wardrobe-item { background:var(--white-warm); border:1px solid var(--sand); padding:0.8rem 1rem; border-radius:2px; margin:0.4rem 0; display:flex; align-items:center; gap:0.8rem; font-size:0.85rem; color:var(--espresso); }
.wardrobe-icon { width:32px; height:32px; background:var(--sand); border-radius:2px; display:flex; align-items:center; justify-content:center; font-size:1rem; }
.stButton > button { background:var(--mid-brown) !important; color:var(--cream) !important; border:none !important; border-radius:2px !important; font-family:'Jost',sans-serif !important; font-size:0.78rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:0.5rem 1.4rem !important; transition:all 0.2s ease !important; }
.stButton > button:hover { background:var(--dark-brown) !important; transform:translateY(-1px); box-shadow:0 4px 12px rgba(44,26,14,0.2) !important; }
.stTextInput > div > div > input { background:var(--white-warm) !important; border:1px solid var(--sand) !important; border-radius:2px !important; color:var(--espresso) !important; font-family:'Jost',sans-serif !important; }
.stTextInput > div > div > input:focus { border-color:var(--caramel) !important; box-shadow:0 0 0 2px rgba(196,135,74,0.15) !important; }
.stSelectbox > div > div { background:var(--white-warm) !important; border:1px solid var(--sand) !important; border-radius:2px !important; color:var(--espresso) !important; }
[data-testid="metric-container"] { background:var(--white-warm); border:1px solid var(--sand); border-radius:2px; padding:0.8rem; }
[data-testid="metric-container"] label { color:var(--warm-brown) !important; font-size:0.72rem !important; letter-spacing:0.1em; text-transform:uppercase; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color:var(--dark-brown) !important; font-family:'Cormorant Garamond',serif !important; font-size:1.8rem !important; }
.stTabs [data-baseweb="tab-list"] { background:transparent; border-bottom:1px solid var(--sand); gap:0; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--warm-brown) !important; font-size:0.75rem !important; letter-spacing:0.15em !important; text-transform:uppercase !important; border-bottom:2px solid transparent !important; padding:0.6rem 1.4rem !important; }
.stTabs [aria-selected="true"] { color:var(--espresso) !important; border-bottom:2px solid var(--caramel) !important; }
.weather-card { background:linear-gradient(135deg,var(--dark-brown),var(--mid-brown)); border-radius:4px; padding:1rem 1.2rem; color:var(--cream); margin-bottom:1rem; }
.weather-card .temp { font-family:'Cormorant Garamond',serif; font-size:2.2rem; font-weight:300; }
.weather-card .city { font-size:0.75rem; letter-spacing:0.15em; text-transform:uppercase; opacity:0.8; }
.weather-card .desc { font-size:0.82rem; opacity:0.9; margin-top:0.2rem; }
.login-title { font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--espresso); text-align:center; letter-spacing:0.2em; margin-bottom:0.3rem; }
.login-sub { text-align:center; font-size:0.72rem; letter-spacing:0.15em; text-transform:uppercase; color:var(--warm-brown); margin-bottom:2rem; }
.user-badge { background:linear-gradient(135deg,var(--caramel),var(--warm-brown)); color:var(--white-warm); padding:0.4rem 1rem; border-radius:20px; font-size:0.75rem; letter-spacing:0.08em; display:inline-block; }
hr { border:none; border-top:1px solid var(--sand); margin:1.2rem 0; }
.chat-container::-webkit-scrollbar { width:4px; }
.chat-container::-webkit-scrollbar-track { background:var(--linen); }
.chat-container::-webkit-scrollbar-thumb { background:var(--tan); border-radius:2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(username: str, password: str) -> dict:
    try:
        existing = supabase.table("users").select("id").eq("username", username).execute()
        if existing.data:
            return {"success": False, "error": "Username already exists."}
        result = supabase.table("users").insert({
            "username": username,
            "password_hash": hash_password(password),
            "created_at": datetime.utcnow().isoformat(),
            "last_login":  datetime.utcnow().isoformat(),
        }).execute()
        user = result.data[0]
        supabase.table("user_profiles").insert({"user_id": user["id"]}).execute()
        return {"success": True, "user": user}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_in(username: str, password: str) -> dict:
    try:
        result = supabase.table("users").select("*") \
            .eq("username", username) \
            .eq("password_hash", hash_password(password)).execute()
        if not result.data:
            return {"success": False, "error": "Invalid username or password."}
        user = result.data[0]
        supabase.table("users").update({"last_login": datetime.utcnow().isoformat()}).eq("id", user["id"]).execute()
        return {"success": True, "user": user}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─────────────────────────────────────────────
# SUPABASE DATA HELPERS
# ─────────────────────────────────────────────
def load_profile(user_id: str) -> dict:
    try:
        r = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
        return r.data[0] if r.data else {}
    except:
        return {}

def save_profile(user_id: str, profile: dict):
    try:
        existing = supabase.table("user_profiles").select("id").eq("user_id", user_id).execute()
        payload  = {**profile, "user_id": user_id, "updated_at": datetime.utcnow().isoformat()}
        if existing.data:
            supabase.table("user_profiles").update(payload).eq("user_id", user_id).execute()
        else:
            supabase.table("user_profiles").insert(payload).execute()
    except:
        pass

def load_wardrobe(user_id: str) -> list:
    try:
        r = supabase.table("wardrobe").select("*").eq("user_id", user_id).order("added_at", desc=True).execute()
        return r.data or []
    except:
        return []

def add_wardrobe_item(user_id: str, item: dict) -> bool:
    try:
        supabase.table("wardrobe").insert({**item, "user_id": user_id, "added_at": datetime.utcnow().isoformat()}).execute()
        return True
    except:
        return False

def delete_wardrobe_item(item_id: str) -> bool:
    try:
        supabase.table("wardrobe").delete().eq("id", item_id).execute()
        return True
    except:
        return False


# ─────────────────────────────────────────────
# ML SETUP
# ─────────────────────────────────────────────
DATASET_PATH = "fashion_dataset.csv"

OUTFIT_SUGGESTIONS = {
    ("Sunny",  "Casual",  "Minimalist"):  ("Linen Wide-Leg Trousers + Fitted White Tee",  "Clean lines, breathable fabric — effortlessly chic."),
    ("Sunny",  "Casual",  "Bohemian"):    ("Flowy Maxi Skirt + Cropped Crochet Top",       "Free-spirited layers perfect for a sunny day."),
    ("Sunny",  "Formal",  "Classic"):     ("Tailored Cream Blazer + Straight Trousers",    "A timeless power look for sun-drenched meetings."),
    ("Rainy",  "Casual",  "Streetwear"):  ("Oversized Trench Coat + Chunky Sneakers",      "Rain-ready street style with attitude."),
    ("Rainy",  "Formal",  "Elegant"):     ("Wrap Dress + Block Heel Ankle Boot",           "Polished and weather-smart."),
    ("Cold",   "Work",    "Business"):    ("Turtleneck Knit + Tailored Wool Trousers",     "Sharp and cosy — boardroom approved."),
    ("Cold",   "Casual",  "Classic"):     ("Camel Overcoat + Dark Denim + Chelsea Boot",   "Autumnal classics done right."),
    ("Cloudy", "Party",   "Trendy"):      ("Satin Slip Dress + Leather Jacket + Mules",    "Effortless party-ready contrast."),
    ("Cloudy", "Date",    "Romantic"):    ("Floral Midi Dress + Kitten Heels",             "Soft, feminine, and utterly charming."),
    ("Sunny",  "Party",   "Trendy"):      ("Cut-Out Bodysuit + High-Waist Trousers",       "Statement-making for sunny socials."),
}

TRENDS_BY_SEASON = {
    "Winter": ["Quiet Luxury","Chocolate Brown Tones","Shearling Everything","Ballet Flats Revival","Knit Sets"],
    "Summer": ["Coastal Grandmother","Linen Suiting","Crochet & Macramé","Micro Bags","Dopamine Dressing"],
    "Spring": ["Butter Yellow","Floral Maximalism","Sheer Layers","Mary Janes","Denim-on-Denim"],
    "Autumn": ["Burgundy & Rust","Leather Trench Coats","Chunky Loafers","Plaid Everything","Velvet Accents"],
}

STYLE_TIPS = {
    "Apple":             "Highlight your waist with wrap silhouettes and A-line skirts. V-necks elongate your frame beautifully.",
    "Pear":              "Balance proportions with structured tops, wide-leg trousers, and statement shoulders.",
    "Hourglass":         "Celebrate your curves with fit-and-flare styles, belted waists, and bodycon silhouettes.",
    "Rectangle":         "Create curves with ruffles, peplum tops, and layered textures to add dimension.",
    "Athletic":          "Embrace your frame with fitted basics, tapered trousers, and structured jackets.",
    "Inverted Triangle": "Balance broad shoulders with wide-leg pants, flared skirts, and V-neck details.",
}

INTENT_RESPONSES = {
    "suggest_outfit": "✨ Based on your profile, here's a curated outfit for you:",
    "rate_outfit":    "📊 Let me analyse your outfit match score...",
    "add_item":       "➕ Head to the Wardrobe tab to add new items!",
    "trend_advice":   "🌟 Here are the hottest trends right now:",
    "style_tip":      "💡 Here's a personalised style tip for you:",
    "weather_outfit": "🌤️ Dressing for today's weather, here's what I suggest:",
    "greeting":       "👋 Hello! I'm VELOUR, your personal fashion advisor. Ask me to suggest an outfit, check trends, or manage your wardrobe!",
    "unknown":        "I'd love to help! Try: 'suggest an outfit', 'show trends', 'rate my outfit', or 'style tip'.",
}

@st.cache_resource
def load_and_train_models():
    try:
        df = pd.read_csv(DATASET_PATH).dropna()
    except Exception:
        df = pd.DataFrame({
            "Color_Preference": ["Neutral","Bold","Pastel","Dark","Warm"]*5,
            "Body_Type":        ["Hourglass","Athletic","Pear","Rectangle","Apple"]*5,
            "Gender":           ["Female","Male","Female","Male","Female"]*5,
            "Age_Group":        ["18-25","26-35","18-25","36-45","26-35"]*5,
            "Weather":          ["Sunny","Rainy","Cloudy","Cold","Sunny"]*5,
            "Occasion":         ["Casual","Formal","Party","Work","Date"]*5,
            "Style_Preference": ["Minimalist","Classic","Trendy","Business","Romantic"]*5,
            "Budget_Range":     ["Medium","High","Low","High","Medium"]*5,
            "Fabric_Preference":["Cotton","Wool","Polyester","Linen","Silk"]*5,
            "Fit_Preference":   ["Slim","Regular","Loose","Regular","Slim"]*5,
            "Intent":           ["suggest_outfit"]*25,
        })
    cat_cols = ["Color_Preference","Body_Type","Gender","Age_Group","Weather",
                "Occasion","Style_Preference","Budget_Range","Fabric_Preference","Fit_Preference"]
    encoders = {col: LabelEncoder() for col in cat_cols}
    X = df[cat_cols].copy()
    for col in cat_cols:
        X[col] = encoders[col].fit_transform(X[col].astype(str))
    intent_enc = LabelEncoder()
    y_enc      = intent_enc.fit_transform(df["Intent"].astype(str))
    scaler     = MinMaxScaler()
    X_scaled   = scaler.fit_transform(X)
    nb_model   = MultinomialNB()
    nb_model.fit((X_scaled * 10).astype(int), y_enc)
    style_enc  = LabelEncoder()
    y_style    = style_enc.fit_transform(df["Style_Preference"].astype(str))
    svm_model  = SVC(kernel="rbf", probability=True, C=1.0, gamma="scale")
    svm_model.fit(X_scaled, y_style)
    return {"nb": nb_model, "svm": svm_model, "encoders": encoders,
            "intent_enc": intent_enc, "style_enc": style_enc,
            "scaler": scaler, "cat_cols": cat_cols}

def classify_intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["suggest","recommend","what should","outfit for","wear"]):    return "suggest_outfit"
    if any(w in t for w in ["trend","trending","fashion week","hot right now","popular"]): return "trend_advice"
    if any(w in t for w in ["rate","score","how good","match","rating"]):                 return "rate_outfit"
    if any(w in t for w in ["add","insert","save","put","new item","bought"]):            return "add_item"
    if any(w in t for w in ["tip","advice","body type","style for","how to dress"]):      return "style_tip"
    if any(w in t for w in ["weather","rain","cold","sunny","temperature"]):              return "weather_outfit"
    if any(w in t for w in ["hi","hello","hey","good morning","sup"]):                    return "greeting"
    return "unknown"

def compute_outfit_rating(user_prefs: dict, models: dict) -> float:
    try:
        row = []
        for col in models["cat_cols"]:
            enc = models["encoders"][col]
            val = user_prefs.get(col, enc.classes_[0])
            row.append(enc.transform([val])[0] if val in enc.classes_ else 0)
        X = models["scaler"].transform([row])
        return min(round(float(np.max(models["svm"].predict_proba(X)[0])) * 10, 1), 10.0)
    except:
        return round(np.random.uniform(6.5, 9.5), 1)

def get_outfit_suggestion(weather, occasion, style) -> tuple:
    key = (weather, occasion, style)
    if key in OUTFIT_SUGGESTIONS: return OUTFIT_SUGGESTIONS[key]
    for (w, o, s), val in OUTFIT_SUGGESTIONS.items():
        if w == weather or o == occasion: return val
    return ("Classic White Shirt + Tailored Trousers + Loafers", "A timeless combination that works for any occasion.")

def get_weather(city: str, api_key: str) -> dict | None:
    # ── PASTE YOUR OPENWEATHERMAP KEY HERE (or use sidebar input) ──
    # api_key = "your_openweathermap_key_here"
    # ───────────────────────────────────────────────────────────────
    if not api_key or api_key == "YOUR_API_KEY_HERE": return None
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric", timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {"city": d["name"], "temp": round(d["main"]["temp"]),
                    "desc": d["weather"][0]["description"].title(), "icon": d["weather"][0]["main"]}
    except: pass
    return None

def weather_to_category(icon: str) -> str:
    return {"Clear":"Sunny","Clouds":"Cloudy","Rain":"Rainy","Drizzle":"Rainy","Snow":"Cold","Thunderstorm":"Rainy"}.get(icon,"Cloudy")

def get_current_season() -> str:
    m = datetime.now().month
    if m in [12,1,2]: return "Winter"
    if m in [3,4,5]:  return "Spring"
    if m in [6,7,8]:  return "Summer"
    return "Autumn"


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in [("logged_in",False),("current_user",None),("chat_history",[]),("user_profile",{}),("auth_mode","login")]:
    if key not in st.session_state:
        st.session_state[key] = default

models = load_and_train_models()


# ─────────────────────────────────────────────
# LOGIN / SIGNUP PAGE
# ─────────────────────────────────────────────
def render_auth_page():
    st.markdown("""
    <div class="velour-header">
        <div class="velour-title">VELOUR</div>
        <div class="velour-subtitle">Personal Fashion Intelligence</div>
    </div>""", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        mode = st.radio("", ["Login","Sign Up"], horizontal=True,
                        index=0 if st.session_state.auth_mode=="login" else 1,
                        label_visibility="collapsed")
        st.session_state.auth_mode = "login" if mode=="Login" else "signup"
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown('<div class="login-title">Welcome Back</div><div class="login-sub">Sign in to your wardrobe</div>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", key="li_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass")
            if st.button("Sign In →", use_container_width=True):
                if username and password:
                    res = sign_in(username.strip(), password)
                    if res["success"]:
                        st.session_state.logged_in    = True
                        st.session_state.current_user = res["user"]
                        saved = load_profile(res["user"]["id"])
                        if saved: st.session_state.user_profile = saved
                        st.rerun()
                    else: st.error(res["error"])
                else: st.warning("Please fill in all fields.")
        else:
            st.markdown('<div class="login-title">Create Account</div><div class="login-sub">Join VELOUR today</div>', unsafe_allow_html=True)
            new_user = st.text_input("Choose a Username", placeholder="e.g. anushka_styles", key="su_user")
            new_pass = st.text_input("Choose a Password", type="password", placeholder="Min 6 characters", key="su_pass")
            confirm  = st.text_input("Confirm Password",  type="password", placeholder="Repeat password",   key="su_conf")
            if st.button("Create Account →", use_container_width=True):
                if not (new_user and new_pass and confirm): st.warning("Please fill in all fields.")
                elif len(new_pass) < 6:                     st.warning("Password must be at least 6 characters.")
                elif new_pass != confirm:                   st.error("Passwords do not match.")
                else:
                    res = sign_up(new_user.strip(), new_pass)
                    if res["success"]:
                        st.session_state.logged_in    = True
                        st.session_state.current_user = res["user"]
                        st.session_state.user_profile = {}
                        st.rerun()
                    else: st.error(res["error"])


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────
def render_main_app():
    user = st.session_state.current_user

    # ── SIDEBAR ───────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center;padding:1.2rem 0 0.8rem;'>
            <div style='font-family:"Cormorant Garamond",serif;font-size:1.9rem;letter-spacing:0.3em;color:#E8C99A;'>VELOUR</div>
            <div style='font-size:0.62rem;letter-spacing:0.22em;color:#C4874A;text-transform:uppercase;margin-top:2px;'>Fashion Intelligence</div>
        </div>
        <hr style='border-color:#4A2C17;margin:0.5rem 0 1rem;'>
        <div style='text-align:center;margin-bottom:1rem;'>
            <span class='user-badge'>👤 {user['username']}</span>
            <div style='font-size:0.65rem;color:#D4A574;margin-top:0.5rem;letter-spacing:0.06em;'>
                ID: {str(user['id'])[:8].upper()}
            </div>
        </div>
        <hr style='border-color:#4A2C17;margin:0.5rem 0 1rem;'>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">Your Profile</div>', unsafe_allow_html=True)
        saved = st.session_state.user_profile

        def idx(options, key):
            val = saved.get(key)
            return options.index(val) if val in options else 0

        gender     = st.selectbox("Gender",           ["Female","Male","Non-binary"],                                                                           index=idx(["Female","Male","Non-binary"],"gender"))
        age_group  = st.selectbox("Age Group",         ["18-25","26-35","36-45","46+"],                                                                         index=idx(["18-25","26-35","36-45","46+"],"age_group"))
        body_type  = st.selectbox("Body Type",         ["Hourglass","Pear","Apple","Rectangle","Athletic","Inverted Triangle"],                                 index=idx(["Hourglass","Pear","Apple","Rectangle","Athletic","Inverted Triangle"],"body_type"))
        weather    = st.selectbox("Current Weather",   ["Sunny","Rainy","Cloudy","Cold"],                                                                       index=idx(["Sunny","Rainy","Cloudy","Cold"],"weather"))
        occasion   = st.selectbox("Occasion",          ["Casual","Formal","Work","Party","Date"],                                                               index=idx(["Casual","Formal","Work","Party","Date"],"occasion"))
        style_pref = st.selectbox("Style Preference",  ["Minimalist","Classic","Trendy","Bohemian","Streetwear","Elegant","Romantic","Business"],                index=idx(["Minimalist","Classic","Trendy","Bohemian","Streetwear","Elegant","Romantic","Business"],"style_preference"))
        color_pref = st.selectbox("Colour Preference", ["Neutral","Bold","Pastel","Dark","Warm"],                                                               index=idx(["Neutral","Bold","Pastel","Dark","Warm"],"color_preference"))
        budget     = st.selectbox("Budget Range",      ["Low","Medium","High"],                                                                                 index=idx(["Low","Medium","High"],"budget_range"))
        fabric     = st.selectbox("Fabric Preference", ["Cotton","Wool","Silk","Linen","Polyester","Chiffon","Denim","Velvet"],                                 index=idx(["Cotton","Wool","Silk","Linen","Polyester","Chiffon","Denim","Velvet"],"fabric_preference"))
        fit        = st.selectbox("Fit Preference",    ["Slim","Regular","Loose"],                                                                              index=idx(["Slim","Regular","Loose"],"fit_preference"))

        new_profile = {
            "gender":gender,"age_group":age_group,"body_type":body_type,
            "weather":weather,"occasion":occasion,"style_preference":style_pref,
            "color_preference":color_pref,"budget_range":budget,
            "fabric_preference":fabric,"fit_preference":fit,
        }
        st.session_state.user_profile = new_profile

        if st.button("💾  Save Profile"):
            save_profile(user["id"], new_profile)
            st.success("Profile saved to Supabase!")

        st.markdown('<hr style="border-color:#4A2C17;margin:1rem 0;">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Weather API</div>', unsafe_allow_html=True)
        city    = st.text_input("City", placeholder="e.g. Mumbai")
        api_key = st.text_input("OpenWeatherMap Key", type="password", placeholder="Paste your key")
        if st.button("🌤  Get Weather"):
            if city and api_key:
                wdata = get_weather(city, api_key)
                if wdata: st.session_state["weather_data"] = wdata
                else: st.error("Could not fetch. Check city/key.")
            else: st.warning("Enter city and API key.")

        st.markdown('<hr style="border-color:#4A2C17;margin:1rem 0;">', unsafe_allow_html=True)
        if st.button("🚪  Log Out"):
            for k in ["logged_in","current_user","chat_history","user_profile","weather_data"]:
                st.session_state.pop(k, None)
            st.session_state.logged_in = False
            st.rerun()

    # ── HEADER ────────────────────────────────
    st.markdown(f"""
    <div class="velour-header">
        <div class="velour-title">VELOUR</div>
        <div class="velour-subtitle">Your Personal Fashion Intelligence Advisor</div>
        <div style='margin-top:0.8rem;'>
            <span class='user-badge'>👤 {user['username']} &nbsp;·&nbsp; ID: {str(user['id'])[:8].upper()}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    if "weather_data" in st.session_state:
        wd = st.session_state["weather_data"]
        st.markdown(f"""
        <div class="weather-card">
            <div class="city">📍 {wd['city']}</div>
            <div class="temp">{wd['temp']}°C</div>
            <div class="desc">{wd['desc']}</div>
        </div>""", unsafe_allow_html=True)
        st.session_state.user_profile["weather"] = weather_to_category(wd["icon"])

    tab_chat, tab_wardrobe, tab_trends, tab_rating = st.tabs(
        ["💬  Chat Advisor","👗  Wardrobe","✨  Trends","⭐  Outfit Rating"])

    profile = st.session_state.user_profile

    def ml_profile():
        return {
            "Weather":          profile.get("weather","Sunny"),
            "Occasion":         profile.get("occasion","Casual"),
            "Style_Preference": profile.get("style_preference","Classic"),
            "Body_Type":        profile.get("body_type","Hourglass"),
            "Color_Preference": profile.get("color_preference","Neutral"),
            "Fit_Preference":   profile.get("fit_preference","Regular"),
            "Fabric_Preference":profile.get("fabric_preference","Cotton"),
            "Gender":           profile.get("gender","Female"),
            "Age_Group":        profile.get("age_group","26-35"),
            "Budget_Range":     profile.get("budget_range","Medium"),
        }

    # ── CHAT TAB ──────────────────────────────
    with tab_chat:
        col_chat, col_info = st.columns([2,1])
        with col_chat:
            st.markdown('<div class="section-label">Chat with VELOUR</div>', unsafe_allow_html=True)
            chat_html = '<div class="chat-container">'
            if not st.session_state.chat_history:
                chat_html += f'<div class="msg-bot"><div class="bot-avatar">V</div><div class="bubble">Welcome back, <strong>{user["username"]}</strong>! Ask me to suggest an outfit, discover trends, rate your look, or manage your wardrobe 👗</div></div>'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div class="msg-user"><div class="bubble">{msg["text"]}</div></div>'
                else:
                    chat_html += f'<div class="msg-bot"><div class="bot-avatar">V</div><div class="bubble">{msg["text"]}</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

            c1, c2 = st.columns([5,1])
            with c1:
                user_input = st.text_input("", placeholder="Ask me anything about fashion...", label_visibility="collapsed", key="chat_input")
            with c2:
                send = st.button("Send →")

            if send and user_input.strip():
                intent = classify_intent(user_input)
                mp     = ml_profile()
                st.session_state.chat_history.append({"role":"user","text":user_input})
                reply  = INTENT_RESPONSES.get(intent, INTENT_RESPONSES["unknown"])
                if intent == "suggest_outfit":
                    outfit, desc = get_outfit_suggestion(mp["Weather"], mp["Occasion"], mp["Style_Preference"])
                    score = compute_outfit_rating(mp, models)
                    reply += f'<br><br><strong>{outfit}</strong><br><em style="color:#A0622A;">{desc}</em><br><br><span class="rating-badge">Match Score: {score}/10</span>'
                elif intent == "trend_advice":
                    chips = " ".join(f'<span class="trend-chip">{t}</span>' for t in TRENDS_BY_SEASON[get_current_season()])
                    reply += f"<br><br>{chips}"
                elif intent == "rate_outfit":
                    score = compute_outfit_rating(mp, models)
                    reply = f"Match score: <span class='rating-badge'>{score}/10</span> {'⭐'*int(score//2)}"
                elif intent == "style_tip":
                    reply += f"<br><br><em>{STYLE_TIPS.get(mp['Body_Type'],'Wear what makes you feel confident!')}</em>"
                elif intent == "weather_outfit":
                    outfit, desc = get_outfit_suggestion(mp["Weather"], mp["Occasion"], mp["Style_Preference"])
                    reply += f"<br><br><strong>{outfit}</strong><br><em style='color:#A0622A;'>{desc}</em>"
                st.session_state.chat_history.append({"role":"bot","text":reply})
                st.rerun()

        with col_info:
            st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)
            for p in ["Suggest an outfit for today","What are trending styles?","Rate my current outfit","Give me a style tip","What to wear in this weather?"]:
                if st.button(p, key=f"qp_{p}"):
                    intent = classify_intent(p)
                    mp     = ml_profile()
                    reply  = INTENT_RESPONSES.get(intent, INTENT_RESPONSES["unknown"])
                    if intent == "suggest_outfit":
                        outfit, desc = get_outfit_suggestion(mp["Weather"], mp["Occasion"], mp["Style_Preference"])
                        score = compute_outfit_rating(mp, models)
                        reply += f'<br><br><strong>{outfit}</strong><br><em style="color:#A0622A;">{desc}</em><br><br><span class="rating-badge">Match Score: {score}/10</span>'
                    elif intent == "trend_advice":
                        chips = " ".join(f'<span class="trend-chip">{t}</span>' for t in TRENDS_BY_SEASON[get_current_season()])
                        reply += f"<br><br>{chips}"
                    elif intent == "rate_outfit":
                        score = compute_outfit_rating(mp, models)
                        reply = f"Match score: <span class='rating-badge'>{score}/10</span>"
                    elif intent == "style_tip":
                        reply += f"<br><br><em>{STYLE_TIPS.get(mp['Body_Type'],'Wear what makes you feel confident!')}</em>"
                    elif intent == "weather_outfit":
                        outfit, desc = get_outfit_suggestion(mp["Weather"], mp["Occasion"], mp["Style_Preference"])
                        reply += f"<br><br><strong>{outfit}</strong><br><em style='color:#A0622A;'>{desc}</em>"
                    st.session_state.chat_history.append({"role":"user","text":p})
                    st.session_state.chat_history.append({"role":"bot","text":reply})
                    st.rerun()
            if st.button("🗑  Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

    # ── WARDROBE TAB ──────────────────────────
    with tab_wardrobe:
        st.markdown('<div class="section-label">My Wardrobe</div>', unsafe_allow_html=True)
        col_add, col_list = st.columns([1,2])
        ICONS = {"Tops":"👕","Bottoms":"👖","Dresses":"👗","Outerwear":"🧥","Footwear":"👠","Accessories":"💍","Bags":"👜"}

        with col_add:
            st.markdown("**Add New Item**")
            item_name     = st.text_input("Item Name",  placeholder="e.g. Black Blazer")
            item_category = st.selectbox("Category",    ["Tops","Bottoms","Dresses","Outerwear","Footwear","Accessories","Bags"])
            item_color    = st.text_input("Colour",     placeholder="e.g. Camel")
            item_occasion = st.selectbox("Best For",    ["Casual","Formal","Work","Party","Date","All"])
            item_season   = st.selectbox("Season",      ["All","Spring","Summer","Autumn","Winter"])
            if st.button("＋  Add to Wardrobe"):
                if item_name.strip():
                    ok = add_wardrobe_item(user["id"], {
                        "item_name": item_name.strip(), "category": item_category,
                        "color": item_color or "—", "occasion": item_occasion,
                        "season": item_season, "icon": ICONS.get(item_category,"👗"),
                    })
                    if ok: st.success(f"'{item_name}' added!"); st.rerun()
                    else:  st.error("Could not add. Check Supabase connection.")
                else: st.warning("Enter an item name.")

        with col_list:
            wardrobe = load_wardrobe(user["id"])
            if wardrobe:
                c1,c2,c3 = st.columns(3)
                c1.metric("Total Items", len(wardrobe))
                c2.metric("Categories",  len(set(i["category"] for i in wardrobe)))
                c3.metric("Outfits Est.", len(wardrobe)*2)
                st.markdown("<br>", unsafe_allow_html=True)
                filter_cat = st.selectbox("Filter", ["All"]+list(set(i["category"] for i in wardrobe)))
                shown = wardrobe if filter_cat=="All" else [i for i in wardrobe if i["category"]==filter_cat]
                for item in shown:
                    ci, cd = st.columns([5,1])
                    with ci:
                        st.markdown(f"""
                        <div class="wardrobe-item">
                            <div class="wardrobe-icon">{item.get('icon','👗')}</div>
                            <div><strong>{item['item_name']}</strong><br>
                            <span style="color:#A0622A;font-size:0.75rem;">{item['category']} · {item.get('color','—')} · {item['occasion']} · {item['season']}</span></div>
                        </div>""", unsafe_allow_html=True)
                    with cd:
                        if st.button("✕", key=f"del_{item['id']}"):
                            delete_wardrobe_item(item["id"]); st.rerun()
                if st.button("📥  Export CSV"):
                    df_w = pd.DataFrame(wardrobe)
                    st.download_button("Download", df_w.to_csv(index=False), f"wardrobe_{user['username']}.csv","text/csv")
            else:
                st.markdown("""
                <div style='text-align:center;padding:3rem;color:#C4874A;'>
                    <div style='font-size:3rem;'>👗</div>
                    <div style='font-family:"Cormorant Garamond",serif;font-size:1.3rem;'>Your wardrobe is empty</div>
                    <div style='font-size:0.8rem;margin-top:0.4rem;color:#A0622A;'>Add your first item using the form on the left</div>
                </div>""", unsafe_allow_html=True)

    # ── TRENDS TAB ────────────────────────────
    with tab_trends:
        st.markdown('<div class="section-label">Fashion Trends</div>', unsafe_allow_html=True)
        season = get_current_season()
        cols   = st.columns(2)
        for i, s in enumerate([season]+[x for x in ["Spring","Summer","Autumn","Winter"] if x!=season]):
            with cols[i%2]:
                border = "border-left:4px solid #C4874A;" if s==season else "border-left:4px solid #D4A574;"
                badge  = '<span style="background:#C4874A;color:#FFFDF8;padding:0.15rem 0.5rem;border-radius:10px;font-size:0.65rem;margin-left:0.5rem;">CURRENT</span>' if s==season else ""
                chips  = " ".join(f'<span class="trend-chip">{t}</span>' for t in TRENDS_BY_SEASON[s])
                st.markdown(f'<div class="outfit-card" style="{border}"><h4>{s} 2024 {badge}</h4><div style="margin-top:0.6rem;">{chips}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Personalised Trend Match</div>', unsafe_allow_html=True)
        mp = ml_profile()
        outfit, desc = get_outfit_suggestion(mp["Weather"], mp["Occasion"], mp["Style_Preference"])
        score = compute_outfit_rating(mp, models)
        st.markdown(f'<div class="outfit-card"><h4>Curated for {user["username"]} — {mp["Style_Preference"]} × {mp["Occasion"]}</h4><p>🎨 <strong>{outfit}</strong></p><p style="margin-top:0.4rem;">{desc}</p><div style="margin-top:0.6rem;"><span class="rating-badge">Trend Match: {score}/10</span></div></div>', unsafe_allow_html=True)

    # ── RATING TAB ────────────────────────────
    with tab_rating:
        st.markdown('<div class="section-label">ML Outfit Rating System</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Rate an Outfit**")
            r_w   = st.selectbox("Weather",  ["Sunny","Rainy","Cloudy","Cold"],                                                                          key="r_w")
            r_o   = st.selectbox("Occasion", ["Casual","Formal","Work","Party","Date"],                                                                  key="r_o")
            r_s   = st.selectbox("Style",    ["Minimalist","Classic","Trendy","Bohemian","Streetwear","Elegant","Romantic","Business"],                   key="r_s")
            r_b   = st.selectbox("Body",     ["Hourglass","Pear","Apple","Rectangle","Athletic","Inverted Triangle"],                                    key="r_b")
            r_c   = st.selectbox("Colour",   ["Neutral","Bold","Pastel","Dark","Warm"],                                                                  key="r_c")
            r_f   = st.selectbox("Fit",      ["Slim","Regular","Loose"],                                                                                 key="r_f")
            r_fab = st.selectbox("Fabric",   ["Cotton","Wool","Silk","Linen","Polyester","Chiffon","Denim","Velvet"],                                    key="r_fab")
            if st.button("⭐  Calculate Rating"):
                tp = {"Weather":r_w,"Occasion":r_o,"Style_Preference":r_s,"Body_Type":r_b,
                      "Color_Preference":r_c,"Fit_Preference":r_f,"Fabric_Preference":r_fab,
                      "Gender":"Female","Age_Group":"26-35","Budget_Range":"Medium"}
                score   = compute_outfit_rating(tp, models)
                outfit, desc = get_outfit_suggestion(r_w, r_o, r_s)
                verdict = "Exceptional ✨" if score>=9 else "Great 👏" if score>=7.5 else "Good 👍" if score>=6 else "Needs Work 🔧"
                st.session_state["last_rating"] = {"score":score,"stars":"⭐"*int(score//2),"verdict":verdict,"outfit":outfit,"desc":desc}
        with c2:
            if "last_rating" in st.session_state:
                r = st.session_state["last_rating"]
                st.markdown(f"""
                <div class="outfit-card" style="text-align:center;padding:2rem 1.4rem;">
                    <div style='font-family:"Cormorant Garamond",serif;font-size:3.5rem;color:#C4874A;font-weight:300;'>{r['score']}</div>
                    <div style='font-size:0.7rem;letter-spacing:0.15em;color:#A0622A;text-transform:uppercase;'>out of 10</div>
                    <div style='font-size:1.4rem;margin:0.5rem 0;'>{r['stars']}</div>
                    <div style='font-family:"Cormorant Garamond",serif;font-size:1.3rem;color:#2C1A0E;margin-bottom:1rem;'>{r['verdict']}</div>
                    <hr style='border-color:#E8C99A;'>
                    <div style='text-align:left;margin-top:0.8rem;'>
                        <strong style='color:#4A2C17;'>{r['outfit']}</strong>
                        <p style='color:#7B4A2D;font-size:0.82rem;margin-top:0.3rem;'>{r['desc']}</p>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align:center;padding:3rem;color:#C4874A;'>
                    <div style='font-size:3rem;'>⭐</div>
                    <div style='font-family:"Cormorant Garamond",serif;font-size:1.2rem;margin-top:0.5rem;'>Configure your outfit and click Calculate Rating</div>
                </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if st.session_state.logged_in and st.session_state.current_user:
    render_main_app()
else:
    render_auth_page()
