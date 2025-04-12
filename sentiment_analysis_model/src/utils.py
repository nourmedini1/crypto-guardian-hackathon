import requests
from config import SCAM_ALERT_AGENT_URL

async def send_pd_alert(blog):
    try:
        response = requests.post(SCAM_ALERT_AGENT_URL, json={"blog": blog})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending pd alert: {e}")
        return None
