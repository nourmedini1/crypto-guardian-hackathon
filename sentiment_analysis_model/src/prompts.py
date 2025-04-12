def get_pd_alert_prompt(message):
    return f"""
You are a sentiment analysis model and chatbot for cryptocurrency topics.
Your task is to analyze the following Telegram message discussing potential pump and dump schemes.
For the message, write a short concise engaging blog about it:
\n\n
{message}
\n\n
"""

def get_telegram_messages_prompt(messages):
    return f"""
You are a sentiment analysis model and chatbot for cryptocurrency topics.
Your task is to analyze the following Telegram messages discussing potential pump and dump schemes.
For each message, determine:
1. Whether the message is discussing a pump or dump scheme (return a boolean).
2. The cryptocurrencies being discussed.
3. A summary paragraph of what the messages are about.

Messages:
{messages}

Return the result in the following JSON format:
{{
    "is_pump_and_dump": boolean,
    "cryptocurrencies": [list of cryptocurrencies],
    "summary": "summary paragraph"
}}
"""

def get_news_prompt(news):
    return f"""
You are a sentiment analysis model and chatbot specialized in cryptocurrency news.
Analyze the following news headlines and classify them into:
1. Political sentiment about crypto,
2. Technical analysis of the market,
3. News about new coins or projects.

Return a JSON object with the following format:
{{
    "political_sentiment": {{
        "summary_paragraph": "summary paragraph",
        "news_related_to": [list of headlines]
    }},
    "technical_analysis": {{
        "summary_paragraph": "summary paragraph",
        "news_related_to": [list of headlines]
    }},
    "new_coins": {{
        "summary_paragraph": "summary paragraph",
        "news_related_to": [list of headlines]
    }}
}}

News:
{news}
"""
