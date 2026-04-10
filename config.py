
SUPABASE_URL = "https://wzdnthepblpxymniwmqq.supabase.co"  # ← paste your URL
SUPABASE_KEY = "sb_publishable_wiIEOzvU9LxVjXxCElBL4w_m2ZtST_m"             # ← paste your anon key

OPENWEATHER_API_KEY = "your-openweathermap-key-here"   # ← paste your key

DATASET_PATH = "fashion_dataset.csv"

CAT_COLS = [
    "Color_Preference", "Body_Type", "Gender", "Age_Group",
    "Weather", "Occasion", "Style_Preference", "Budget_Range",
    "Fabric_Preference", "Fit_Preference",
]

OPTIONS = {
    "gender":           ["Female", "Male", "Non-binary"],
    "age_group":        ["18-25", "26-35", "36-45", "46+"],
    "body_type":        ["Hourglass", "Pear", "Apple", "Rectangle", "Athletic", "Inverted Triangle"],
    "weather":          ["Sunny", "Rainy", "Cloudy", "Cold"],
    "occasion":         ["Casual", "Formal", "Work", "Party", "Date"],
    "style_preference": ["Minimalist", "Classic", "Trendy", "Bohemian", "Streetwear", "Elegant", "Romantic", "Business"],
    "color_preference": ["Neutral", "Bold", "Pastel", "Dark", "Warm"],
    "budget_range":     ["Low", "Medium", "High"],
    "fabric_preference":["Cotton", "Wool", "Silk", "Linen", "Polyester", "Chiffon", "Denim", "Velvet"],
    "fit_preference":   ["Slim", "Regular", "Loose"],
    "category":         ["Tops", "Bottoms", "Dresses", "Outerwear", "Footwear", "Accessories", "Bags"],
    "occasion_wear":    ["Casual", "Formal", "Work", "Party", "Date", "All"],
    "season":           ["All", "Spring", "Summer", "Autumn", "Winter"],
}

CATEGORY_ICONS = {
    "Tops": "👕", "Bottoms": "👖", "Dresses": "👗",
    "Outerwear": "🧥", "Footwear": "👠", "Accessories": "💍", "Bags": "👜",
}

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
    "Winter": ["Quiet Luxury", "Chocolate Brown Tones", "Shearling Everything", "Ballet Flats Revival", "Knit Sets"],
    "Summer": ["Coastal Grandmother", "Linen Suiting", "Crochet & Macramé", "Micro Bags", "Dopamine Dressing"],
    "Spring": ["Butter Yellow", "Floral Maximalism", "Sheer Layers", "Mary Janes", "Denim-on-Denim"],
    "Autumn": ["Burgundy & Rust", "Leather Trench Coats", "Chunky Loafers", "Plaid Everything", "Velvet Accents"],
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
    "greeting":       "👋 Hello! I'm VELOUR — ask me to suggest an outfit, check trends, or manage your wardrobe!",
    "unknown":        "Try: 'suggest an outfit', 'show trends', 'rate my outfit', or 'style tip'.",
}
WEATHER_MAP = {
    "Clear": "Sunny", "Clouds": "Cloudy",
    "Rain":  "Rainy", "Drizzle": "Rainy",
    "Snow":  "Cold",  "Thunderstorm": "Rainy",
}
