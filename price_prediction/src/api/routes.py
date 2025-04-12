
from fastapi import APIRouter, HTTPException
from data.loader import load_data
from models.lstm import LSTMModel

router = APIRouter()
model = LSTMModel()

@router.get("/predict")
def predict():
    try:
        # Load the preprocessed data
        df = load_data()
        
        # Make prediction
        predictions = model.predict(df)
        
        return {"predicted_close_prices": predictions}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")