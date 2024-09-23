from aiogram import Router, F
from aiogram.types import  CallbackQuery

from datetime import datetime

from database.models.character import Character

from services.character_service import CharacterService
from services.match_character_service import MatchCharacterService

from bot.callbacks.league_callbacks import  JoinToFight, ViewCharacterRegisteredInMatch

from league.club_in_match import ClubsInMatch
from league.club_fight import ClubMatch, ClubMatchManager


join_to_fight_router = Router()



@join_to_fight_router.callback_query(JoinToFight.filter())
async def join_to_match(query: CallbackQuery, callback_data: JoinToFight, character: Character):
    if character.reminder.character_in_training:
        return await query.answer(
            text = "Ваш персонаж на тренуванні, ви не можете взяти участь у матчі"
        )
    
    
    fight_instance = ClubMatchManager.get_fight_by_id(
        match_id=callback_data.match_id
    )
    
    current_time = datetime.now()
    if current_time > fight_instance.start_time:
        await query.answer(
            text="❌ Даний матч уже закінчився"
        )
        return await query.message.delete()
    
    if not character.club_id:
        return await query.message.answer("❌ У данного персонажа нету клуба")
    
    

    character_in_match = await MatchCharacterService.get_character_in_match(
        character=character,
        club_in_match=fight_instance.clubs_in_match
    )
    if character_in_match is None:
        
        
        
        await MatchCharacterService.add_character_in_match(
            club_in_match = fight_instance.clubs_in_match,
            character=character
        )
        await query.message.answer(text = "✅ <b>Ваш персонаж був доданий на матч</b>")
        await query.message.edit_reply_markup(reply_markup=None)
    
    else:
        await query.answer("❌ Ваш персонаж уже й так бере участь у цьому матчі")
        

@join_to_fight_router.callback_query(ViewCharacterRegisteredInMatch.filter())
async def join_to_match(query: CallbackQuery, callback_data: ViewCharacterRegisteredInMatch, character: Character):
    character_club_in_match = await MatchCharacterService.get_charaters_club_in_match(
        match_id=callback_data.match_id,
        club_id=character.club_id
    )
    
    if not character_club_in_match:
        return await query.message.answer("На даний матч <b>ніхто з клубу ще не зареєструвався</b>")
    
    total_power = 0
    text = "🏆 <b>На матч зареєструвались</b>:\n\n"
    for match_character in character_club_in_match:
        character = await CharacterService.get_character_by_id(match_character.character_id)
        text += f"👤 {character.name} <b>[{character.full_power:.2f}]</b>\n"
        total_power += character.full_power
        
    text += f"\n💪 <b>Загальна сила команди</b> {total_power:.2f}"
    
    await query.message.answer(text)