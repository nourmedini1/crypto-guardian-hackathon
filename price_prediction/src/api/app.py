"""
FastAPI application setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf

# Configure TensorFlow
tf.config.run_functions_eagerly(True)

def create_app():
    app = FastAPI(title="Crypto LSTM Prediction API")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app