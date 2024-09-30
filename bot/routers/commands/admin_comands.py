import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.filters.check_admin_filter import CheckUserIsAdmin
from bot.states.admin_comands_state import SendAllUserMessage

from services.character_service import CharacterService

from loader import logger

admin_comands_router = Router()


@admin_comands_router.message(Command("send_message"), CheckUserIsAdmin())
async def send_message_all_user(message: Message, state: FSMContext):
    await message.answer("Напишіть що завгодно, це повідомлення буде надіслано всім")
    await state.set_state(SendAllUserMessage.get_text_from_send)
    
    
@admin_comands_router.message(SendAllUserMessage.get_text_from_send, CheckUserIsAdmin())
async def send_message(message: Message, state: FSMContext):
    all_users_character = await CharacterService.get_all_users_not_bot()
    await state.clear()
    for user_character in all_users_character:
        try:
            await asyncio.sleep(1)
            await message.send_copy(
                chat_id=user_character.characters_user_id
            )
        except Exception as E:
            logger.error(f"НЕ СМОГ ОТПРАВИТЬ ПРИ ТОТАЛЬНОЙ РАССЫЛКЕ - {user_character.name}")
    
    await message.answer("Розсилання цього повідомлення було закінчено")
    
