import os
import json
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import HousePredictRequest, HousePredictResponse

app = FastAPI(title="House Price Prediction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تحديد مسارات الموديل والمناطق
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "house_price.pkl")
LOCATIONS_PATH = os.path.join(BASE_DIR, "models", "locations.json")

model = None
allowed_locations = []

@app.on_event("startup")
def load_assets():
    global model, allowed_locations
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    
    if os.path.exists(LOCATIONS_PATH):
        with open(LOCATIONS_PATH, "r") as f:
            allowed_locations = json.load(f)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/locations")
def get_locations():
    return {"locations": allowed_locations}

@app.post("/predict", response_model=HousePredictResponse)
def predict(payload: HousePredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    input_data = pd.DataFrame([payload.model_dump()])
    
    # التنبؤ (مع إرجاع السعر لقيمته الأصلية من اللوجاريتم)
    log_pred = model.predict(input_data)[0]
    predicted_price = round(float(np.expm1(log_pred)), 2)
    
    return HousePredictResponse(predicted_price=predicted_price)