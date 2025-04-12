import requests
import time
from config import COINGECKO_BASE_URL, REQUEST_DELAY
import datetime

def get_coin_details(coin_id):
    """Get detailed information about a specific coin"""
    url = f"{COINGECKO_BASE_URL}/coins/{coin_id}?localization=false"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving details for coin {coin_id}: {e}")
        return None

def get_recent_coins(max_age_seconds, limit=5):
    """Get recently created coins filtered by age"""
    url_markets = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    
    try:
        response = requests.get(url_markets, params=params)
        response.raise_for_status()
        coins = response.json()
    except Exception as e:
        print(f"Error retrieving markets data: {e}")
        return []
        
    
    
    recent_coins = []
    now = datetime.datetime.utcnow()
    
    for coin in coins:
        coin_id = coin["id"]
        details = get_coin_details(coin_id)
        time.sleep(REQUEST_DELAY)
        
        if details is None:
            continue
            
        genesis_date = details.get("genesis_date")
        if not genesis_date:
            continue
            
        try:
            genesis_dt = datetime.datetime.strptime(genesis_date, "%Y-%m-%d")
        except Exception as e:
            continue
            
        age_seconds = (now - genesis_dt).total_seconds()
        
        if age_seconds < max_age_seconds:
            platforms = details.get("platforms", {})
            eth_address = platforms.get("ethereum")
            
            if eth_address:
                recent_coins.append({
                    "id": coin_id,
                    "symbol": details.get("symbol", "").upper(),
                    "genesis_date": genesis_date,
                    "contract_address": eth_address,
                    "decimals": 18, 
                    "market_data": details.get("market_data", {}),
                    "details": details
                })
                print(f"Found recent coin: {coin_id} (Genesis: {genesis_date})")
                
                if len(recent_coins) >= limit:
                    break
                    
    return recent_coins

def get_coin_price(token_details):
    """Extract USD price from token details"""
    try:
        market_data = token_details.get("market_data", {})
        current_price = market_data.get("current_price", {})
        return current_price.get("usd", None)
    except Exception as e:
        print(f"Error extracting price: {e}")
        return None