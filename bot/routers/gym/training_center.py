from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models import Character, UserBot
from services.character_service import CharacterService

from bot.keyboards.gym_keyboard import menu_gym
from bot.callbacks.gym_calbacks import SelectGymType, SelectTimeGym

from constants import GYM_PHOTO, const_name_characteristics, const_energy_by_time
from schedulers.scheduler_tasks import GymTaskScheduler


training_center_router = Router()

@training_center_router.message(F.text == "🏫 Навчальний центр")
async def go_to_gym(message: Message):
    await message.answer("Ласкаво просимо до навчального центру\nТут ви зможете підняти свій рівень", reply_markup=menu_gym())