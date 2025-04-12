"""
Data fetching from external sources
"""
import requests
from datetime import datetime, timedelta

def fetch_yesterday_data(symbol="ETHUSDT"):
    """
    Fetch yesterday's data from Binance API
    
    Args:
        symbol: Trading symbol
    
    Returns:
        Dictionary with yesterday's OHLCV data
    """
    end_time = int(datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000) - 1
    start_time = int((datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).timestamp() * 1000)
    
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1d",
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from Binance: " + response.text)
    data = response.json()
    
    if len(data) == 0:
        raise Exception("No data returned from Binance for the given period.")
    
    kline = data[0]
    
    daily_data = {
        "date": datetime.utcfromtimestamp(kline[0]/1000).strftime("%b %d, %Y"),
        "open": float(kline[1]),
        "high": float(kline[2]),
        "low": float(kline[3]),
        "close": float(kline[4]),
        "volume": float(kline[5])
    }
    return daily_data