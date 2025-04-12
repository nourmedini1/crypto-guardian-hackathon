import torch

class Config:
    """Centralized configuration settings"""
    MODEL_NAME = "BAAI/bge-m3"
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    VECTOR_STORE_PATH = "vector_store"