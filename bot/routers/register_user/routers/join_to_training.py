import asyncio
import random

from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery


from database.models.user_bot import UserBot, STATUS_USER_REGISTER
from database.models.character import Character
from database.events.event_new_member_exp import EXP_CONSTANT

from bot.routers.register_user.config import (
    PHOTO_STAGE_REGISTER_USER,
    TEXT_STAGE_REGISTER_USER
)
from bot.routers.register_user.keyboard.join_first_training import join_first_training
from bot.routers.register_user.keyboard.get_new_member_bonus import new_member_bonus_keyboard
from bot.keyboards.menu_keyboard import main_menu

from constants import (
    const_name_characteristics,
    TOTAL_POINTS_ADD_NEW_MEMBER,
    PHOTO_NEW_BONUS_MEMBER_HAR
)

from schedulers.scheduler_gym_rasks import GymScheduler
from services.user_service import UserService
from services.reminder_character_service import RemniderCharacterService
from services.club_infrastructure_service import ClubInfrastructureService


first_training_router = Router()

TEMPLATE_STARTER_POWER_POINTS = f"""
🎉 <b>Вітаємо в грі, новачку!</b> 

За свій перший крок ти отримуєш <u>{TOTAL_POINTS_ADD_NEW_MEMBER} очок Сили</u> — твій стартовий бонус! 🚀

Що далі?
⚡ Використовуй Силу на тренування і матчі
🏆 Розвивайся і ставай сильнішим щодня

<b>І пам'ятай:</b> коли збереш <u>{EXP_CONSTANT} Енергії</u>, на тебе чекатиме спеціальний <b>Бокс з нагородами</b>! 🎁

<b>Твоя пригода тільки починається. Вперед до перемог!</b> 🔥
"""

async def join_to_training(
    message: Message,
    character: Character
) -> None:
    await asyncio.sleep(6)
    new_status = STATUS_USER_REGISTER.FIRST_TRAINING
    
    await UserService.edit_status_register(
        user_id=character.characters_user_id,
        status=new_status
    )
    await message.answer_photo(
        caption = TEXT_STAGE_REGISTER_USER[new_status],
        photo   = PHOTO_STAGE_REGISTER_USER[new_status],
        reply_markup = join_first_training()
    )


@first_training_router.callback_query(
    F.data == "join_first_training"
)
async def first_training_handler(
    query: CallbackQuery,
    character: Character,
    user: UserBot
):
    await query.message.delete()

    gym_type = random.choice(list(const_name_characteristics.keys()))
    gym_time = timedelta(minutes=5)
     
    club_infrastructure = None
    
    if character.club_id:
        club_infrastructure = await ClubInfrastructureService.get_infrastructure(character.club_id)
    
    gym_scheduler = GymScheduler(
        character        = character,
        type_characteristic = gym_type,
        time_training       = gym_time,
        club_infrastructure = club_infrastructure
    )
    gym_scheduler.start_training()
    await RemniderCharacterService.update_training_info(
        character_id          = character.id,
        training_stats        = gym_type,
        time_start_training   = datetime.now(),
        time_training_seconds = gym_time.total_seconds()
    )
    await RemniderCharacterService.toggle_character_training_status(
        character_id=character.id,   
    )
    
    new_status = STATUS_USER_REGISTER.END_TRAINING    
    await UserService.edit_status_register(
        user_id=character.characters_user_id,
        status=new_status
    )
    await query.message.answer_photo(
        photo=PHOTO_NEW_BONUS_MEMBER_HAR,
        caption = TEMPLATE_STARTER_POWER_POINTS,
        reply_markup = new_member_bonus_keyboard()
    )
    await asyncio.sleep(6)
    await query.message.answer(
        text = TEXT_STAGE_REGISTER_USER[new_status],
        reply_markup = main_menu(user)
    )
