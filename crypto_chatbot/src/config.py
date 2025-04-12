import logging
import dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model settings
RAG_MODEL_NAME = "BAAI/bge-m3"
MISTRAL_MODEL_NAME = "mistral-large-latest"
DEVICE = "cpu"

# API keys
MISTRAL_API_KEY = dotenv.get_key(".env", "MISTRAL_API_KEY")

# Vector store settings
VECTOR_STORE_PATH = "vector_store"