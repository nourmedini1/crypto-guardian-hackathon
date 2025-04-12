from mistralai import Mistral
from config import MISTRAL_API_KEY, MODEL

llm = Mistral(api_key=MISTRAL_API_KEY)

async def get_llm_sentiment_verdict(prompt):
    chat_response = llm.chat.complete(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return chat_response.choices[0].message
