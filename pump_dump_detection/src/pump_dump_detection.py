from fastapi import FastAPI, HTTPException
import joblib
from prediction_request import PredictionRequest
import uvicorn


app = FastAPI(description="Pump and Dump Detection API", version="0.1.0")

model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")


feature_columns = [
    'std_rush_order', 'avg_rush_order', 'std_trades', 'std_volume',
    'avg_volume', 'std_price', 'avg_price', 'avg_price_max',
    'hour_sin', 'hour_cos', 'minute_sin', 'minute_cos'
]

@app.post("/pump-dump/predict")
def predict(request: PredictionRequest):
    try:
        features = request.to_df(feature_columns)
        features_scaled = scaler.transform(features)
        prediction_proba = model.predict_proba(features_scaled)[:, 1]
        return {
            "prediction_probability": float(prediction_proba[0])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("pump_dump_detection:app", host="0.0.0.0", port=5080)
