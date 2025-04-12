import time
import datetime

def get_current_unix_time():
    """Return current time as Unix timestamp"""
    return int(time.time())

def parse_date_to_unix(date_str, format="%Y-%m-%d"):
    """Convert date string to Unix timestamp"""
    try:
        dt = datetime.datetime.strptime(date_str, format)
        return int(dt.timestamp())
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return None

def get_seconds_since(timestamp):
    """Get seconds elapsed since the given timestamp"""
    now = datetime.datetime.utcnow()
    dt = datetime.datetime.fromtimestamp(timestamp)
    return (now - dt).total_seconds()

def seconds_to_months(seconds):
    """Convert seconds to months (approximate)"""
    return seconds / (30 * 24 * 3600)