import time
import random

from aiogram import Router, F
from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models.character import Character

from services.character_service import CharacterService

from bot.callbacks.league_callbacks import EpizodeDonateEnergyToMatch
from bot.states.league_match_state import DonateEnergyInMatch
from bot.keyboards.gym_keyboard import no_energy_keyboard

from utils.photo_utils import get_photo, save_photo_id
from match.core.manager import ClubMatchManager
from match.entities import MatchData
from match.constans import (
    MIN_DONATE_ENERGY_TO_BONUS_KOEF,
    KOEF_DONATE_ENERGY,
    DONE_ENERGY_PHOTOS
)

from utils.club_utils import send_message_characters_club


add_energy_in_match_router = Router()

TEXT_EPIZODE_DONATE_ENERGY = """
⚡️ <b>Команда</b>: <u>{name_club}</u> зібрала <b>{min_donate_bonus_energy} енергії</b> в цьому епізоді!  
💪 Завдяки зусиллям гравців, команда отримує <b>BOOST</b> +{koef_add_power_from_donat}% до <b>суми донату</b>!

🔋 <b>Енергія — це сила!</b> Чим більше її Ви вкладаєте в епізод тим більший шанс збити гол!

👟 <b>Граємо далі</b> та йдемо до перемоги!
"""


@add_energy_in_match_router.callback_query(EpizodeDonateEnergyToMatch.filter())
async def donate_energy_from_match_handler(
        query: CallbackQuery, 
        callback_data: EpizodeDonateEnergyToMatch, 
        character: Character,
        state: FSMContext
    ):

    if int(time.time()) > callback_data.time_end_goal:
        await query.answer("Час для цього голу вже закінчився",
                                  show_alert= True)
        return await query.message.delete()
    
    
    if character.club_id is None:
        await query.answer("Ви не перебуваєте в команді", 
                                  show_alert = True)
        return await query.message.delete()
    
    
    match_data = ClubMatchManager.get_match(callback_data.match_id)
    if not match_data:
        return
    
    await state.update_data(match_data = match_data)
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
    
    MIN_ENERGY_DONATE_MATCH = 10
    energy = int(message.text)
    if energy < MIN_ENERGY_DONATE_MATCH:
        await state.clear()
        return await message.answer(f"Мінімум {MIN_ENERGY_DONATE_MATCH} енергії")
    
    if character.current_energy < energy:
        await state.clear()
        return await message.answer(
            text = "У вас не вистачає енергії, ви можете купити енергію в Крамниці енергії",
            reply_markup = no_energy_keyboard()
        ) 
        
    
    data = await state.get_data()
    
    match_data: MatchData = data.get("match_data", False)
    if not match_data:
        return

    old_chance_club  = match_data.get_chance_clubs()
    old_first_club_chance = old_chance_club[0]*100
    old_second_club_chance = old_chance_club[1]*100
    
    if character.id in match_data.first_club.charactets_match_ids:
        match_data.first_club.epiіsode_donate_energy += energy
        my_club = match_data.first_club
        
    elif character.id in match_data.second_club.charactets_match_ids:
        match_data.second_club.epiіsode_donate_energy += energy
        my_club = match_data.second_club
    else:
        return
        
    if my_club.epiіsode_donate_energy >= MIN_DONATE_ENERGY_TO_BONUS_KOEF:
        if not my_club.text_is_send_epizode_donate_energy:
            random_patch = random.choice(DONE_ENERGY_PHOTOS)
            is_save, photo = await get_photo(random_patch)
            
            text_epizode_donate = TEXT_EPIZODE_DONATE_ENERGY.format(
                name_club = my_club.club_name,
                min_donate_bonus_energy = MIN_DONATE_ENERGY_TO_BONUS_KOEF,
                koef_add_power_from_donat = KOEF_DONATE_ENERGY*100
            )
            
            message_photo = await send_message_characters_club(
                characters_club = match_data.all_characters,
                my_character = None,
                text = text_epizode_donate,
                photo = photo,
            )
            my_club.text_is_send_epizode_donate_energy = True
            if message_photo and not is_save:
                await save_photo_id(
                    patch_to_photo = random_patch,
                    photo_id = message_photo.photo[0].file_id,
                )

                    
    after_chance_club = match_data.get_chance_clubs()
    chance_first_club_after = after_chance_club[0]*100
    chance_second_club_after = after_chance_club[1]*100
    
    text = f"""
⚽️ <b>{character.character_name} додав {energy}🔋 до сил команді {my_club.club_name}!</b> ⚽️  

🔥 <b>Зміни шансів на гол:</b>  
- ⚽️ Команда: {match_data.first_club.club_name} - <b>{old_first_club_chance:.2f}%</b> → <b>{chance_first_club_after:.2f}%</b>  
- ⚽️ Команда: {match_data.second_club.club_name} - <b>{old_second_club_chance:.2f}%</b> → <b>{chance_second_club_after:.2f}%</b>  

💪 Завдяки підтримці команда {my_club.club_name} отримала значний поштовх! 🚀 
    """
    await CharacterService.consume_energy(character_id=character.id, energy_consumed=energy)
    await send_message_characters_club(
        characters_club = match_data.all_characters,
        my_character = None,
        text = text
    )
    
    
    

# @add_energy_in_match_router.message(F.text == "🔋 Задонатити в матч")
# async def donate_energy_from_match(message: Message, character: Character, state: FSMContext):
#     if character.club_id is None:
#         return await message.answer("Ви не перебуваєте в команді")
    

#     current_match_db = await LeagueFightService.get_match_today(
#         club_id=character.club_id
#     )

#     if current_match_db is None:
#         return await message.answer("На даний момент немає матчів")
    
#     match_data = ClubMatchManager.get_match(current_match_db.match_id)
#     await state.update_data(match_data = match_data)
    
#     current_datetime = datetime.now()
#     if (current_datetime < match_data.start_time) or (current_datetime > match_data.start_time + TIME_FIGHT):
#         return await message.answer("Зараз не час поповнювати енергію, можна буде поповнити її протягом матчу")
    
#     await state.set_state(DonateEnergyInMatch.send_count_donate_energy)
#     await message.answer(f"Напишіть скільки ви хочете поповнити енергії в поточний матч\n5 енергії + 1 сила до команди в матчі\n\nПоточна енергія у тебе - {character.current_energy} 🔋")
    

    
    
# @add_energy_in_match_router.message(DonateEnergyInMatch.send_count_donate_energy, (F.text.func(str.isdigit)))
# async def select_coint_donate_energy_in_match(message: Message, character: Character, state: FSMContext):
#     count_energy = int(message.text)
#     if count_energy < KOEF_ENERGY_DONATE:
#         return await message.answer(f"Мінімально можна підтримати на {KOEF_ENERGY_DONATE} енергії")
    
#     if character.club_id is None:
#         return await message.answer("Ви не перебуваєте в команді")
    
#     if count_energy > character.current_energy:
#         await state.clear()
#         return await message.answer(
#             text = "У вас не вистачає енергії, ви можете купити енергію в Крамниці енергії",
#             reply_markup = no_energy_keyboard()
#         ) 
    
#     data = await state.get_data()
#     match_data: MatchData = data.get("match_data", False)
    
#     if character.club_id == current_match.club_id:
#         current_match.clubs_in_match.donate_energy_first_club += count_energy
#         current_donate_energy = current_match.clubs_in_match.donate_energy_first_club
        
#     elif character.club_id == current_match.clubs_in_match.second_club_id:
#         current_match.clubs_in_match.donate_energy_second_club += count_energy
#         current_donate_energy = current_match.clubs_in_match.donate_energy_second_club

#     total_power = await count_energy_characters_in_match(current_match.clubs_in_match.match_id, character.club_id) + current_donate_energy//KOEF_ENERGY_DONATE

#     character = await CharacterService.get_character(character_user_id=character.characters_user_id)
#     await CharacterService.consume_energy(character_id=character.id, energy_consumed=count_energy)
    
#     await send_message_members_match_to_donate_energy(
#         current_match = current_match,
#         my_character=character,
#         count_energy=count_energy
#         )
    
    
#     text = f"""❤️‍🔥 Ви підтримали свою команду, тим самим підвищивши її силу на <b>{(count_energy//KOEF_ENERGY_DONATE)}</b>

# 💪🏻 Поточна сила твоєї команди - {total_power:.2f}"""
    
#     await message.answer(text)
#     await state.clear()
    
    

# async def send_message_members_match_to_donate_energy(current_match: ClubMatch, my_character: Character, count_energy: int):
#     text = (f"👑Учасник <b>{my_character.character_name}</b> задонатив <b>{count_energy}</b> одиниць енергії🔋, "
#         f"зміцнив свою команду <b>{my_character.club.name_club}</b>, "
#         f"додавши <b>{count_energy/KOEF_ENERGY_DONATE}</b> до його сили💪")

    
#     all_members_match = current_match.clubs_in_match.first_club.characters + current_match.clubs_in_match.second_club.characters
#     await send_message_characters_club(
#         characters_club=all_members_match,
#         my_character=my_character,
#         text=text
#     )
    
    