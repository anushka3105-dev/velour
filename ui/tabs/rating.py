

import streamlit as st
from ml.predictor import compute_outfit_rating, get_outfit_suggestion
from utils.helpers import get_rating_verdict
from config import OPTIONS


def render_rating_tab(models: dict):
    """Render the outfit rating tab."""
    st.markdown('<div class="section-label">ML Outfit Rating System</div>', unsafe_allow_html=True)

    col_form, col_result = st.columns(2)

    with col_form:
        _render_rating_form(models)

    with col_result:
        _render_rating_result()

    _render_how_it_works()


# ── Private helpers ───────────────────────────

def _render_rating_form(models: dict):
    st.markdown("**Configure an Outfit**")

    r_weather  = st.selectbox("Weather",   OPTIONS["weather"],          key="r_w")
    r_occasion = st.selectbox("Occasion",  OPTIONS["occasion"],         key="r_o")
    r_style    = st.selectbox("Style",     OPTIONS["style_preference"], key="r_s")
    r_body     = st.selectbox("Body Type", OPTIONS["body_type"],        key="r_b")
    r_color    = st.selectbox("Colour",    OPTIONS["color_preference"], key="r_c")
    r_fit      = st.selectbox("Fit",       OPTIONS["fit_preference"],   key="r_f")
    r_fabric   = st.selectbox("Fabric",    OPTIONS["fabric_preference"],key="r_fab")

    if st.button("⭐  Calculate Rating"):
        test_profile = {
            "Weather":           r_weather,
            "Occasion":          r_occasion,
            "Style_Preference":  r_style,
            "Body_Type":         r_body,
            "Color_Preference":  r_color,
            "Fit_Preference":    r_fit,
            "Fabric_Preference": r_fabric,
            "Gender":            "Female",   # neutral defaults for rating
            "Age_Group":         "26-35",
            "Budget_Range":      "Medium",
        }
        score        = compute_outfit_rating(test_profile, models)
        outfit, desc = get_outfit_suggestion(r_weather, r_occasion, r_style)
        verdict      = get_rating_verdict(score)

        st.session_state["last_rating"] = {
            "score":   score,
            "stars":   "⭐" * int(score // 2),
            "verdict": verdict,
            "outfit":  outfit,
            "desc":    desc,
        }


def _render_rating_result():
    if "last_rating" not in st.session_state:
        st.markdown("""
        <div style='text-align:center; padding:3rem; color:#C4874A;'>
            <div style='font-size:3rem;'>⭐</div>
            <div style='font-family:"Cormorant Garamond",serif; font-size:1.2rem; margin-top:0.5rem;'>
                Configure your outfit and click Calculate Rating
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    r = st.session_state["last_rating"]
    st.markdown(f"""
    <div class="outfit-card" style="text-align:center; padding:2rem 1.4rem;">
        <div style='font-family:"Cormorant Garamond",serif; font-size:3.5rem; color:#C4874A; font-weight:300;'>
            {r['score']}
        </div>
        <div style='font-size:0.7rem; letter-spacing:0.15em; color:#A0622A; text-transform:uppercase;'>
            out of 10
        </div>
        <div style='font-size:1.4rem; margin:0.5rem 0;'>{r['stars']}</div>
        <div style='font-family:"Cormorant Garamond",serif; font-size:1.3rem; color:#2C1A0E; margin-bottom:1rem;'>
            {r['verdict']}
        </div>
        <hr style='border-color:#E8C99A;'>
        <div style='text-align:left; margin-top:0.8rem;'>
            <strong style='color:#4A2C17;'>{r['outfit']}</strong>
            <p style='color:#7B4A2D; font-size:0.82rem; margin-top:0.3rem;'>{r['desc']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_how_it_works():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">How the Rating Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="outfit-card">
        <p>The rating engine uses a trained <strong>Support Vector Machine (SVM)</strong> with an RBF kernel,
        trained on your preference dataset.</p>
        <p style="margin-top:0.5rem;">It encodes your outfit parameters — weather, occasion, style, body type,
        colour, fit, and fabric — then computes a <strong>probability confidence score</strong> via SVM's
        predict_proba, scaled to a 0–10 match rating.</p>
        <p style="margin-top:0.5rem;">Higher scores mean the outfit combination aligns more strongly with
        known high-confidence style profiles in the training data.</p>
    </div>
    """, unsafe_allow_html=True)
