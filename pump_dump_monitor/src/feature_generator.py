import logging
from typing import Dict
from utils import sanitize_features
from config import EXPECTED_FEATURE_KEYS
from data_collectors.etherscan import EtherscanCollector
from data_collectors.cryptocompare import CryptoCompareCollector
from data_collectors.time_features import TimeFeatureCollector

class FeatureGenerator:
    def __init__(self):
        self.etherscan_collector = EtherscanCollector()
        self.cryptocompare_collector = CryptoCompareCollector()
        self.time_collector = TimeFeatureCollector()
    
    def generate_features(self, symbol: str, contract_address: str) -> Dict:
        """Generate all features needed for the pump & dump prediction model."""
        features = {}
        
        # Collect features from different sources
        features.update(self.time_collector.calculate_time_features())
        features.update(self.etherscan_collector.get_transaction_features(contract_address))
        features.update(self.cryptocompare_collector.get_market_features(symbol))
        
        # Ensure all expected keys are present
        for key in EXPECTED_FEATURE_KEYS:
            if key not in features or features[key] is None:
                features[key] = 0.0
                
        # Sanitize features to prevent extreme values
        return sanitize_features(features)