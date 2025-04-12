"""
Application entry point
"""
import uvicorn
import logging
from api.app import create_app
from api.routes import router
from utils.scheduler import create_scheduler, setup_jobs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = create_app()
app.include_router(router)

# Create and start scheduler
scheduler = create_scheduler()
scheduler = setup_jobs(scheduler)

if __name__ == "__main__":
    scheduler.start()
    uvicorn.run(app, host="0.0.0.0", port=5020)