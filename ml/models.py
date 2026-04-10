# ─────────────────────────────────────────────
# ml/models.py — Train & cache all ML models
#
# Models trained here:
#   1. NLP Intent Classifier  — TF-IDF + Multinomial Naive Bayes
#      Input : raw chat sentence (string)
#      Output: intent label (suggest_outfit, trend_advice, etc.)
#
#   2. SVM Outfit Rater       — RBF SVM on encoded user profile
#      Input : encoded user preferences (numeric vector)
#      Output: style class probability → 0–10 match score
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from config import DATASET_PATH, CAT_COLS


# ─────────────────────────────────────────────
# NLP TRAINING DATA
# Each entry is (sentence, intent_label).
# The more varied the sentences, the better
# the model generalises to unseen user input.
# ─────────────────────────────────────────────
NLP_TRAINING_DATA = [

    # ── suggest_outfit ────────────────────────
    ("what should I wear today",                          "suggest_outfit"),
    ("suggest an outfit for me",                          "suggest_outfit"),
    ("recommend something to wear",                       "suggest_outfit"),
    ("can you pick an outfit",                            "suggest_outfit"),
    ("I have no idea what to put on",                     "suggest_outfit"),
    ("help me decide what to wear",                       "suggest_outfit"),
    ("give me an outfit idea",                            "suggest_outfit"),
    ("outfit for today please",                           "suggest_outfit"),
    ("what clothes should I pick",                        "suggest_outfit"),
    ("I need a look for tonight",                         "suggest_outfit"),
    ("dress me up",                                       "suggest_outfit"),
    ("what do you think I should wear",                   "suggest_outfit"),
    ("style me for today",                                "suggest_outfit"),
    ("plan my outfit",                                    "suggest_outfit"),
    ("pick clothes for me",                               "suggest_outfit"),
    ("I'm going out, what should I wear",                 "suggest_outfit"),
    ("need a fresh look",                                 "suggest_outfit"),
    ("suggest something stylish",                         "suggest_outfit"),
    ("what outfit fits my vibe",                          "suggest_outfit"),
    ("show me what to wear for a date",                   "suggest_outfit"),

    # ── trend_advice ──────────────────────────
    ("what's trending right now",                         "trend_advice"),
    ("show me current fashion trends",                    "trend_advice"),
    ("what are the popular styles this season",           "trend_advice"),
    ("tell me about fashion week looks",                  "trend_advice"),
    ("what's hot in fashion",                             "trend_advice"),
    ("latest fashion trends",                             "trend_advice"),
    ("what styles are in right now",                      "trend_advice"),
    ("what are people wearing these days",                "trend_advice"),
    ("fashion forecast",                                  "trend_advice"),
    ("what's in style",                                   "trend_advice"),
    ("show me trends",                                    "trend_advice"),
    ("what's popular in fashion",                         "trend_advice"),
    ("any new fashion trends",                            "trend_advice"),
    ("what should I follow this season",                  "trend_advice"),
    ("runway trends",                                     "trend_advice"),
    ("what are celebrities wearing",                      "trend_advice"),
    ("top fashion picks this season",                     "trend_advice"),
    ("spring fashion trends",                             "trend_advice"),
    ("winter style trends",                               "trend_advice"),
    ("what's the vibe this year",                         "trend_advice"),

    # ── rate_outfit ───────────────────────────
    ("rate my outfit",                                    "rate_outfit"),
    ("how good does my look score",                       "rate_outfit"),
    ("give my outfit a score",                            "rate_outfit"),
    ("how well does this outfit match",                   "rate_outfit"),
    ("score my style",                                    "rate_outfit"),
    ("is my outfit good",                                 "rate_outfit"),
    ("what's my outfit rating",                           "rate_outfit"),
    ("judge my look",                                     "rate_outfit"),
    ("how does my outfit rank",                           "rate_outfit"),
    ("evaluate my outfit",                                "rate_outfit"),
    ("tell me if my outfit is good",                      "rate_outfit"),
    ("how stylish is my look",                            "rate_outfit"),
    ("grade my outfit",                                   "rate_outfit"),
    ("what score does my look get",                       "rate_outfit"),
    ("outfit check",                                      "rate_outfit"),
    ("is this outfit a good match",                       "rate_outfit"),
    ("how does this look",                                "rate_outfit"),
    ("rate what I'm wearing",                             "rate_outfit"),
    ("how would you rate my style",                       "rate_outfit"),
    ("is this a good outfit combination",                 "rate_outfit"),

    # ── add_item ──────────────────────────────
    ("add a new item to my wardrobe",                     "add_item"),
    ("I bought a new jacket",                             "add_item"),
    ("save this to my wardrobe",                          "add_item"),
    ("put a dress in my wardrobe",                        "add_item"),
    ("add shoes to my collection",                        "add_item"),
    ("I want to save a new item",                         "add_item"),
    ("insert a top into my wardrobe",                     "add_item"),
    ("new item for my closet",                            "add_item"),
    ("I picked up a new outfit piece",                    "add_item"),
    ("update my wardrobe with a new item",                "add_item"),
    ("I got new clothes",                                 "add_item"),
    ("add this outfit piece",                             "add_item"),
    ("store a new item",                                  "add_item"),
    ("log a new clothing item",                           "add_item"),
    ("record a new wardrobe addition",                    "add_item"),
    ("I purchased new pants",                             "add_item"),
    ("add my new sneakers",                               "add_item"),
    ("save a scarf to my wardrobe",                       "add_item"),
    ("add a blazer to my collection",                     "add_item"),
    ("I want to track a new piece",                       "add_item"),

    # ── style_tip ─────────────────────────────
    ("give me a style tip",                               "style_tip"),
    ("how should I dress for my body type",               "style_tip"),
    ("any fashion advice for me",                         "style_tip"),
    ("style advice please",                               "style_tip"),
    ("how do I dress better",                             "style_tip"),
    ("what works for my body shape",                      "style_tip"),
    ("tips for dressing well",                            "style_tip"),
    ("fashion tips",                                      "style_tip"),
    ("how to look more stylish",                          "style_tip"),
    ("what should I know about my style",                 "style_tip"),
    ("styling advice",                                    "style_tip"),
    ("how to dress for my shape",                         "style_tip"),
    ("clothes that flatter my figure",                    "style_tip"),
    ("how to improve my style",                           "style_tip"),
    ("what cuts suit me",                                 "style_tip"),
    ("fashion guidance",                                  "style_tip"),
    ("how to dress my body type",                         "style_tip"),
    ("what to wear for my figure",                        "style_tip"),
    ("help me with style",                                "style_tip"),
    ("any tips on fashion",                               "style_tip"),

    # ── weather_outfit ────────────────────────
    ("what should I wear in the rain",                    "weather_outfit"),
    ("outfit for cold weather",                           "weather_outfit"),
    ("it's sunny today what do I wear",                   "weather_outfit"),
    ("dress me for the weather",                          "weather_outfit"),
    ("what to wear when it's cloudy",                     "weather_outfit"),
    ("it's freezing outside what do I wear",              "weather_outfit"),
    ("weather appropriate outfit",                        "weather_outfit"),
    ("outfit for hot weather",                            "weather_outfit"),
    ("what should I wear today it's raining",             "weather_outfit"),
    ("clothes for winter weather",                        "weather_outfit"),
    ("dress for the cold",                                "weather_outfit"),
    ("what works for rainy days",                         "weather_outfit"),
    ("outfit ideas for summer heat",                      "weather_outfit"),
    ("it's windy what should I wear",                     "weather_outfit"),
    ("dress for the weather today",                       "weather_outfit"),
    ("clothes for warm weather",                          "weather_outfit"),
    ("what to wear when it's stormy",                     "weather_outfit"),
    ("outfit suited for today's weather",                 "weather_outfit"),
    ("it's cold dress me up",                             "weather_outfit"),
    ("weather based outfit suggestion",                   "weather_outfit"),

    # ── greeting ──────────────────────────────
    ("hi",                                                "greeting"),
    ("hello",                                             "greeting"),
    ("hey there",                                         "greeting"),
    ("good morning",                                      "greeting"),
    ("good evening",                                      "greeting"),
    ("hey VELOUR",                                        "greeting"),
    ("what's up",                                         "greeting"),
    ("howdy",                                             "greeting"),
    ("greetings",                                         "greeting"),
    ("hi there",                                          "greeting"),
    ("hey how are you",                                   "greeting"),
    ("hello fashion advisor",                             "greeting"),
    ("yo",                                                "greeting"),
    ("sup",                                               "greeting"),
    ("namaste",                                           "greeting"),

    # ── unknown ───────────────────────────────
    ("what is the meaning of life",                       "unknown"),
    ("tell me a joke",                                    "unknown"),
    ("what's two plus two",                               "unknown"),
    ("who are you",                                       "unknown"),
    ("I don't know",                                      "unknown"),
    ("nothing",                                           "unknown"),
    ("never mind",                                        "unknown"),
    ("forget it",                                         "unknown"),
    ("what can you do",                                   "unknown"),
    ("just browsing",                                     "unknown"),
]


def _build_fallback_df() -> pd.DataFrame:
    """Minimal hardcoded dataset used if CSV is missing."""
    return pd.DataFrame({
        "Color_Preference":  ["Neutral", "Bold", "Pastel", "Dark", "Warm"] * 5,
        "Body_Type":         ["Hourglass", "Athletic", "Pear", "Rectangle", "Apple"] * 5,
        "Gender":            ["Female", "Male", "Female", "Male", "Female"] * 5,
        "Age_Group":         ["18-25", "26-35", "18-25", "36-45", "26-35"] * 5,
        "Weather":           ["Sunny", "Rainy", "Cloudy", "Cold", "Sunny"] * 5,
        "Occasion":          ["Casual", "Formal", "Party", "Work", "Date"] * 5,
        "Style_Preference":  ["Minimalist", "Classic", "Trendy", "Business", "Romantic"] * 5,
        "Budget_Range":      ["Medium", "High", "Low", "High", "Medium"] * 5,
        "Fabric_Preference": ["Cotton", "Wool", "Polyester", "Linen", "Silk"] * 5,
        "Fit_Preference":    ["Slim", "Regular", "Loose", "Regular", "Slim"] * 5,
        "Intent":            ["suggest_outfit"] * 25,
    })


def _train_nlp_intent_classifier() -> Pipeline:
    """
    Train a TF-IDF → Multinomial Naive Bayes pipeline on
    the NLP_TRAINING_DATA sentences above.

    Pipeline steps:
      1. TfidfVectorizer  — converts raw text → TF-IDF feature matrix
      2. MultinomialNB    — classifies the TF-IDF vectors into intent labels

    Returns a fitted sklearn Pipeline ready for .predict() calls.
    """
    sentences, labels = zip(*NLP_TRAINING_DATA)

    # TfidfVectorizer parameters explained:
    #   ngram_range=(1,2)  — use single words AND two-word pairs
    #                        "not wear" is captured as one feature
    #                        this helps with negation handling
    #   min_df=1           — include a term even if it appears only once
    #                        important since training set is small
    #   stop_words=None    — do NOT remove stop words like "not", "don't"
    #                        removing them would break negation detection
    #   sublinear_tf=True  — apply log(1 + tf) instead of raw tf
    #                        reduces dominance of very frequent words
    #   strip_accents='unicode' — normalise accented characters

    nlp_pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            stop_words=None,
            sublinear_tf=True,
            strip_accents="unicode",
            lowercase=True,
        )),
        ("clf", MultinomialNB(alpha=0.3)),
        #                     ↑
        # alpha = Laplace smoothing factor
        # Lower value (0.3) → model trusts training data more
        # Higher value (1.0) → more smoothing, safer for unseen words
        # 0.3 works well for a small, clean training set like ours
    ])

    nlp_pipeline.fit(sentences, labels)
    return nlp_pipeline


@st.cache_resource
def load_and_train_models() -> dict:
    """
    Load dataset, encode features, train all models.
    Cached by Streamlit — runs only once per session.

    Returns a dict containing:
        nlp_pipeline — TF-IDF + Naive Bayes for intent classification
        svm          — RBF SVM for outfit match scoring
        encoders     — dict of fitted LabelEncoders per column
        style_enc    — LabelEncoder for Style_Preference
        scaler       — fitted MinMaxScaler
    """
    # ── 1. Load tabular data ──────────────────
    try:
        df = pd.read_csv(DATASET_PATH).dropna()
    except Exception:
        df = _build_fallback_df()

    # ── 2. Encode categorical features ────────
    encoders = {col: LabelEncoder() for col in CAT_COLS}
    X = df[CAT_COLS].copy()
    for col in CAT_COLS:
        X[col] = encoders[col].fit_transform(X[col].astype(str))

    # ── 3. Scale to 0–1 ───────────────────────
    scaler   = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # ── 4. Train SVM for outfit rating ────────
    style_enc = LabelEncoder()
    y_style   = style_enc.fit_transform(df["Style_Preference"].astype(str))
    svm_model = SVC(kernel="rbf", probability=True, C=1.0, gamma="scale")
    svm_model.fit(X_scaled, y_style)

    # ── 5. Train NLP intent classifier ────────
    nlp_pipeline = _train_nlp_intent_classifier()

    return {
        "nlp_pipeline": nlp_pipeline,   # ← NEW: replaces old keyword matcher
        "svm":          svm_model,
        "encoders":     encoders,
        "style_enc":    style_enc,
        "scaler":       scaler,
    }
