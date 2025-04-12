import requests
from config import ETHERSCAN_API_KEY

def get_token_transactions(token_address, start_time, api_key=ETHERSCAN_API_KEY):
    """Get token transactions from Etherscan API"""
    params = {
        "module": "account",
        "action": "tokentx",
        "contractaddress": token_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key,
    }
    
    try:
        r = requests.get("https://api.etherscan.io/api", params=params)
        r.raise_for_status()
        data = r.json()
        
        if data.get("status") == "1":
            txs = data.get("result", [])
            return [tx for tx in txs if int(tx["timeStamp"]) >= start_time]
    except Exception as e:
        print(f"Error retrieving transactions for {token_address}: {e}")
        
    return []