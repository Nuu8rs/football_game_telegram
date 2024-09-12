from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import re

from database.models.user_bot import UserBot
from database.models.character import Character

from services.character_service import CharacterService
from services.user_service import UserService
from services.club_service import ClubService
from bot.callbacks.club_callbacks import LeaveThisClub

from bot.keyboards.club_keyboard import create_or_join_club, club_menu_keyboard, menu_club
from bot.states.club_states import ChangeClubChatLink

from constants import CLUB_PHOTO
from utils.club_utils import get_club_text, rating_club


my_club_router = Router()

@my_club_router.message(F.text == "🎪 Мій клуб")
async def get_my_club_handler(message: Message, user: UserBot, character: Character):
    if  not character.club_id:
        return await message.answer("На жаль, у вас немає клубу, ви можете створити свій клуб, або приєднатися до вже реалізованого клубу",
                                    reply_markup=create_or_join_club())
        
        
    await message.answer("Вітаю у клубі",reply_markup=menu_club())
    
    club = await ClubService.get_club(club_id=character.club_id)
    await message.answer_photo(
        photo=CLUB_PHOTO,
        caption= await get_club_text(club=club,
                              character=character),
        reply_markup=club_menu_keyboard(
            club=club,
            user=user
        )
    )
    
@my_club_router.callback_query(F.data == "change_club_chat")
async def change_chat_link_clube(query: CallbackQuery, state: FSMContext, user: UserBot, character: Character):
    await query.message.answer("Надішліть посилання на чат клубу")
    await state.set_state(state=ChangeClubChatLink.send_chat_link)
    
    
@my_club_router.message(ChangeClubChatLink.send_chat_link)
async def edit_chat_link_club(message: Message, state: FSMContext, character: Character):
    def is_telegram_chat_link(link: str) -> bool:
        pattern = re.compile(
            r'^(https:\/\/t\.me\/(?:\+[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)|t\.me\/(?:\+[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)|tg:\/\/join\?invite=[a-zA-Z0-9_]+)$',
            re.IGNORECASE
        )
        
        return bool(pattern.match(link))
    if not is_telegram_chat_link(message.text):
        return await message.answer("Надішліть коректне посилання на чат")
    
    link = message.text
    club = await ClubService.get_club(club_id=character.club_id)
    await ClubService.update_link_to_chat(club=club, new_link=link)
    await message.answer(f"Ссылка на чат клуба была поменянна на - <a href={link}>Чат</a>")
    await state.clear()
    
@my_club_router.callback_query(F.data == "view_all_members_club")
async def change_chat_link_clube(query: CallbackQuery, state: FSMContext, user: UserBot, character: Character):
    club = await ClubService.get_club(club_id=character.club_id)
    rating_club_text = rating_club(
        club=club,
        character=character
    )
    await query.message.reply(text=rating_club_text)
    
    
@my_club_router.callback_query(F.data == "leave_club")
async def leave_club_handler(query: CallbackQuery, user: UserBot, character: Character):
    if not character.club_id:
        return await query.answer("❌ Ви й так не в клубі")
    
    club = await ClubService.get_club(club_id=character.club_id)
    await CharacterService.leave_club(character)
    await query.message.edit_reply_markup(reply_markup=None)
    await query.message.reply(f"<b>Ви вийшли з клубу</b> - {club.name_club}")