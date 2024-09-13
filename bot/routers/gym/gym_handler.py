from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from database.models.user_bot import UserBot
from database.models.character import Character

from services.character_service import CharacterService

from bot.keyboards.gym_keyboard import select_type_gym, select_time_to_gym, menu_gym
from bot.callbacks.gym_calbacks import SelectGymType, SelectTimeGym

from constants import GYM_PHOTO, const_name_characteristics, const_energy_by_time
from schedulers.scheduler_tasks import GymTaskScheduler


gym_router = Router()

@gym_router.message(F.text == "🖲 Тренажерний зал")
async def go_to_gym(message: Message):
    await message.answer("Вітаємо тебе у тренажерному залі! Піти на тренування та покращити навички? Відновити енергію у масажному залі? Обирати тобі!", reply_markup=menu_gym())
    
@gym_router.message(F.text == "🧤 Піти на тренування")
async def go_to_gym(message: Message):
    await message.answer_photo(
        photo=GYM_PHOTO,
        caption="Виберіть що ви хочете прокачати",
        reply_markup=select_type_gym())
    
@gym_router.callback_query(SelectGymType.filter())
async def select_position_character(query: CallbackQuery, callback_data:SelectGymType):
    await query.message.edit_caption(
        caption="""
<b>30 хвилин</b>, шанс підвищення навички <b>25%</b>  
Вартість - <b>10</b> енергії 

<b>60</b> хвилин, шанс підвищення навички <b>35%</b>  
Вартість - <b>20</b> енергії

<b>90</b> хвилин, шанс підвищення навички <b>50%</b>  
Вартість - <b>40</b> енергії

<b>120</b> хвилин, шанс підвищення навички <b>65%</b> 
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
    if character.character_in_training:
        return await query.message.reply("<b>Ваш персонаж і так уже тренується</b>")
    
    if character.current_energy <= const_energy_by_time[callback_data.gym_time]:
        try:
            return await query.message.edit_caption(
                caption="<b>У персонажа не вистачає енергії щоб піти на тренування, вибери інший час, aбо віднови енергію у массажному салону</b>",
                reply_markup=query.message.reply_markup
            )
        except:
            pass
    
    await query.message.edit_caption(caption="Починаю тренування характеристики - {type_gym}\n\n"\
                                     "До завершення тренування - {end_time} хв.\n"\
                                     "Тренування завершиться в {end_time_full}".format(
                                         type_gym = const_name_characteristics[callback_data.gym_type],
                                         end_time = int(callback_data.gym_time.total_seconds() / 60),
                                         end_time_full = (datetime.now() + callback_data.gym_time).strftime("%d-%m-%Y, %H:%M")
                                     )
                                     ,reply_markup=None)
    scheduler = GymTaskScheduler()
    await scheduler.schedule_task(
        task_id=f"{user.user_id}_gym_{callback_data.gym_type}_time_{callback_data.gym_time}",
        run_after=callback_data.gym_time,
        type_characteristics=callback_data.gym_type,
        characters_user_id = character.characters_user_id,
        bot=query.bot,
        user_id=user.user_id
    )
    await CharacterService.toggle_character_training_status(
        character_obj=character
    )
    
    await CharacterService.consume_energy(
        character_obj=character,
        energy_consumed=const_energy_by_time[callback_data.gym_time]
    )