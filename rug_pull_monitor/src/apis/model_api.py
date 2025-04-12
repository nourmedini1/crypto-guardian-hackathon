import requests
from config import RUGPULL_MODEL_URL, SCAM_ALERT_AGENT_URL

def send_rugpull_prediction_request(features, token):
    """Send feature data to rug pull prediction model"""
    payload = {"features": features, "token": token}
    
    try:
        response = requests.post(RUGPULL_MODEL_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending rug pull request: {e}")
        return None

def send_scam_alert(features, token):
    """Send alert to scam alert service"""
    payload = {"features": features, "token": token}
    
    try:
        response = requests.post(SCAM_ALERT_AGENT_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending scam alert: {e}")
        return None