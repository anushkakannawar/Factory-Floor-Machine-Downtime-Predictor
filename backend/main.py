from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import joblib
import numpy as np
import os
from datetime import datetime, timedelta
import random

app = FastAPI(title="Factory Floor Machine Downtime Predictor")

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models/factory_model.pkl")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models/features.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "sensor_data.csv")

try:
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    df_raw = pd.read_csv(DATA_PATH)
    df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'])
except Exception as e:
    print(f"Error loading resources: {e}")

# Machine Stats Helper
def get_machine_health(machine_id):
    # Simulated current state: pick the latest record from history + small random jitter
    # (In a real app, this would be fresh incoming IoT data)
    m_data = df_raw[df_raw['machine_id'] == machine_id].sort_values('timestamp').iloc[-50:] # last 50
    latest = m_data.iloc[-1]
    
    # Calculate Risk Score (Pro Tip logic from USER)
    max_temp = 120
    vibration_weight = 10
    risk = (latest['temperature'] / max_temp) * (latest['vibration'] * vibration_weight)
    
    # Simple Health Score: (1 - normalized_risk) * 100
    health_score = max(0, min(100, 100 * (1 - risk)))
    
    # Prediction: Remaining Useful Life
    # We use features: temp, vib, press, rolling_mean... as per our model
    feature_row = []
    # Simplified live prediction (in prod we'd compute rolling averages for the last X pings)
    # Here we take the data as it was during simulation if available.
    # To be realistic, we re-run the prediction logic on the current packet
    
    # Fake a 'live' feature row for now based on the last record
    # (Since rolling averages require historical context)
    feature_vals = [
        latest['temperature'], latest['vibration'], latest['pressure'],
        m_data['temperature'].mean(), m_data['vibration'].mean(), m_data['pressure'].mean(),
        m_data['temperature'].std(), m_data['vibration'].std(), m_data['pressure'].std(),
        m_data.iloc[-2]['temperature'] if len(m_data) > 1 else latest['temperature'],
        m_data.iloc[-2]['vibration'] if len(m_data) > 1 else latest['vibration'],
        m_data.iloc[-2]['pressure'] if len(m_data) > 1 else latest['pressure']
    ]
    
    prediction = model.predict([feature_vals])[0]
    
    return {
        "machine_id": machine_id,
        "telemetry": {
            "temperature": latest['temperature'],
            "vibration": latest['vibration'],
            "pressure": latest['pressure'],
        },
        "health_score": round(health_score, 1),
        "predicted_rul": round(prediction, 1),
        "risk_level": round(risk, 3),
        "status": "Healthy" if health_score > 80 else ("Warning" if health_score > 40 else "Critical"),
        "history": m_data[['timestamp', 'temperature', 'vibration', 'pressure']].tail(20).to_dict('records')
    }

@app.get("/api/dashboard")
def get_dashboard():
    machines = df_raw['machine_id'].unique()
    return [get_machine_health(m) for m in machines]

@app.get("/")
def read_root():
    # Path relative to this script's directory
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(frontend_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
