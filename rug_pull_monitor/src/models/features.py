import numpy as np
import datetime
from utils.time_utils import seconds_to_months
from apis.bitquery_api import get_token_holders_count
from apis.uniswap_api import fetch_pool_day_data, compute_liquidity_metrics
from config import HOLDER_THRESHOLD

def compute_features(token, tx_list, current_time, price_usd, pool_details):
    """Compute features for rug pull detection model"""
    try:
        creation_dt = datetime.datetime.strptime(token["genesis_date"], "%Y-%m-%d")
    except Exception as e:
        print(f"Error parsing creation time for {token['id']}: {e}")
        return {}
        
    coin_age_seconds = (datetime.datetime.utcnow() - creation_dt).total_seconds()
    coin_age_months = seconds_to_months(coin_age_seconds)
    
    # Process transaction data
    no_of_transactions = len(tx_list)
    decimals = token.get("decimals", 18)
    volumes = []
    tx_times = []
    
    for tx in tx_list:
        try:
            value = float(tx.get("value", 0)) / (10 ** decimals)
        except:
            value = 0.0
        volumes.append(value * price_usd)
        tx_times.append(int(tx["timeStamp"]))
        
    total_volume_usd = sum(volumes) if volumes else 0.0
    max_volume_usd = max(volumes) if volumes else 0.0
    
    if volumes and tx_times:
        max_idx = volumes.index(max_volume_usd)
        time_hr_diff = (tx_times[max_idx] - int(creation_dt.timestamp())) / 3600.0
    else:
        time_hr_diff = 0.0
        
    time_day_diff = time_hr_diff / 24.0
    price_volatility = np.std(volumes) if len(volumes) > 1 else 0.0

    # Process liquidity data
    liquidity_drawdown = 0.0
    liquidity_recovery = 0.0
    
    if pool_details:
        pool_id = pool_details.get("id")
        start_timestamp = current_time - 24 * 3600
        pool_day_data = fetch_pool_day_data(pool_id, start_timestamp)
        
        if pool_day_data:
            _, drawdown, recovery = compute_liquidity_metrics(pool_day_data)
            liquidity_drawdown = drawdown
            liquidity_recovery = recovery

    # Get holder statistics
    holders_count = get_token_holders_count(token["contract_address"])
    trust_in_owners = 0.5 if holders_count > HOLDER_THRESHOLD else 0.0

    # Assemble feature dictionary
    features = {
        "coin_age_months": coin_age_months,
        "trust_in_owners": trust_in_owners,
        "no_of_transactions": no_of_transactions,
        "volume_usd": total_volume_usd,
        "no_of_holders": holders_count,
        "max_volume_usd": max_volume_usd,
        "time_hr_diff": time_hr_diff,
        "time_day_diff": time_day_diff,
        "price_usd": price_usd,
        "price_volatility": price_volatility,
        "liquidity_drawdown": liquidity_drawdown,
        "liquidity_recovery": liquidity_recovery,
        "price_total_variation": np.sum(np.abs(np.diff(volumes))) if len(volumes) > 1 else 0.0
    }
    
    return features