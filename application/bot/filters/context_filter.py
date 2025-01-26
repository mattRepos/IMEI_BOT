from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Union

class ContextFilter(BaseFilter):

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    async def __call__(self, event: Union[Message, CallbackQuery], state: FSMContext) -> bool:
        return (await state.get_data()).get(self.key) == self.value
