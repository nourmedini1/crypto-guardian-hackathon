import dotenv

# Load environment variables
TOKEN = dotenv.get_key(".env", "TELEGRAM_TOKEN")
MISTRAL_API_KEY = dotenv.get_key(".env", "MISTRAL_API_KEY")
CHATBOT_API_URL = "http://20.199.77.28:5010/chat/"

# LLM Config
LLM_MODEL = "mistral-large-latest"

# Server Config
HOST = "0.0.0.0"
PORT = 5050