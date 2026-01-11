from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load trained pipeline
model = joblib.load("xgboost_model.pkl")

app = FastAPI(title="Bengaluru House Price Predictor")

# Input schema (matches training features)
class HouseInput(BaseModel):
    location: str
    total_sqft: float
    bath: float
    bhk: float

@app.get("/")
def home():
    return {"message": "House Price Prediction API is running"}

@app.post("/predict")
def predict_price(data: HouseInput):
    # Convert input to DataFrame (IMPORTANT)
    input_df = pd.DataFrame([{
        "location": data.location,
        "total_sqft": data.total_sqft,
        "bath": data.bath,
        "bhk": data.bhk
    }])

    prediction = model.predict(input_df)[0]

    return {
        "predicted_price_lakhs": round(float(prediction), 2)
    }
