from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import re

from database.models.user_bot import UserBot
from database.models.character import Character

from services.character_service import CharacterService
from services.user_service import UserService
from services.club_service import ClubService
from bot.callbacks.club_callbacks import ViewCharatcerClub

from bot.keyboards.club_keyboard import club_menu_keyboard, main_menu_club
from bot.states.club_states import ChangeClubChatLink


from utils.club_utils import get_club_text, rating_club, send_message_characters_club, get_text_schemas

from constants import CLUB_PHOTO


my_club_router = Router()

@my_club_router.message(F.text == "🎪 Клуби")
async def get_my_club_handler(message: Message, character: Character):
    await message.answer("Вітаю в меню клуба",reply_markup=main_menu_club(character))
    
@my_club_router.message(F.text == "🎪 Мій клуб")
async def my_club(message: Message, character: Character):
    if  not character.club_id:
        return await message.answer("На жаль, у вас немає клубу, ви можете створити свій клуб, або приєднатися до вже реалізованого клубу",
                                    reply_markup=main_menu_club(character))
        
    
    club = await ClubService.get_club(club_id=character.club_id)
    await message.answer_photo(
        photo=CLUB_PHOTO,
        caption= await get_club_text(club=club,
                              character=character),
        reply_markup=club_menu_keyboard(
            club=club,
            character=character
        )
    )    
    
    
@my_club_router.callback_query(F.data == "change_club_chat")
async def change_chat_link_clube(query: CallbackQuery, state: FSMContext, user: UserBot, character: Character):
    if character.club_id is None:
        return await query.answer("Ви зараз не в клубі")
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
    
@my_club_router.callback_query(ViewCharatcerClub.filter())
async def change_chat_link_clube(query: CallbackQuery, character: Character, callback_data: ViewCharatcerClub):
    club = await ClubService.get_club(club_id=callback_data.club_id)
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
    await send_message_characters_club(
        characters_club=club.characters,
        my_character=character,
        text=f"☹️ Персонаж <b>{character.name}</b> покинул ваш клуб"
    )

@my_club_router.callback_query(F.data == "view_schema_club")
async def view_schema_club(query: CallbackQuery, user: UserBot, character: Character):
    if not character.club_id:
        return await query.answer("❌ Ви й так не в клубі")
    
    await query.message.answer(
        text=get_text_schemas(character.club)
    )