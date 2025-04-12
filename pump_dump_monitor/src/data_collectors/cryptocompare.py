import requests
import numpy as np
import logging
from typing import Dict

class CryptoCompareCollector:
    def get_market_features(self, symbol: str) -> Dict:
        """Get market features from CryptoCompare for a given symbol."""
        try:
            url = "https://min-api.cryptocompare.com/data/v2/histominute"
            params = {"fsym": symbol.upper(), "tsym": "USD", "limit": 60}
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get("Response") == "Error" or "Data" not in data:
                logging.error(f"CryptoCompare error for {symbol}: {data.get('Message', 'Unknown error')}")
                return {}
                
            candles = data["Data"]["Data"]
            if not candles:
                return {}
                
            prices = [candle["close"] for candle in candles]
            volumes = [candle["volumeto"] for candle in candles]
            price_changes = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))] if len(prices) > 1 else []
            
            std_trades_market = 0.0  
            std_volume = np.std(volumes, ddof=1) if len(volumes) > 1 else 0.0
            avg_volume = np.mean(volumes) if volumes else 0.0
            std_price = np.std(price_changes, ddof=1) if len(price_changes) > 1 else 0.0
            avg_price = np.mean(prices) if prices else 0.0
            avg_price_max = max(prices) if prices else 0.0
            
            return {
                'std_trades': std_trades_market,  
                'std_volume': std_volume,
                'avg_volume': avg_volume,
                'std_price': std_price,
                'avg_price': avg_price,
                'avg_price_max': avg_price_max
            }
            
        except requests.exceptions.RequestException as e:
            logging.error(f"CryptoCompare API Error for {symbol}: {str(e)}")
            return {}