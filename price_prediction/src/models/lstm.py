"""
LSTM model management including loading, prediction, and fine-tuning.
"""
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
import pandas as pd

class LSTMModel:
    def __init__(self, model_path="crypto_lstm_model.h5", scaler_path="scaler.pkl"):
        """Initialize the LSTM model and scaler"""
        self.model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})
        self.scaler = joblib.load(scaler_path)
        self.seq_length = 30
        self.pred_length = 7
    
    def predict(self, data):
        """
        Predict future prices using the most recent sequence of data
        
        Args:
            data: DataFrame with preprocessed data
            
        Returns:
            List of predicted close prices
        """
        data_values = data.values
        n_features = data_values.shape[1]
        
        data_scaled = self.scaler.transform(data_values)
        
        if data_scaled.shape[0] < self.seq_length:
            raise ValueError("Not enough data for prediction.")
        
        last_sequence = data_scaled[-self.seq_length:]
        last_sequence = last_sequence.reshape(1, self.seq_length, n_features)
        
        predictions_scaled = self.model.predict(last_sequence)
        predictions_scaled = predictions_scaled.reshape(self.pred_length, 1)
        
        close_col_index = 3  # Assuming 'Close' is at index 3
        dummy_array = np.zeros((self.pred_length, n_features))
        dummy_array[:, close_col_index] = predictions_scaled.flatten()
        
        predictions_full = self.scaler.inverse_transform(dummy_array)
        predictions = predictions_full[:, close_col_index]
        
        return predictions.tolist()
    
    def fine_tune(self, df, epochs=2, batch_size=16, learning_rate=1e-7):
        """
        Fine-tune the model with new data
        
        Args:
            df: DataFrame with updated data
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate for optimizer
            
        Returns:
            Updated model and scaler
        """
        data = df.values
        
        self.scaler.fit(data)
        updated_scaled = self.scaler.transform(data)
        
        X, y = self._create_sequences_multi_step(updated_scaled, self.seq_length, self.pred_length)
        
        # Use recent data for fine-tuning
        if X.shape[0] > 100:
            X_finetune = X[-100:]
            y_finetune = y[-100:]
        else:
            X_finetune, y_finetune = X, y
        
        self.model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mse')
        self.model.fit(X_finetune, y_finetune, epochs=epochs, batch_size=batch_size, verbose=1)
        
        # Save updated model and scaler
        self.model.save("crypto_lstm_model.h5")
        joblib.dump(self.scaler, "scaler.pkl")
        
        return self
    
    def _create_sequences_multi_step(self, data, seq_length, pred_length):
        """Create sequences for multi-step prediction"""
        X, y = [], []
        for i in range(len(data) - seq_length - pred_length + 1):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length:i+seq_length+pred_length, 3])  # 3 is the index for 'Close'
        return np.array(X), np.array(y)