from aiogram import Bot, Dispatcher
from core.config import config
from .handlers import all_routers
from application.bot.middlewares import all_middlewares

class BotManager:

    ROUTERS = all_routers

    MIDDLEWARES = all_middlewares

    def __init__(self):
        self.bot = Bot(token=config.bot_token)
        self.dp = Dispatcher()

    def setup_routers(self):
        for router in self.ROUTERS:
            self.dp.include_router(router)

    def setup_middlewares(self):
        for middleware in self.MIDDLEWARES:
            self.dp.callback_query.middleware.register(middleware)
            self.dp.message.middleware.register(middleware)

