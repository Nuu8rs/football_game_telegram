from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from database.models.club import Club
from database.models.character import Character

from services.club_service import ClubService
from services.character_service import CharacterService

from bot.states.club_states import FindClub
from bot.keyboards.club_keyboard import find_club, join_to_club_keyboard
from bot.callbacks.club_callbacks import SelectClubToJoin, JoinToClub
from bot.callbacks.switcher import SwitchClub

from constants import TIME_TO_JOIN_TO_CLUB

from loader import logger

from constants import CLUB_PHOTO
from utils.club_utils import get_club_description, send_message_characters_club

research_club_router = Router()

@research_club_router.message(F.text == "🎪 Мій клуб")
async def research_club_handler(message: Message, character: Character):
    pass