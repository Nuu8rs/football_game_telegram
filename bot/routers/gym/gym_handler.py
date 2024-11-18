from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from datetime import datetime

from database.models.user_bot import UserBot
from database.models.character import Character

from services.character_service import CharacterService
from services.reminder_character_service import RemniderCharacterService

from bot.keyboards.gym_keyboard import select_type_gym, select_time_to_gym, no_energy_keyboard
from bot.callbacks.gym_calbacks import SelectGymType, SelectTimeGym

from constants import GYM_PHOTO, const_name_characteristics, const_energy_by_time
from schedulers.scheduler_gym_rasks import GymScheduler

gym_router = Router()

@gym_router.message(F.text == "🖲 Тренування")
async def go_to_gym(message: Message):
    await message.answer_photo(
        photo=GYM_PHOTO,
        caption="Виберіть що ви хочете прокачати",
        reply_markup=select_type_gym())
    
@gym_router.callback_query(SelectGymType.filter())
async def select_position_character(query: CallbackQuery, callback_data:SelectGymType):
    await query.message.edit_caption(
        caption="""
<b>30 хвилин</b>, шанс підвищення навички <b>35%</b>  
Вартість - <b>10</b> енергії 

<b>60</b> хвилин, шанс підвищення навички <b>45%</b>  
Вартість - <b>20</b> енергії

<b>90</b> хвилин, шанс підвищення навички <b>55%</b>  
Вартість - <b>40</b> енергії

<b>120</b> хвилин, шанс підвищення навички <b>75%</b> 
Вартість - <b>60</b> енергії""",
        reply_markup=select_time_to_gym(callback_data.gym_type)
    )
    
@gym_router.callback_query(F.data == "back_to_select_gym_type")
async def select_position_character(query: CallbackQuery):
    await query.message.edit_caption(
        caption="Виберіть що ви хочете прокачати",
        reply_markup=select_type_gym())

    
@gym_router.callback_query(SelectTimeGym.filter())
async def start_gym(query: CallbackQuery, callback_data:SelectTimeGym, user: UserBot, character: Character):
    if character.reminder.character_in_training:
        return await query.message.reply("<b>Ваш персонаж і так уже тренується</b>")
    
    if character.current_energy < const_energy_by_time[callback_data.gym_time]:
        try:
            return await query.message.answer(
                text = "У вас не вистачає енергії, ви можете купити енергію в Крамниці енергії",
                reply_markup = no_energy_keyboard()
            ) 
        except:
            return
    
    await query.message.edit_caption(caption="Починаю тренування характеристики - {type_gym}\n\n"\
                                     "До завершення тренування - {end_time} хв.\n"\
                                     "Тренування завершиться в {end_time_full}".format(
                                         type_gym = const_name_characteristics[callback_data.gym_type],
                                         end_time = int(callback_data.gym_time.total_seconds() / 60),
                                         end_time_full = (datetime.now() + callback_data.gym_time).strftime("%d-%m-%Y, %H:%M")
                                     )
                                     ,reply_markup=None)
  
    gym_scheduler = GymScheduler(
        character_id        = character.id,
        type_characteristic = callback_data.gym_type,
        time_training       = callback_data.gym_time 
    )
    gym_scheduler.start_training()
    await RemniderCharacterService.update_training_info(
        character_id=character.id,
        training_stats=callback_data.gym_type,
        time_start_training=datetime.now(),
        time_training_seconds=callback_data.gym_time.total_seconds()
    )
    await RemniderCharacterService.toggle_character_training_status(
        character_id=character.id,
        
    )
    
    await CharacterService.consume_energy(
        character_id=character.id,
        energy_consumed=const_energy_by_time[callback_data.gym_time]
    )
    

@gym_router.callback_query(F.data == "get_out_of_gym")
async def leave_from_gym(query: CallbackQuery, character: Character):
    await RemniderCharacterService.toggle_character_training_status(character_id=character.id)
    await RemniderCharacterService.update_training_info(character_id=character.id)
    await query.message.answer("Ви вийшли з тренування")
