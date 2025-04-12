import requests
import logging
import time
from typing import Dict, List
from config import PND_DETECTION_MODEL_ENDPOINT, EXPECTED_FEATURE_KEYS
from data_collectors.coinmarketcap import CoinMarketCapCollector
from feature_generator import FeatureGenerator

class PumpDetector:
    def __init__(self):
        self.coin_collector = CoinMarketCapCollector()
        self.feature_generator = FeatureGenerator()
    
    def analyze_coins(self) -> List[Dict]:
        """Analyze potentially risky coins for pump & dump patterns."""
        risky_coins = self.coin_collector.get_risky_coins()
        if not risky_coins:
            logging.warning("No risky coins found")
            return []
            
        predictions = []
        for coin in risky_coins:
            try:
                logging.info(f"Processing {coin['symbol']}")
                features = self.feature_generator.generate_features(
                    coin['symbol'], 
                    coin['contract_address']
                )
                
                # Prepare payload for model endpoint
                model_payload = {key: features.get(key, 0.0) for key in EXPECTED_FEATURE_KEYS}
                logging.info("Payload to model: %s", model_payload)
                
                # Call prediction model API
                headers = {"Content-Type": "application/json"}
                response = requests.post(
                    PND_DETECTION_MODEL_ENDPOINT, 
                    json=model_payload, 
                    headers=headers, 
                    timeout=20
                )
                response.raise_for_status()
                prediction = response.json()
                
                predictions.append({
                    'symbol': coin['symbol'],
                    'features': features,
                    'prediction': prediction
                })
                
                time.sleep(1)  # Avoid rate limiting
                
            except Exception as e:
                logging.error(f"Failed processing {coin['symbol']}: {str(e)}")
                continue
                
        return predictions