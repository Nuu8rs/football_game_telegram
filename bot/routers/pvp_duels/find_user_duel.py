from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character

from services.character_service import CharacterService



find_user_duel_router = Router()

@find_user_duel_router.message(F.text == "👨‍❤️‍💋‍👨 Дуелі")
async def find_user_duel_handler(message: Message, character: Character):
    ...