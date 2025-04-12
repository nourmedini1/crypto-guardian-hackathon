import requests
from config import UNISWAP_SUBGRAPH_URL

def get_pool_details(token_contract_address):
    """Get Uniswap pool details for a token"""
    query = """
    {
      pools(where: { token0: "%s" }) {
        id
        liquidity
        feeTier
      }
    }
    """ % token_contract_address.lower()
    
    try:
        response = requests.post(UNISWAP_SUBGRAPH_URL, json={"query": query})
        response.raise_for_status()
        data = response.json()
        pools = data.get("data", {}).get("pools", [])
        
        if pools:
            pool = max(pools, key=lambda x: float(x["liquidity"]))
            return pool
    except Exception as e:
        print(f"Error retrieving Uniswap pool details: {e}")
        
    return None

def fetch_pool_day_data(pool_id, start_timestamp):
    """Fetch daily pool data from Uniswap subgraph"""
    query = """
    {
      poolDayData(
        where: { pool: "%s", date_gt: %d },
        orderBy: date,
        orderDirection: asc
      ) {
        date
        liquidity
      }
    }
    """ % (pool_id.lower(), start_timestamp)
    
    try:
        response = requests.post(UNISWAP_SUBGRAPH_URL, json={"query": query})
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("poolDayData", [])
    except Exception as e:
        print(f"Error fetching pool day data: {e}")
        return []

def compute_liquidity_metrics(pool_day_data):
    """Compute liquidity metrics from pool data"""
    liquidity_values = [float(entry["liquidity"]) for entry in pool_day_data if entry.get("liquidity")]
    
    if not liquidity_values:
        return 0.0, 0.0, 0.0
        
    peak = max(liquidity_values)
    trough = min(liquidity_values)
    current = liquidity_values[-1]
    
    drawdown = (peak - trough) / peak if peak > 0 else 0.0
    recovery = (current - trough) / (peak - trough) if (peak - trough) > 0 else 0.0
    
    return peak, drawdown, recovery