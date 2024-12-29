import time

from aiogram import Router, F
from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime

from database.models.character import Character

from services.character_service import CharacterService
from services.league_service import LeagueFightService

from bot.callbacks.league_callbacks import EpizodeDonateEnergyToMatch
from bot.states.league_match_state import DonateEnergyInMatch
from bot.keyboards.gym_keyboard import no_energy_keyboard

from league.club_fight import ClubMatch

from utils.league_utils import count_energy_characters_in_match
from utils.club_utils import send_message_characters_club


from league.club_fight import ClubMatch, ClubMatchManager
from constants import TIME_FIGHT, KOEF_ENERGY_DONATE

add_energy_in_match_router = Router()


@add_energy_in_match_router.message(F.text == "🔋 Задонатити в матч")
async def donate_energy_from_match(message: Message, character: Character, state: FSMContext):
    if character.club_id is None:
        return await message.answer("Ви не перебуваєте в команді")
    

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
    await message.answer(f"Напишіть скільки ви хочете поповнити енергії в поточний матч\n5 енергії + 1 сила до команди в матчі\n\nПоточна енергія у тебе - {character.current_energy} 🔋")
    

@add_energy_in_match_router.callback_query(EpizodeDonateEnergyToMatch.filter())
async def donate_energy_from_match_handler(
        query: CallbackQuery, 
        callback_data: EpizodeDonateEnergyToMatch, 
        character: Character,
        state: FSMContext
    ):
    if time.time() > callback_data.time_end_goal:
        await query.answer("Час для цього голу вже закінчився",
                                  show_alert= True)
        return await query.message.delete()
    
    
    if character.club_id is None:
        await query.answer("Ви не перебуваєте в команді", 
                                  show_alert = True)
        return await query.message.delete()
    
    
    current_match = ClubMatchManager.get_fight_by_id(callback_data.match_id)
    if not current_match:
        return
    
    await state.update_data(current_match = current_match)
    await state.set_state(DonateEnergyInMatch.send_epizode_donate_energy)
    await query.message.answer(f"Напишіть скільки ви хочете поповнити енергії в поточний матч\n1 енергія + 1 сила до команди в матчі\n\nПоточна енергія у тебе - {character.current_energy} 🔋")
    

@add_energy_in_match_router.message(
    DonateEnergyInMatch.send_epizode_donate_energy,
    (F.text.func(str.isdigit))
)
async def donate_epizode_energy(
    message: Message,
    character: Character,
    state: FSMContext
):
    energy = int(message.text)
    if energy < 1:
        await state.clear()
        return await message.answer("Мінімум 1 енергії")
    
    if character.current_energy < energy:
        await state.clear()
        return await message.answer(
            text = "У вас не вистачає енергії, ви можете купити енергію в Крамниці енергії",
            reply_markup = no_energy_keyboard()
        ) 
        
    
    data = await state.get_data()
    
    current_match: ClubMatch = data.get("current_match", False)
    if not current_match:
        return

    match = current_match.clubs_in_match
    if character.id in match.charactets_id_first_club:
        key = "epizode_energy_first_club"
        my_club = match.first_club
        
    elif character.id in match.charactets_id_second_club:
        key = "epizode_energy_second_club" 
        my_club = match.second_club
    else:
        return
    
    chance_first_club_before  = match.calculate_chances 
    chance_second_club_before = 100 - chance_first_club_before 
    
    setattr(match, key, getattr(match, key) + energy*5)
    
    chance_first_club_after  = match.calculate_chances 
    chance_second_club_after = 100 - chance_first_club_after
    
    text = f"""
⚽️ <b>{character.name} додав {energy}💪 сил команді {my_club.name_club}!</b> ⚽️  

🔥 <b>Зміни шансів на гол:</b>  
- ⚽️ Команда: {match.first_club.name_club} - <b>{chance_first_club_before:.2f}%</b> → <b>{chance_first_club_after:.2f}%</b>  
- ⚽️ Команда: {match.second_club.name_club} - <b>{chance_second_club_before:.2f}%</b> → <b>{chance_second_club_after:.2f}%</b>  

💪 Завдяки підтримці команда {my_club.name_club} отримала значний поштовх! 🚀 
    """
    await CharacterService.consume_energy(character_id=character.id, energy_consumed=energy)
    await send_message_characters_club(
        characters_club = match.all_characters_in_match,
        my_character = None,
        text = text
    )
    
    
    
@add_energy_in_match_router.message(DonateEnergyInMatch.send_count_donate_energy, (F.text.func(str.isdigit)))
async def select_coint_donate_energy_in_match(message: Message, character: Character, state: FSMContext):
    count_energy = int(message.text)
    if count_energy < KOEF_ENERGY_DONATE:
        return await message.answer(f"Мінімально можна підтримати на {KOEF_ENERGY_DONATE} енергії")
    
    if character.club_id is None:
        return await message.answer("Ви не перебуваєте в команді")
    
    if count_energy > character.current_energy:
        await state.clear()
        return await message.answer(
            text = "У вас не вистачає енергії, ви можете купити енергію в Крамниці енергії",
            reply_markup = no_energy_keyboard()
        ) 
    
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
    await CharacterService.consume_energy(character_id=character.id, energy_consumed=count_energy)
    
    await send_message_members_match_to_donate_energy(
        current_match = current_match,
        my_character=character,
        count_energy=count_energy
        )
    
    
    text = f"""❤️‍🔥 Ви підтримали свою команду, тим самим підвищивши її силу на <b>{(count_energy//KOEF_ENERGY_DONATE)}</b>

💪🏻 Поточна сила твоєї команди - {total_power:.2f}"""
    
    await message.answer(text)
    await state.clear()
    
    

async def send_message_members_match_to_donate_energy(current_match: ClubMatch, my_character: Character, count_energy: int):
    text = (f"👑Учасник <b>{my_character.name}</b> задонатив <b>{count_energy}</b> одиниць енергії🔋, "
        f"зміцнив свою команду <b>{my_character.club.name_club}</b>, "
        f"додавши <b>{count_energy/KOEF_ENERGY_DONATE}</b> до його сили💪")

    
    all_members_match = current_match.clubs_in_match.first_club.characters + current_match.clubs_in_match.second_club.characters
    await send_message_characters_club(
        characters_club=all_members_match,
        my_character=my_character,
        text=text
    )
    
    