class PromptHandler:
    @staticmethod
    def generate_prompt(user_question, retrieved_docs, is_first_message=True):
        """Generate a prompt for the LLM"""
        docs_text = "\n---\n".join([doc.page_content for doc in retrieved_docs])
        
        if is_first_message:
            context_instruction = (
                "This is the first message from the user. Please infer the context solely from the provided documents."
            )
        else:
            context_instruction = (
                "Please use the conversation context provided below to refine your answer."
            )
        
        prompt = f"""
You are a knowledgeable assistant specialized in cryptocurrencies, blockchain, and crypto scams.
{context_instruction}

Relevant Documents:
{docs_text}

User Question:
{user_question}

Return your answer in the following JSON format:
{{
  "context": "context",
  "chatbot_response": "chatbot response to the user message"
}}
"""
        return prompt.strip()