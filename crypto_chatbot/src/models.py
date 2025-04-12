from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_question: str
    context: str = "This is the first message from the user. Please infer the context solely from the provided documents."

class ChatResponse(BaseModel):
    context: str
    chatbot_response: str