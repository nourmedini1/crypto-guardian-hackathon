import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from utils.logging_setup import setup_logging
from utils.config import HOST, PORT
from bot.client import TelegramBotClient
from services.notification_service import NotificationService
from services.llm_service import LLMService
from api.routes import router

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services
    notification_service = NotificationService()
    llm_service = LLMService()
    bot_client = TelegramBotClient(notification_service)
    
    # Initialize and start the bot
    await bot_client.initialize()
    await bot_client.start()
    
    # Store references in app state
    app.state.telegram_bot = bot_client.application.bot
    app.state.notification_service = notification_service
    app.state.llm_service = llm_service
    
    logger.info("Application started successfully")
    yield
    
    # Shutdown bot
    await bot_client.stop()
    logger.info("Application shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="CryptoGuardian API",
    description="API for sending crypto scam alerts via Telegram",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(router)

# Create __init__.py files
def create_init_files():
    import os
    for dir_path in ['api', 'bot', 'services', 'utils']:
        init_path = os.path.join('src', dir_path, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                pass

if __name__ == "__main__":
    create_init_files()
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)