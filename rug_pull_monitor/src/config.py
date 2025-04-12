import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# API Keys and URLs
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
UNISWAP_SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
RUGPULL_MODEL_URL = "http://20.199.77.28:5060/rg/predict"
SCAM_ALERT_AGENT_URL = "http://20.199.77.28:5050/rg"

# Operational parameters
AGGREGATION_WINDOW = 24 * 3600      # 24 hours in seconds
MAX_TOKEN_AGE = 6 * 30 * 24 * 3600  # 6 months in seconds
REQUEST_DELAY = 10                  # Delay between API requests
HOLDER_THRESHOLD = 100              # Minimum number of holders
RUGPULL_THRESHOLD = 0.4             # Probability threshold for rugpull alerts
CACHE_EXPIRY = 3600 * 3             # Cache expiry time (3 hours)