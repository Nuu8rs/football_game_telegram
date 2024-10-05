from aiogram import Router, F
from aiogram.types import Message

from database.models.character import Character

from services.character_service import CharacterService
from services.club_service import ClubService
from services.league_service import LeagueFightService
from services.match_character_service import MatchCharacterService

from bot.keyboards.hall_fame_keyboard import menu_hall_fame

from utils.hall_fame_utils import (get_top_characters_by_power,
                                   get_top_characters_by_level,
                                   get_top_club_by_power,
                                   get_top_bomber_raiting
                                   )
from constants import HALL_FAME_PHOTO

hall_fame_router = Router()


@hall_fame_router.message(F.text == "🏆 Зал слави")
async def menu_hall_of_fame(message: Message):
    await message.answer_photo(
        photo=HALL_FAME_PHOTO,
        caption="Ви прийшли в зал слави",
        reply_markup=menu_hall_fame()
    )
    
@hall_fame_router.message(F.text == "💪Рейтинг за силою гравця")
async def menu_hall_of_fame(message: Message, character: Character):
    all_characters = await CharacterService.get_all_users_not_bot()
    await message.answer(
        text=get_top_characters_by_power(
            all_characters=all_characters,
            my_character=character
        )
    )
    

@hall_fame_router.message(F.text == "📊 Рейтинг за рівнем гравця")
async def menu_hall_of_fame(message: Message, character: Character):
    all_characters = await CharacterService.get_all_users_not_bot()
    await message.answer(
        text=get_top_characters_by_level(
            all_characters=all_characters,
            my_character=character
        )
    )
    
    

@hall_fame_router.message(F.text == "🏆 Рейтинг команд за силою")
async def menu_hall_of_fame(message: Message, character: Character):
    my_club = await ClubService.get_club(club_id=character.club_id)
    all_clubs = await ClubService.get_all_clubs()

    await message.answer(
        text=get_top_club_by_power(
            all_clubs=all_clubs,
            my_club=my_club
        )
    )
    
@hall_fame_router.message(F.text == "🏃🏼 Рейтинг бомбардирів")
async def menu_hall_of_fame(message: Message, character: Character):
    group_id_mathces = await LeagueFightService.get_group_id_by_club(club_id=character.club_id)
    all_matches_charaters = await MatchCharacterService.get_characters_by_group_id(group_id_mathces)
    await message.answer(
        text=await get_top_bomber_raiting(
            all_matches=all_matches_charaters,
            my_character=character
        )
    )
