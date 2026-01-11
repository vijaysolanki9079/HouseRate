import streamlit as st
import requests
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bengaluru House Price Predictor",
    page_icon="🏡",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
# ---------------- GLOBAL DARK THEME ----------------
st.markdown("""
<style>
    /* App Background */
    .stApp {
        background-color: #0e1117;
        color: #e5e7eb;
    }

    /* Headings & Text */
    h1, h2, h3, h4, h5, p, span, label {
        color: #e5e7eb !important;
    }

    /* Input Fields */
    input, textarea, select {
        background-color: #1f2933 !important;
        color: #f9fafb !important;
        border: 1px solid #374151 !important;
        border-radius: 6px;
        padding: 6px;
    }

    /* Buttons */
    button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100%;
    }

    button:hover {
        background-color: #1d4ed8 !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        background-color: #020617;
        border: 1px solid #1e293b;
        color: #e5e7eb;
        border-radius: 8px;
    }

    /* Number input arrows fix */
    button[title="Increment"], button[title="Decrement"] {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("## 🏡 Bengaluru House Price Prediction")
st.markdown("---")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../backend/Cleaned_data.csv")
        return sorted(df["location"].unique())
    except FileNotFoundError:
        return []

locations = load_data()

if not locations:
    st.error("⚠️ Could not load data. Please check if 'Cleaned_data.csv' exists.")

# ---------------- INPUT SECTION ----------------
df = pd.read_csv("../backend/Cleaned_data.csv")
locations = sorted(df["location"].unique())

st.markdown("### 📋 Property Details")

location = st.selectbox("📍 Location", locations)

col1, col2 = st.columns(2)
with col1:
    total_sqft = st.number_input("📐 Total Square Feet", min_value=300, step=50)
with col2:
    bhk = st.number_input("🛏️ BHK", min_value=1, step=1)

bath = st.number_input("🚿 Bathrooms", min_value=1, step=1)


# ---------------- PREDICTION BUTTON ----------------
def format_price(price_lakhs):
    if price_lakhs >= 100:
        price_cr = price_lakhs / 100
        return f"₹ {price_cr:.2f} Cr"
    else:
        return f"₹ {price_lakhs:.2f} Lakhs"


if st.button("🔮 Predict Price"):
    payload = {
        "location": location,
        "total_sqft": total_sqft,
        "bath": bath,
        "bhk": bhk
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            price = response.json().get("predicted_price_lakhs", 0)

            if price < 0:
                price = 0

            formatted_price = format_price(price)
            st.success(f"💰 Estimated Price: {formatted_price}")
        else:
            st.error("❌ Prediction failed")

    except Exception:
        st.error("🚫 Backend is not running")
