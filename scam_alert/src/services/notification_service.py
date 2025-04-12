import logging
import requests

from utils.config import CHATBOT_API_URL

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.subscribers = set()
        self.last_bot_message = {}
        
    def add_subscriber(self, chat_id):
        self.subscribers.add(chat_id)
        
    def update_last_message(self, chat_id, message):
        self.last_bot_message[chat_id] = message
        
    def get_last_message(self, chat_id):
        return self.last_bot_message.get(chat_id, "No previous message")
    
    def get_subscribers(self):
        return self.subscribers
    
    async def get_chatbot_response(self, user_message, chat_id):
        payload = {
            "user_question": user_message,
            "context": self.get_last_message(chat_id),
        }
        chatbot_response = "Sorry, I'm currently unavailable. Please try again later."
        try:
            response = requests.post(CHATBOT_API_URL, json=payload)
            llm_response = response.json()
            chatbot_response = llm_response.get("chatbot_response", chatbot_response)
        except Exception as e:
            logger.error(f"Error calling chatbot API for chat_id {chat_id}: {e}")
        
        return chatbot_response