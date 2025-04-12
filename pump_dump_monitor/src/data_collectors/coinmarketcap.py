import requests
import logging
from typing import Dict, List
from datetime import datetime
from config import API_KEYS
from utils import is_valid_erc20

class CoinMarketCapCollector:
    def __init__(self):
        self.headers = {'X-CMC_PRO_API_KEY': API_KEYS['COINMARKETCAP']}
        self.base_params = {
            'convert': 'USD',
            'aux': 'num_market_pairs,date_added,platform'
        }
    
    def get_risky_coins(self) -> List[Dict]:
        """Fetch potentially risky coins from CoinMarketCap based on market cap, age, etc."""
        try:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            params = {**self.base_params, 'start': 1, 'limit': 500}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            risky_coins = []
            current_time = datetime.now()
            
            for coin in data['data']:
                try:
                    added_date = datetime.strptime(coin['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    age_days = (current_time - added_date).days
                    market_cap = coin['quote']['USD']['market_cap']
                    volume = coin['quote']['USD']['volume_24h']
                    
                    if (market_cap < 1e8 or volume < 5e6) or age_days < 365 or coin['num_market_pairs'] < 3:
                        contract_address = None
                        if coin.get('platform'):
                            addr = coin['platform'].get('token_address')
                            if is_valid_erc20(addr):
                                contract_address = addr
                            else:
                                logging.warning(f"Invalid contract address for {coin['symbol']}")
                        
                        risky_coins.append({
                            'symbol': coin['symbol'],
                            'contract_address': contract_address,
                            'market_cap': market_cap,
                            'volume_24h': volume,
                            'age_days': age_days
                        })
                except KeyError as e:
                    logging.warning(f"Missing field {str(e)} in coin data")
                    continue
                    
            logging.info(f"Found {len(risky_coins)} risky coins.")
            return sorted(risky_coins, key=lambda x: x['market_cap'])[:10]
            
        except requests.exceptions.RequestException as e:
            logging.error(f"CMC API Error: {str(e)}")
            return []