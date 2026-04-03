# 👗 VELOUR — Fashion Advisor Chatbot

A ML-powered personal fashion advisor built with Streamlit, Scikit-learn, Pandas & NumPy.

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements(1).txt
```

### 2. Add your dataset
Place your `fashion_dataset.csv` in the same folder as `app.py`.
Required columns:
```
Color_Preference, Body_Type, Gender, Age_Group, Weather,
Occasion, Style_Preference, Budget_Range, Fabric_Preference,
Fit_Preference, Intent
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## 🌤️ Weather API Setup

1. Go to [openweathermap.org/api](https://openweathermap.org/api) and sign up for a **free API key**
2. In the app sidebar → **Weather API** section → paste your key
3. Enter your city and click **Get Weather**

> The app will automatically adjust outfit suggestions based on live weather!

---

## 🤖 ML Models Used

| Model | Purpose |
|-------|---------|
| **Naive Bayes** | Intent classification from chat input |
| **SVM (RBF kernel)** | Outfit match scoring & style classification |

---

## ✨ Features

- 💬 **Chat Advisor** — Natural language fashion Q&A
- 👗 **Wardrobe Manager** — Add/remove/export clothing items
- ✨ **Trend Explorer** — Season-based trend discovery
- ⭐ **Outfit Rater** — ML-powered match scoring (0–10)
- 🌤️ **Weather Integration** — Live weather-aware suggestions
- 🎨 **Brown & Beige Theme** — Luxury editorial aesthetic
