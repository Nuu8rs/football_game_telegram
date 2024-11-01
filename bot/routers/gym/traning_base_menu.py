from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.models.character import Character
from bot.keyboards.training_base import menu_training_base


training_base_router = Router()

@training_base_router.message(F.text == "🗄 Тренувальна база")
async def training_facilities_handler(message: Message, character: Character, state: FSMContext):
    await message.answer("Вітаю на тренувальній базі!", 
                         reply_markup = menu_training_base())