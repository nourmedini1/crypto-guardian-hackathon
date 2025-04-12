import json
from config import logger

class ResponseParser:
    @staticmethod
    def parse_response(raw_message):
        """Parse the raw LLM response into structured data"""
        response_json = None
        
        # Try direct JSON parsing
        try:
            response_json = json.loads(raw_message)
        except Exception as e:
            logger.warning(f"Direct JSON parsing failed: {e}")
            
            # Try extracting JSON from code block
            try:
                extracted = raw_message.split("```json")[-1].split("```")[0].strip()
                response_json = json.loads(extracted)
            except Exception as e2:
                logger.error(f"Error extracting JSON from code block: {e2}")
                response_json = {
                    "context": "",
                    "chatbot_response": raw_message
                }
        
        # Check for nested JSON in chatbot_response
        if "chatbot_response" in response_json:
            inner = response_json["chatbot_response"].strip()
            if inner.startswith("{"):
                try:
                    inner_json = json.loads(inner)
                    if "context" in inner_json and "chatbot_response" in inner_json:
                        response_json = inner_json
                except Exception as e:
                    logger.warning(f"Could not parse inner chatbot_response as JSON: {e}")
        
        return response_json