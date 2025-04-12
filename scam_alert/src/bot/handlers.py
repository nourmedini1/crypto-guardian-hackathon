import logging
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

class TelegramHandlers:
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    async def start(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        self.notification_service.add_subscriber(chat_id)
        message = (
            "Welcome to CryptoGuardian!\n\n"
            "Stay ahead in the Crypto market with real-time updates!\n\n"
            "Latest Crypto News\n"
            "Market Insights & Price Trends\n"
            "Pump & Dump Warnings\n\n"
            "Rug Pull Alerts\n\n"
            "I'll keep you informed about the latest crypto movements. Stay safe, stay smart!\n\n"
            "Expect updates soon!"
        )
        await update.message.reply_text(message)
        self.notification_service.update_last_message(chat_id, message)
        logger.info(f"Sent welcome message to chat_id: {chat_id}")

    async def handle_message(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        user_message = update.message.text

        chatbot_response = await self.notification_service.get_chatbot_response(user_message, chat_id)
        
        await update.message.reply_text(chatbot_response)
        self.notification_service.update_last_message(chat_id, chatbot_response)
        logger.info(f"Processed message from chat_id {chat_id}")