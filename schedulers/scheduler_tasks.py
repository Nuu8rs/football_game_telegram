from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError


from database.models.character import Character
from services.character_service import CharacterService
from datetime import datetime, timedelta

from constants import chance_add_point, const_name_characteristics
from logging_config import logger
from utils.randomaizer import check_chance
from datetime import datetime

class GymTaskScheduler:
        
    def __init__(self):

        self.scheduler = AsyncIOScheduler()
        

    async def point_spread_character(self, 
                                     type_characteristics: str, 
                                     character: Character, 
                                     time_job_gym: timedelta,
                                     bot: Bot,
                                     user_id: int):
        chance = check_chance(chance_add_point[time_job_gym])
        if chance:
            await CharacterService.update_character_field(
                character_obj=character,
                param=type_characteristics,
                add_point=1
            )
            await bot.send_message(
                chat_id=user_id,
                text="<b>Вітаю</b> параметр персонажа {type_characteristics} - було покращено на 1 очко!".format(
                    type_characteristics = const_name_characteristics[type_characteristics]
                )
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text="<b>На жаль</b>, ваш персонаж не зміг прокачати параметр {type_characteristics}, спробуйте ще раз!".format(
                    type_characteristics = const_name_characteristics[type_characteristics]
                )
            )            
        await CharacterService.toggle_character_training_status(
                            character_obj=character
                                                                )
        
    async def schedule_task(self, task_id: str, 
                      run_after: timedelta, 
                      type_characteristics: str, 
                      character: Character,
                      bot: Bot,
                      user_id: int):
        
        self.scheduler.add_job(
            self.point_spread_character, 
            trigger='date', 
            run_date=datetime.now() + run_after,
            id=task_id,
            args=[type_characteristics, character, run_after, bot, user_id]
        )
        logger.debug(f"START TASK {task_id}")
        self.scheduler.start()


    async def stating_schedule(self):
        all_character_in_gym = await CharacterService.get_characters_in_training()
        for character in all_character_in_gym:
            self.scheduler
            