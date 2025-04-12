import requests
import schedule
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SENTIMENT_ANALYSIS_URL = 'http://20.199.77.28:5030/pd'
SCAM_ALERT_ENDPOINT = 'http://20.199.77.28:5050/pd-alert'

def run_sentiment_to_scam_alert():
    try:
        logging.info("Requesting sentiment analysis data...")
        response = requests.get(SENTIMENT_ANALYSIS_URL, timeout=15)
        response.raise_for_status()
        sentiment_data = response.json()  # Convert response to dictionary
        logging.info("Sentiment analysis data retrieved: %s", sentiment_data)
    except Exception as e:
        logging.error(f"Error fetching sentiment analysis: {e}")
        return

    try:
        logging.info("Sending sentiment data to scam alert agent...")
        alert_response = requests.post(SCAM_ALERT_ENDPOINT, json=sentiment_data, timeout=15)
        alert_response.raise_for_status()
        alert_result = alert_response.json()
        logging.info("Scam alert agent response: %s", alert_result)
    except Exception as e:
        logging.error(f"Error sending scam alert: {e}")

def main():
    schedule.every(2).minutes.do(run_sentiment_to_scam_alert)
    logging.info("Scheduler started, running every 2 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__ == "__main__":
    main()
