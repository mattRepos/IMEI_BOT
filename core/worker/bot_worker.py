from application.bot.manager import BotManager
import asyncio
from loguru import logger
import traceback

async def bot_start():
    logger.info("Bot starting...")
    manager = BotManager()
    manager.setup_routers()
    manager.setup_middlewares()
    while True:
        try:
            await manager.dp.start_polling(manager.bot)
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            logger.error(traceback.format_exc())
            await asyncio.sleep(10)

