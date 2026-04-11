# VELOUR — AI Fashion Advisor

> A machine learning powered personal fashion advisor built with Python, Streamlit, and Supabase.

VELOUR understands what you want to wear through natural language, suggests outfits based on your body type, style preferences, and live weather — and manages your wardrobe, all in one app.

---

## Features

- **NLP Chat Interface** — Type naturally. TF-IDF + Naive Bayes classifies your intent from free text
- **ML Outfit Suggestions** — SVM trained on user preference data recommends outfits by weather, occasion, and style
- **Outfit Rating System** — ML model scores any outfit combination 0–10 based on match confidence
- **Wardrobe Manager** — Add, filter, and export your clothing items per user account
- **Trend Explorer** — Season-aware fashion trend discovery personalised to your style profile
- **Weather Integration** — Live weather via OpenWeatherMap auto-adjusts outfit suggestions
- **User Authentication** — Multi-user login system with Supabase, SHA-256 password hashing, and per-user data isolation
- **Conditional UI** — Smart form rendering (e.g. body type field hidden for male users)

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| ML — Intent | TF-IDF Vectoriser + Multinomial Naive Bayes |
| ML — Rating | Support Vector Machine (RBF kernel) |
| Data | Pandas, NumPy, Scikit-learn |
| Auth & DB | Supabase (PostgreSQL) |
| Language | Python 3.10+ |

---

## Project Structure

```
velour/
├── app.py                    ← Entry point — run this
├── config.py                 ← All constants, API keys, dropdown options, data
├── requirements.txt
│
├── auth/
│   ├── __init__.py
│   └── supabase_auth.py      ← sign_in, sign_up, password hashing, validation
│
├── database/
│   ├── __init__.py
│   └── db.py                 ← Supabase singleton client, profile & wardrobe queries
│
├── ml/
│   ├── __init__.py
│   ├── models.py             ← Train & cache NLP pipeline + SVM (runs once per session)
│   └── predictor.py          ← classify_intent, compute_outfit_rating, build_bot_reply
│
├── ui/
│   ├── __init__.py
│   ├── styles.py             ← Full brown & beige CSS theme
│   ├── auth_page.py          ← Login and sign up screens
│   ├── sidebar.py            ← Profile form, weather input, logout
│   └── tabs/
│       ├── __init__.py
│       ├── chat.py           ← Chat advisor tab
│       ├── wardrobe.py       ← Wardrobe manager tab
│       ├── trends.py         ← Trends discovery tab
│       └── rating.py         ← Outfit rating tab
│
└── utils/
    ├── __init__.py
    ├── helpers.py            ← Shared utility functions
    └── weather.py            ← OpenWeatherMap API integration
```

---

## How the ML Works

### Intent Classification (NLP)
User messages are classified into intents using a scikit-learn `Pipeline`:

```
Raw text → TfidfVectorizer (ngram_range=1,2) → MultinomialNB → Intent label
```

- **TF-IDF** converts sentences into weighted numeric vectors
- **Bigrams** capture phrases like "don't suggest" or "not recommend" for negation handling
- **Naive Bayes** calculates the probability of each intent and picks the highest confidence one
- A **confidence threshold** (0.25) returns `unknown` rather than a low-confidence wrong answer

### Outfit Rating (SVM)
User profile features (weather, occasion, style, body type, etc.) are encoded and rated:

```
Profile dict → LabelEncoder (per column) → MinMaxScaler → SVM predict_proba → 0–10 score
```

- **LabelEncoder** converts categorical strings to integers
- **MinMaxScaler** rescales all features to 0–1 so no single feature dominates
- **SVM (RBF kernel)** classifies the profile into a style class and returns confidence probabilities
- The highest class probability × 10 becomes the outfit match score

---

## Dataset

The ML models are trained on a synthetic 700-row fashion preference dataset with 11 columns. The `Intent` column serves as the target label for classification. Place the CSV in the project root before running.

---

## Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
supabase>=2.0.0
requests>=2.31.0
joblib>=1.3.0
```
