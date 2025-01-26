from aiogram import BaseMiddleware
from core.config import config
from aiogram.types import Message, CallbackQuery
from typing import Any, Dict, Callable, Union, Awaitable
from loguru import logger

class WhiteListMiddleware(BaseMiddleware):

    def __init__(self):
        self.allowed_users = config.allowed_users

    async def __call__(self, handler: Union[Callable[[Message], Awaitable[Any]], Callable[[CallbackQuery], Awaitable[Any]]], event: Union[Message, CallbackQuery], data: dict[str, Any]) -> Any:
        if event.from_user.username not in self.allowed_users:
            await event.answer("You are not allowed to use this bot")
            return

        return await handler(event, data)

