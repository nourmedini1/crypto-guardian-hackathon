import requests
import numpy as np
import time
import logging
from typing import Dict
from config import API_KEYS
from utils import is_valid_erc20

class EtherscanCollector:
    def __init__(self):
        self.api_key = API_KEYS['ETHERSCAN']
    
    def get_transaction_features(self, contract_address: str) -> Dict:
        """Get transaction features from Etherscan for a given token contract."""
        if not contract_address or not is_valid_erc20(contract_address):
            logging.warning("Invalid or missing contract address; skipping Etherscan data.")
            return {'std_rush_order': 0.0, 'avg_rush_order': 0.0, 'std_trades': 0.0}
            
        try:
            end_time = int(time.time())
            start_time = end_time - 3600
            url = "https://api.etherscan.io/api"
            params = {
                'module': 'account',
                'action': 'tokentx',
                'contractaddress': contract_address,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'asc',
                'apikey': self.api_key,
                'startTimestamp': start_time,
                'endTimestamp': end_time
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != '1':
                logging.warning(f"Etherscan error: {data.get('message', 'Unknown error')}")
                return {'std_rush_order': 0.0, 'avg_rush_order': 0.0, 'std_trades': 0.0}
                
            tx_list = data['result']
            if not tx_list:
                return {'std_rush_order': 0.0, 'avg_rush_order': 0.0, 'std_trades': 0.0}
                
            values = [float(tx['value']) / 1e18 for tx in tx_list]
            timestamps = [int(tx['timeStamp']) for tx in tx_list]
            
            min_ts = min(timestamps)
            max_ts = max(timestamps)
            time_window = max_ts - min_ts if max_ts > min_ts else 1
            
            weighted_values = [v * ((ts - min_ts) / time_window) for v, ts in zip(values, timestamps)]
            std_rush_order = np.std(weighted_values, ddof=1) if len(weighted_values) > 1 else 0.0
            avg_rush_order = np.mean(weighted_values)
            std_trades = np.std(values, ddof=1) if len(values) > 1 else 0.0
            
            return {
                'std_rush_order': std_rush_order,
                'avg_rush_order': avg_rush_order,
                'std_trades': std_trades
            }
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Etherscan request failed: {str(e)}")
            return {'std_rush_order': 0.0, 'avg_rush_order': 0.0, 'std_trades': 0.0}