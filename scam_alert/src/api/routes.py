import logging
from fastapi import APIRouter, Depends, Request

logger = logging.getLogger(__name__)

# Create router for alert endpoints
router = APIRouter(tags=["alerts"])

@router.post("/pd-alert")
async def send_pump_dump_alert(message: dict, request: Request):
    notification_service = request.app.state.notification_service
    llm_service = request.app.state.llm_service
    bot = request.app.state.telegram_bot
    
    llm_response = "Sorry, I'm currently unavailable. Please try again later."
    try: 
        alert = message.get("analysis")
        alert_summary = alert.get("summary")
        llm_response = await llm_service.get_response(alert_summary)
    except Exception as e:
        logger.error(f"Error parsing pump-and-dump alert message: {e}")
        return {"status": "Error parsing pump-and-dump alert message"}
    
    subscribers = notification_service.get_subscribers()
    if not subscribers:
        logger.info("Send-message API called but no subscribers found.")
        return {"status": "No users subscribed"}
    
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=llm_response)
            notification_service.update_last_message(chat_id, llm_response)
        except Exception as e:
            logger.error(f"Error sending message to chat_id {chat_id}: {e}")
    
    return {"status": "Pump and Dump alert sent to all subscribers"}

@router.post("/rg")
async def send_rug_pull_alert(message: dict, request: Request):
    notification_service = request.app.state.notification_service
    llm_service = request.app.state.llm_service
    bot = request.app.state.telegram_bot
    
    subscribers = notification_service.get_subscribers()
    if not subscribers:
        logger.info("Send-message API called but no subscribers found.")
        return {"status": "No users subscribed"}
    
    logger.info(f"Sending rug pull alert to {len(subscribers)} subscribers.")
    
    features = message.get("features", {})
    token_info = message.get("token", {})
    token_symbol = token_info.get("symbol", "Unknown") if isinstance(token_info, dict) else "Unknown"
    
    RUG_PULL_PROMPT = (
        "Write a short and concise blog post about a detected rug pull incident. "
        "The detection was based on the following indicators:\n"
        f"Token: {token_symbol}\n"
        f"Coin Age (Months): {features.get('coin_age_months', 'N/A')}\n"
        f"Trust in Owners Score: {features.get('trust_in_owners', 'N/A')}\n"
        # ... remaining indicators ...
        "Explain why this token was flagged as a rug pull and advise investors on precautions."
    )
    
    blog_msg = await llm_service.get_response(RUG_PULL_PROMPT)
    logger.info(f"Generated rug pull alert")
    
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=blog_msg)
            notification_service.update_last_message(chat_id, blog_msg)
            logger.info(f"Sent rug pull alert to chat_id: {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send rug pull alert to chat_id {chat_id}: {e}")
    
    return {"status": "Rug pull alert sent to all subscribers"}

@router.post("/pd")
async def send_pump_dump_alert(message: dict, request: Request):
    notification_service = request.app.state.notification_service
    llm_service = request.app.state.llm_service
    bot = request.app.state.telegram_bot
    
    subscribers = notification_service.get_subscribers()
    if not subscribers:
        logger.info("Send-message API called but no subscribers found.")
        return {"status": "No users subscribed"}
    
    logger.info(f"Sending pump-and-dump alert to {len(subscribers)} subscribers.")
    
    features = message.get("features", {})
    token_symbol = message.get("token", "Unknown")
    
    PUMP_DUMP_PROMPT = (
        "Write a short and concise blog post about a detected pump-and-dump scheme. "
        "The detection was based on the following indicators:\n"
        f"Token: {token_symbol}\n"
        # ... remaining indicators ...
        "Explain why this token was flagged as being involved in a pump-and-dump scheme."
    )
    
    blog_msg = await llm_service.get_response(PUMP_DUMP_PROMPT)
    logger.info(f"Generated pump-and-dump alert")
    
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=blog_msg)
            notification_service.update_last_message(chat_id, blog_msg)
            logger.info(f"Sent pump-and-dump alert to chat_id: {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send pump-and-dump alert to chat_id {chat_id}: {e}")
    
    return {"status": "Pump-and-dump alert sent to all subscribers"}