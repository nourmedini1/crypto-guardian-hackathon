import requests
import logging
import time
import schedule
from config import SCAM_ALERT_ENDPOINT
from pump_detector import PumpDetector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function that runs the pump & dump detection and alerts."""
    logging.info("Starting analysis job...")
    detector = PumpDetector()
    results = detector.analyze_coins()
    logging.info("Analysis Results: %s", results)
    
    # Check for coins predicted as pump & dump schemes
    alert_coins = [result for result in results if result.get("prediction", {}).get("prediction") == 1]
    
    if alert_coins:
        # Format data for the alert endpoint
        data = {alert_coins[i]['symbol']: alert_coins[i]['features'] for i in range(len(alert_coins))}
        try:
            response = requests.post(SCAM_ALERT_ENDPOINT, json=data, timeout=20)
            response.raise_for_status()
            logging.info("Scam alert sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send scam alert: {e}")
    else:
        logging.info("No pump and dump detected; no alert sent.")

if __name__ == "__main__":
    # Schedule to run every 4 hours
    schedule.every(4).hours.do(main)
    print("Scheduler started. Running main() every 4 hours.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)