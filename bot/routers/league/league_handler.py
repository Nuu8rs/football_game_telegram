from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.league_keyboard import menu_league_zone, keyboard_to_join_character_to_fight
from database.models.character import Character

from services.league_service import LeagueFightService
from services.club_service import ClubService

from constants import LEAGUE_PHOTO, JOIN_TO_FIGHT

from utils.league_utils import get_text_league, get_text_calendar_matches, get_text_result, get_text_rating


league_router = Router()



@league_router.message(F.text == "🏟 Стадіон")
async def get_my_character(message: Message, character: Character):
    
    if not character.club_id:
        return await message.answer(f"Ви не перебуваєте в команді, тому ви не можете користуватися [{message.text}]")
    
    club = await ClubService.get_club(club_id=character.club_id)
    await message.answer_photo(
        photo=LEAGUE_PHOTO,
        caption=await get_text_league(club),
        reply_markup=menu_league_zone()
    )    


@league_router.message(F.text == "📝 Зареєструватися в матч")
async def register_character_to_match(message: Message, character: Character):
    if not character.club_id:
        return await message.answer(f"Ви не перебуваєте в команді, тому ви не можете користуватися [{message.text}]")
        
    club = await ClubService.get_club(club_id=character.club_id)
    next_match = await LeagueFightService.get_next_league_fight_by_club(
        club_id=character.club_id
    )
    if next_match is None:
        return await message.answer(
            text="❌ Сезон ще на розпочався, очікуйте на початок подій. 1 числа кожного місяця а кубок стартує 23"
        )


    await message.answer_photo(
        photo=JOIN_TO_FIGHT,
        caption=await get_text_league(club),
        reply_markup=keyboard_to_join_character_to_fight(
            match_id=next_match.match_id
        )
    )
    
@league_router.message(F.text == "📅 Календар ігор")
async def get_calendar_matches(message: Message, character: Character):
    if not character.club_id:
        return await message.answer(f"Ви не перебуваєте в команді, тому ви не можете користуватися [{message.text}]")
    
    next_match = await LeagueFightService.get_next_league_fight_by_club(
        club_id=character.club_id
    )
    if next_match is None:
        return await message.answer(
            text="❌ Сезон ще на розпочався, очікуйте на початок подій. 1 числа кожного місяця а кубок стартує 24"
        )

    all_matches = await LeagueFightService.get_the_monthly_matches_by_club(club_id=character.club_id)
    await message.answer(
        text=get_text_calendar_matches(matches=all_matches, club_id=character.club_id)
    )
    
@league_router.message(F.text == "📊 Результати")
async def get_result_matches(message: Message, character: Character):
    if not character.club_id:
        return await message.answer(f"Ви не перебуваєте в команді, тому ви не можете користуватися [{message.text}]")
    
    next_match = await LeagueFightService.get_next_league_fight_by_club(
        club_id=character.club_id
    )
    if next_match is None:
        return await message.answer(
            text="❌ Сезон ще на розпочався, очікуйте на початок подій. 1 числа кожного місяця а кубок стартує 24"
        )

    
    all_matches = await LeagueFightService.get_the_monthly_matches_by_club(club_id=character.club_id)
    await message.answer(
        text=get_text_result(fights=all_matches, club_id=character.club_id)
    )
    
@league_router.message(F.text == "📋 Таблиця")
async def get_table_rait(message: Message, character: Character):
    if not character.club_id:
        return await message.answer(f"Ви не перебуваєте в команді, тому ви не можете користуватися [{message.text}]")

    next_match = await LeagueFightService.get_next_league_fight_by_club(
        club_id=character.club_id
    )
    if next_match is None:
        return await message.answer(
            text="❌ Сезон ще на розпочався, очікуйте на початок подій. 1 числа кожного місяця а кубок стартує 24"
        )

    
    group_id_mathces = await LeagueFightService.get_group_id_by_club(club_id=character.club_id)
    all_mathes_by_group = await LeagueFightService.get_the_monthly_matches_by_group(group_id=group_id_mathces)
    await message.answer(
        text=await get_text_rating(all_mathes_by_group)
    )