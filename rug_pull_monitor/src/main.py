import time
import schedule
from scanner import scan_tokens
import requests_cache
from config import CACHE_EXPIRY

def main():
    """Run the token scanner"""
    print("Starting rug pull monitoring scan...")

# Setup cache for API requests
    requests_cache.install_cache('api_cache', expire_after=CACHE_EXPIRY)
    scan_tokens(limit=5)
    print("Scan completed.")

if __name__ == "__main__":
    # Schedule scan to run every 4 hours
    schedule.every(4).hours.do(main)
    print("Rug pull monitor initialized")
    print("Scheduler started. Running main() every 4 hours.")
    
    # Run once immediately on startup
    main()
    
    # Keep running the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)