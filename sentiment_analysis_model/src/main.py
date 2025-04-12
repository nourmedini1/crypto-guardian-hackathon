import asyncio
from uvicorn import Config, Server
from telegram_client import monitor_groups
from api import app

async def main():
    monitor_task = asyncio.create_task(monitor_groups())
    config = Config(app, host="0.0.0.0", port=5030, reload=False, loop="asyncio")
    server = Server(config)
    server_task = asyncio.create_task(server.serve())
    await asyncio.gather(monitor_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())
