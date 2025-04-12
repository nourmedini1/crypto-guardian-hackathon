import time
from utils.time_utils import get_current_unix_time, parse_date_to_unix
from apis.coingecko_api import get_recent_coins, get_coin_price
from apis.etherscan_api import get_token_transactions
from apis.uniswap_api import get_pool_details
from apis.model_api import send_rugpull_prediction_request, send_scam_alert
from models.features import compute_features
from config import (
    MAX_TOKEN_AGE, AGGREGATION_WINDOW, REQUEST_DELAY, 
    RUGPULL_THRESHOLD
)

def scan_tokens(limit=5):
    """Main scanning function to detect potential rug pulls"""
    current_time = get_current_unix_time()
    print("Retrieving recent coins (less than 6 months old) from CoinGecko...")
    
    recent_coins = get_recent_coins(MAX_TOKEN_AGE, limit=limit)
    if not recent_coins:
        print("No recent coins found.")
        return

    for token in recent_coins:
        print(f"\nProcessing coin {token['id']} ({token['symbol']}) with contract: {token['contract_address']}")
        
        try:
            creation_time_unix = parse_date_to_unix(token["genesis_date"])
            if not creation_time_unix:
                continue
                
            if current_time - creation_time_unix > MAX_TOKEN_AGE:
                print("Token is older than 6 months. Skipping.")
                continue

            # Get recent transactions
            start_time = current_time - AGGREGATION_WINDOW
            tx_list = get_token_transactions(token["contract_address"], start_time)
            print(f"Found {len(tx_list)} transactions in the last 24 hours.")

            # Get price information
            price_usd = get_coin_price(token)
            if price_usd is None:
                print("Could not retrieve price. Skipping coin.")
                continue
            print(f"Current price: ${price_usd}")

            # Get liquidity information
            pool_details = get_pool_details(token["contract_address"])
            if pool_details:
                print("Liquidity pool details retrieved:")
                print(pool_details)
            else:
                print("No liquidity pool details found.")

            # Compute features for model
            features = compute_features(token, tx_list, current_time, price_usd, pool_details)
            print("Computed Features:")
            for k, v in features.items():
                print(f"  {k}: {v}")

            # Get prediction from rug pull model
            result = send_rugpull_prediction_request(features, token)
            if result and "prediction_probability" in result:
                prob = result["prediction_probability"]
                print(f"Detection Model Prediction Probability: {prob}")
                
                if prob > RUGPULL_THRESHOLD:
                    print(f"Probability exceeds threshold {RUGPULL_THRESHOLD}. Sending scam alert...")
                    alert_result = send_scam_alert(features, token)
                    print("Scam Alert Response:")
                    print(alert_result)
                else:
                    print(f"Probability below threshold {RUGPULL_THRESHOLD}. No scam alert sent.")
            else:
                print("No valid response from detection model.")

        except Exception as e:
            print(f"Error processing token {token['id']}: {e}")
            
        # Delay before processing next token
        time.sleep(REQUEST_DELAY)