from collections import deque
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, PND_GROUPS, NEWS_GROUPS
from prompts import get_pd_alert_prompt
from llm_utils import get_llm_sentiment_verdict
from utils import send_pd_alert
import asyncio

pnd_unsent_messages = deque(maxlen=20)
news_unsent_messages = deque(maxlen=20)

client = TelegramClient('sentiment_analysis_session', API_ID, API_HASH)

def make_event_handler(queue: deque):
    async def handler(event):
        print("Received message:", event.message.text)
        chat = await event.get_chat()
        message_data = {
            "group_id": chat.id,
            "group_name": chat.title,
            "message_id": event.message.id,
            "sender": event.message.sender_id,
            "text": event.message.text,
            "timestamp": event.message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        llm_message = await get_llm_sentiment_verdict(get_pd_alert_prompt(message_data["text"]))
        await send_pd_alert(llm_message.content)
        queue.append(message_data)
        print(f"Queue size is now: {len(queue)}")
    return handler

async def monitor_groups():
    await client.start(phone=PHONE_NUMBER)
    links = PND_GROUPS + NEWS_GROUPS
    for link in links:
        try:
            group = await client.get_entity(link)
            print(f"Monitoring group: {group.title}")
            if link in PND_GROUPS:
                client.add_event_handler(make_event_handler(pnd_unsent_messages), events.NewMessage(chats=[group]))
            else:
                client.add_event_handler(make_event_handler(news_unsent_messages), events.NewMessage(chats=[group]))
        except Exception as e:
            print(f"Failed to monitor {link}: {e}")
    print("Listening for new messages...")
    await asyncio.Event().wait()
