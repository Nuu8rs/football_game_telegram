from aiogram import Router,  Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from database.models.user_bot import UserBot
from database.models.character import Character

from constants import get_photo_character, GYM_PHOTO
from utils.character_utils import get_character_text

menu_character_router = Router()

@menu_character_router.message(F.text == "⚽️ Мій персонаж")
async def get_my_character(message: Message, state: FSMContext, user: UserBot, character: Character):
    await state.clear()
    await message.answer_photo(
        photo=get_photo_character(character),
        caption=get_character_text(character)
    )

