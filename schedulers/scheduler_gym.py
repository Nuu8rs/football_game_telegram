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

from loader import bot

class GymTaskScheduler:
    
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        
        
        
    async def gym_spread_character(character: Character,
                             time_job_gym: timedelta,
                             type_characteristics: str
                            ):
        chance = check_chance(chance_add_point[time_job_gym])
        if chance:
            await CharacterService.update_character_field(
                character_obj=character,
                param=type_characteristics,
                add_point=1
            )
            await bot.send_message(
                chat_id=character.characters_user_id,
                text="<b>Вітаю</b> параметр персонажа {type_characteristics} - було покращено на 1 очко!".format(
                    type_characteristics = const_name_characteristics[type_characteristics]
                )
            )
        else:
            await bot.send_message(
                chat_id=character.characters_user_id,
                text="<b>На жаль</b>, ваш персонаж не зміг прокачати параметр {type_characteristics}, спробуйте ще раз!".format(
                    type_characteristics = const_name_characteristics[type_characteristics]
                )
            )            
        await CharacterService.toggle_character_training_status(character_obj=character)
        
    
    async def add_job_gym(self, character: Character, time_job_gym: timedelta, type_characteristics: str):
        self.scheduler.add_job(
            self.gym_spread_character, 
            trigger='date', 
            run_date=datetime.now() + time_job_gym,
            args=[character, time_job_gym, type_characteristics]
        )

        self.scheduler.start()


    async def cheking_job_gym(self):
        all_character_in_gym = await CharacterService.get_characters_in_training()
        for character in all_character_in_gym:
            if character.time_character_training < datetime.now():
                await self.gym_spread_character(
                    character = character,
                    time_job_gym=timedelta(minutes = 60),
                    type_characteristics=character.training_characteristic
                )
        
            else:
                self.scheduler.add_job(
                    self.gym_spread_character, 
                    trigger='date', 
                    run_date=character.time_character_training,
                    args=[character, timedelta(minutes = 60), character.training_characteristic]
                )

        self.scheduler.start()
            