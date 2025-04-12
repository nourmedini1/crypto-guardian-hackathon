from mistralai import Mistral
from config import MISTRAL_API_KEY, MISTRAL_MODEL_NAME, logger

class LLMClient:
    def __init__(self):
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.model_name = MISTRAL_MODEL_NAME
    
    def generate_response(self, prompt):
        """Generate a response from the LLM"""
        logger.info(f"Sending prompt to LLM (first 200 chars): {prompt[:200]}...")
        
        chat_response = self.client.chat.complete(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        
        raw_message = chat_response.choices[0].message.content
        logger.info(f"Received raw response from LLM")
        return raw_message