import dotenv

API_HASH = dotenv.get_key('.env', 'API_HASH')
API_ID = dotenv.get_key('.env', 'API_ID')
PHONE_NUMBER = dotenv.get_key('.env', 'PHONE_NUMBER')
MISTRAL_API_KEY = dotenv.get_key('.env', 'MISTRAL_API_KEY')
SCAM_ALERT_AGENT_URL = "http://20.199.77.28:5050/pd-alert"

PND_GROUPS = [
    'https://t.me/sharks_pump',
    'https://t.me/cryptoclubpump',
    'https://t.me/VerifiedCryptoNews',
    'https://t.me/mega_pump_group',
    'https://t.me/mega_pump_group_signals',
    'https://t.me/cryptoflashsignals',
    'https://t.me/RocketWallet_Official',
    'https://t.me/testing_scraping'
]

NEWS_GROUPS = [
    'https://t.me/ethereumnews',
    'https://t.me/VerifiedCryptoNews',
    'https://t.me/coinlistofficialchannel', 
]

MODEL = "mistral-large-latest"
