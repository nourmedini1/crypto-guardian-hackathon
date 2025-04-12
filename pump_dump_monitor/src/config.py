import dotenv

# API Keys
API_KEYS = {
    'COINMARKETCAP': dotenv.get_key('.env', 'COINMARKETCAP_API_KEY'),
    'ETHERSCAN': dotenv.get_key('.env', 'ETHERSCAN_API_KEY')
}

# API Endpoints
PND_DETECTION_MODEL_ENDPOINT = "http://20.199.77.28:5040/pd/predict"
SCAM_ALERT_ENDPOINT = "http://20.199.77.28:5050/pd"

# Feature sanitization limits
MAX_VALUES = {
    'std_rush_order': 10,
    'avg_rush_order': 10,
    'std_trades': 100,
    'std_volume': 1e6,
    'avg_volume': 1e6,
    'std_price': 1,
    'avg_price': 1e4,
    'avg_price_max': 1e4
}

# Expected feature keys for model input
EXPECTED_FEATURE_KEYS = [
    "std_rush_order", "avg_rush_order", "std_trades",
    "std_volume", "avg_volume", "std_price", "avg_price",
    "avg_price_max", "hour_sin", "hour_cos", "minute_sin", "minute_cos"
]