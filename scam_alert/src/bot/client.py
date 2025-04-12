import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from utils.config import TOKEN
from handlers import TelegramHandlers

logger = logging.getLogger(__name__)

class TelegramBotClient:
    def __init__(self, notification_service):
        self.token = TOKEN
        self.notification_service = notification_service
        self.handlers = TelegramHandlers(notification_service)
        self.application = None
    
    async def initialize(self):
        self.application = Application.builder().token(self.token).build()
        
        # Register handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
        )
        
        await self.application.initialize()
        logger.info("Telegram bot initialized")
        
    async def start(self):
        if self.application:
            await self.application.start()
            await self.application.updater.start_polling()
            logger.info("Telegram bot started and polling is active")
        else:
            logger.error("Cannot start uninitialized Telegram bot")
    
    async def stop(self):
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Telegram bot shutdown complete")