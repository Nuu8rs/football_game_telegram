import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from database.models.character import Character

from bot.filters.check_admin_filter import CheckUserIsAdmin
from bot.states.admin_comands_state import OptionsNewsletter
from bot.keyboards.admins_keyboard import select_option_newsletter

from services.admins_functional_service import AdminFunctionalService
from utils.admins_functional_utils import get_new_member_characters

from logging_config import logger

admin_info_new_member_router = Router()

@admin_info_new_member_router.message(Command("info_new_member"), CheckUserIsAdmin())
async def new_info_member_handler(message: Message):
    new_characters = await AdminFunctionalService.get_new_members_character(count_members=20)
    text_new_characters = await get_new_member_characters(characters=new_characters)
    await message.answer(text_new_characters)
    