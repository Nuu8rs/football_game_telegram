import asyncio
import random

from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery


from database.models.user_bot import UserBot, STATUS_USER_REGISTER
from database.models.character import Character

from bot.routers.register_user.config import (
    PHOTO_STAGE_REGISTER_USER,
    TEXT_STAGE_REGISTER_USER
)
from bot.routers.register_user.keyboard.join_first_training import join_first_training
from bot.keyboards.menu_keyboard import main_menu

from constants import const_name_characteristics

from schedulers.scheduler_gym_rasks import GymScheduler
from services.user_service import UserService
from services.reminder_character_service import RemniderCharacterService
from services.club_infrastructure_service import ClubInfrastructureService

first_training_router = Router()

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
    gym_type = random.choice(list(const_name_characteristics.keys()))
    gym_time = timedelta(minutes=5) 
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
    await asyncio.sleep(6)
    await query.message.answer(
        text = TEXT_STAGE_REGISTER_USER[new_status],
        reply_markup = main_menu(user)
    )
