from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.config import config
from infrastructure.api_client.theneo import TheneoClient
from aiogram.fsm.context import FSMContext
from ..filters.context_filter import ContextFilter
from loguru import logger


start_router = Router()


@start_router.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить IMEI", callback_data="check_imei")]
    ])
    await message.answer("Тут вы можете проверить IMEI вашего устройства", reply_markup=keyboard)

@start_router.callback_query(F.data == "start")
async def start_handler(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить IMEI", callback_data="check_imei")]
    ])
    await callback.message.edit_text("Тут вы можете проверить IMEI вашего устройства", reply_markup=keyboard)

@start_router.callback_query(F.data == "check_imei")
async def check_imei_handler(callback: CallbackQuery):
    theneo = TheneoClient(config.theneo_api_key)
    await callback.message.edit_text("Подождите, идет загрузка сервисов...")
    services = await theneo.get_services()
    buttons = [[InlineKeyboardButton(text="Вернуться в начало", callback_data="start")]]
    for service in services:
        logger.info(f"Service {service.id} {service.title}")
        buttons.append([InlineKeyboardButton(text=service.title, callback_data=f"check_imei_{service.id}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Выберите сервис для проверки IMEI", reply_markup=keyboard)

@start_router.callback_query(F.data.startswith("check_imei_"))
async def check_imei_handler(callback: CallbackQuery, state: FSMContext):
    service_id = callback.data.split("_")[-1]
    logger.info(f"Selected service {service_id}")
    await state.set_data({"service_id": service_id, "state": "get_imei"})
    await callback.message.edit_text(f"Вы выбрали сервис {service_id}, введите IMEI устройства")

@start_router.message(ContextFilter("state", "get_imei"))
async def get_imei_handler(message: Message, state: FSMContext):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в начало", callback_data="start")]
    ])
    
    imei = message.text.replace(" ", "")
    service_id = (await state.get_data()).get("service_id")
    theneo = TheneoClient(config.theneo_api_key)
    logger.info(f"Checking IMEI {imei} for service {service_id}")
    result = await theneo.check_imei(imei, int(service_id))
    
    device_name = result.properties.device_name
    model_description = result.properties.model_description
    embedded_info = result.properties.embedded_info
    if result.status == "successful":
        response = f"<b>Название устройства:</b> {device_name}\n"
        response += f"<b>Описание модели:</b> {model_description}\n\n"
        response += "<b>Дополнительная информация:</b>\n"
        
        for key, value in embedded_info.items():
            if isinstance(value, bool):
                value = "Да" if value else "Нет"
            response += f"<em><b>{key}:</b></em> {value}\n"
    else:
        response = f"<b>Статус:</b> {result.status}\n"
    
    await message.answer(response, parse_mode="HTML", reply_markup=keyboard)

