"""
Background job scheduler for periodic tasks
"""
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from src.data.fetcher import fetch_yesterday_data
from src.data.loader import update_historical_data
from src.models.lstm import LSTMModel

logger = logging.getLogger(__name__)

def create_scheduler():
    """Create and configure the background scheduler"""
    scheduler = BackgroundScheduler()
    return scheduler

def setup_jobs(scheduler):
    """Set up scheduled jobs"""
    scheduler.add_job(daily_finetuning_job, 'cron', hour=6, minute=50)
    return scheduler

def daily_finetuning_job():
    """Daily job to fetch new data and fine-tune the model"""
    try:
        logger.info("Running daily fine-tuning job...")
        
        # Fetch new data
        new_data = fetch_yesterday_data()
        logger.info(f"Fetched data: {new_data}")
        
        # Update historical data
        df = update_historical_data(new_data)
        logger.info("Historical data updated.")
        
        # Fine-tune model
        model = LSTMModel()
        model.fine_tune(df)
        logger.info("Model fine-tuned successfully.")
    except Exception as e:
        logger.error(f"Error during daily fine-tuning job: {e}")