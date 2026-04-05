import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

def create_features(df):
    """
    Feature Engineering for RUL prediction.
    - Rolling Averages: Smothes noise.
    - Lag features: Captures temporal changes.
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['machine_id', 'timestamp'])
    
    # Simple rolling averages (e.g., last 5 pings)
    for col in ['temperature', 'vibration', 'pressure']:
        df[f'{col}_rolling_mean'] = df.groupby('machine_id')[col].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
        df[f'{col}_rolling_std'] = df.groupby('machine_id')[col].transform(lambda x: x.rolling(window=5, min_periods=1).std()).fillna(0)
    
    # Lag features
    for col in ['temperature', 'vibration', 'pressure']:
        df[f'{col}_lag1'] = df.groupby('machine_id')[col].shift(1).fillna(method='bfill')
        
    return df

def train_model():
    if not os.path.exists('sensor_data.csv'):
        print("Dataset not found! Run simulator.py first.")
        return
        
    df = pd.read_csv('sensor_data.csv')
    df = create_features(df)
    
    # Features & Target
    features = [
        'temperature', 'vibration', 'pressure',
        'temperature_rolling_mean', 'vibration_rolling_mean', 'pressure_rolling_mean',
        'temperature_rolling_std', 'vibration_rolling_std', 'pressure_rolling_std',
        'temperature_lag1', 'vibration_lag1', 'pressure_lag1'
    ]
    X = df[features]
    y = df['rul_hours']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"Model Trained. MSE: {mse:.4f}")
    
    # Save model and feature list
    joblib.dump(model, 'ml_models/factory_model.pkl')
    joblib.dump(features, 'ml_models/features.pkl')
    print("Model saved to ml_models/factory_model.pkl")

if __name__ == "__main__":
    train_model()
