import requests
from config import BITQUERY_API_KEY

def get_token_holders_count(token_address):
    """Get the number of token holders using Bitquery API"""
    query = """
    {
      ethereum {
        transfers(
          currency: {is: "%s"}
          options: {limit: 10000}
        ) {
          receiver {
            address
          }
        }
      }
    }
    """ % token_address.lower()
    
    headers = {"X-API-KEY": BITQUERY_API_KEY}
    
    try:
        r = requests.post("https://graphql.bitquery.io", json={"query": query}, headers=headers)
        r.raise_for_status()
        data = r.json()
        
        transfers = data.get("data", {}).get("ethereum", {}).get("transfers", [])
        addresses = set()
        
        for tx in transfers:
            receiver = tx.get("receiver", {}).get("address")
            if receiver:
                addresses.add(receiver)
                
        return len(addresses)
    except Exception as e:
        print(f"Error retrieving holders count for {token_address} using Bitquery: {e}")
        return 0