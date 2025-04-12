import logging
from mistralai import Mistral

from utils.config import MISTRAL_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = MISTRAL_API_KEY
        self.model = LLM_MODEL
        self.client = Mistral(api_key=self.api_key)
    
    async def get_response(self, prompt):
        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return "Sorry, I'm currently unavailable. Please try again later."