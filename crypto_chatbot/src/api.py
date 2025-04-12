from fastapi import FastAPI, HTTPException
from models import ChatRequest
from vector_store import VectorStoreManager
from llm_client import LLMClient
from prompt_handler import PromptHandler
from response_parser import ResponseParser
from config import logger

# Initialize components
vector_store_manager = VectorStoreManager()
llm_client = LLMClient()
prompt_handler = PromptHandler()
response_parser = ResponseParser()

app = FastAPI(
    title="Crypto Chatbot RAG", 
    description="A chatbot powered by a RAG pipeline using Mistral and FAISS."
)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """Endpoint for chatbot interactions"""
    if not request.user_question:
        raise HTTPException(status_code=400, detail="User question is required.")
    
    # Process the chat request
    result = process_chat_request(request.user_question, request.context)
    return result

def process_chat_request(user_question, context):
    """Process a chat request through the RAG pipeline"""
    # Get relevant documents
    retrieved_docs = vector_store_manager.get_relevant_documents(user_question)
    
    # Check if this is the first message
    is_first_message = (context.strip() == "" or "first message" in context.lower())
    
    # Generate prompt
    prompt = prompt_handler.generate_prompt(user_question, retrieved_docs, is_first_message)
    
    # Get response from LLM
    raw_response = llm_client.generate_response(prompt)
    
    # Parse response
    parsed_response = response_parser.parse_response(raw_response)
    
    return parsed_response