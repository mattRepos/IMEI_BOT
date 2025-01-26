from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from typing import Any, Callable, Awaitable, Union

class CallbackAnswerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery], Awaitable[Any]], event: CallbackQuery, data: dict[str, Any]) -> Any:
        result = await handler(event, data)
        if isinstance(event, CallbackQuery):
            await event.answer()
        return result

