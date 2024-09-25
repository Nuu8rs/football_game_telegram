from aiogram import Router, F
from aiogram.types import  Message
from aiogram.fsm.context import FSMContext

from datetime import datetime

from database.models.character import Character

from services.character_service import CharacterService
from services.league_service import LeagueFightService

from bot.states.league_match_state import DonateEnergyInMatch
from utils.league_utils import count_energy_characters_in_match

from league.club_fight import ClubMatch, ClubMatchManager
from constants import TIME_FIGHT, KOEF_ENERGY_DONATE

add_energy_in_match_router = Router()


@add_energy_in_match_router.message(F.text == "🔋 Задонатити в матч")
async def donate_energy_from_match(message: Message, character: Character, state: FSMContext):
    if character.club_id is None:
        return await message.answer("Ви не перебуваєте в клубі")
    

    current_match_db = await LeagueFightService.get_match_today(
        club_id=character.club_id
    )

    if current_match_db is None:
        return await message.answer("На даний момент немає матчів")
    
    current_match = ClubMatchManager.get_fight_by_id(current_match_db.match_id)
    await state.update_data(current_match = current_match)
    
    current_datetime = datetime.now()
    if (current_datetime < current_match.start_time) or (current_datetime > current_match.start_time + TIME_FIGHT):
        return await message.answer("Зараз не час поповнювати енергію, можна буде поповнити її протягом матчу")
    
    await state.set_state(DonateEnergyInMatch.send_count_donate_energy)
    await message.answer("Напишіть скільки ви хочете поповнити енергії в поточний матч")
    
    
    
@add_energy_in_match_router.message(DonateEnergyInMatch.send_count_donate_energy, (F.text.func(str.isdigit)))
async def select_coint_donate_energy_in_match(message: Message, character: Character, state: FSMContext):
    count_energy = int(message.text)
    if count_energy < KOEF_ENERGY_DONATE:
        return await message.answer("Мінімально можна підтримати на 5 енергії")
    
    if character.club_id is None:
        return await message.answer("Ви не перебуваєте в клубі")
    
    if count_energy > character.current_energy:
        await state.clear()
        return await message.answer("У вас немає стільки енергії")
    
    data = await state.get_data()
    current_match: ClubMatch = data['current_match']
    
    if character.club_id == current_match.clubs_in_match.first_club_id:
        current_match.clubs_in_match.donate_energy_first_club += count_energy
        current_donate_energy = current_match.clubs_in_match.donate_energy_first_club
        
    elif character.club_id == current_match.clubs_in_match.second_club_id:
        current_match.clubs_in_match.donate_energy_second_club += count_energy
        current_donate_energy = current_match.clubs_in_match.donate_energy_second_club

    total_power = await count_energy_characters_in_match(current_match.clubs_in_match.match_id, character.club_id) + current_donate_energy//KOEF_ENERGY_DONATE

    character = await CharacterService.get_character(character_user_id=character.characters_user_id)
    await CharacterService.consume_energy(character_obj=character, energy_consumed=count_energy)
    await state.clear()
    
    text = f"""❤️‍🔥 Ви підтримали свою команду, тим самим підвищивши її силу на <b>{(count_energy//KOEF_ENERGY_DONATE)}</b>

💪🏻 Поточна сила твоєї команди - {total_power:.2f}"""
    
    await message.answer(text)