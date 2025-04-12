from fastapi import FastAPI, HTTPException
import joblib
import uvicorn
from prediction_request import PredictionRequest

app = FastAPI(description="Rug Pull Detection API", version="0.1.0")

model = joblib.load("stacked_rug_pull_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.post("rug-pull/predict")
def predict(request: PredictionRequest):
    try:
        features = request.to_numpy_array()
        features_scaled = scaler.transform(features)
        prediction_proba = model.predict_proba(features_scaled)[:, 1]
        return {
            "prediction_probability": float(prediction_proba[0])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("rug_pull_detection:app", host="0.0.0.0", port=5060)
