from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram_client import pnd_unsent_messages, news_unsent_messages
from prompts import get_telegram_messages_prompt, get_news_prompt
from llm_utils import get_llm_sentiment_verdict
import asyncio
import json

app = FastAPI(description="Crypto Sentiment Analysis API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pd")
def get_messages():
    messages_to_send = list(pnd_unsent_messages)
    analysis = asyncio.run(get_llm_sentiment_verdict(get_telegram_messages_prompt(messages_to_send)))
    content = analysis.content

    try:
        content_json = content.split("```json")[-1].split("```")[0].strip()
        analysis_result = json.loads(content_json)
        fixed_analysis = {
            "is_pump_and_dump": bool(analysis_result.get("is_pump_and_dump", False)),
            "cryptocurrencies": analysis_result.get("cryptocurrencies", []),
            "summary": analysis_result.get("summary", "")
        }
        if not isinstance(fixed_analysis["cryptocurrencies"], list):
            fixed_analysis["cryptocurrencies"] = []
        else:
            fixed_analysis["cryptocurrencies"] = [str(crypto) for crypto in fixed_analysis["cryptocurrencies"]]

    except (ValueError, IndexError, json.JSONDecodeError) as e:
        print(f"Failed to parse JSON: {e}")
        fixed_analysis = {
            "is_pump_and_dump": False,
            "cryptocurrencies": [],
            "summary": "Failed to parse LLM response correctly."
        }

    return {
        "messages": messages_to_send,
        "count": len(messages_to_send),
        "analysis": fixed_analysis
    }

@app.get("/news")
def get_news():
    messages_to_send = list(news_unsent_messages)
    analysis = asyncio.run(get_llm_sentiment_verdict(get_news_prompt(messages_to_send)))
    content = analysis.content

    try:
        content_json = content.split("```json")[-1].split("```")[0].strip()
        analysis_result = json.loads(content_json)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        analysis_result = {}

    return {
        "news": messages_to_send,
        "count": len(messages_to_send),
        "analysis": analysis_result
    }
