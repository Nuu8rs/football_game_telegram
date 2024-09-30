from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError


from database.models.character import Character
from services.character_service import CharacterService
from services.reminder_character_service import RemiderCharacterService
from datetime import datetime, timedelta

from constants import chance_add_point, const_name_characteristics
from logging_config import logger
from utils.randomaizer import check_chance
from datetime import datetime

from loader import bot

class GymTaskScheduler:
    
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        
        
        
    async def gym_spread_character(self, character: Character,
                             time_job_gym: timedelta,
                             type_characteristics: str
                            ):
        chance = check_chance(chance_add_point[time_job_gym])
        character = await CharacterService.get_character_by_id(character_id=character.id)
        if character.reminder.training_stats is None:
            return
        
        
        if chance:
            await CharacterService.update_character_field(
                character_obj=character,
                param=type_characteristics,
                add_point=1
            )
            try:
                await bot.send_message(
                    chat_id=character.characters_user_id,
                    text="<b>Вітаю</b> параметр персонажа {type_characteristics} - було покращено на 1 очко!".format(
                        type_characteristics = const_name_characteristics[type_characteristics]
                    )
                )
            except Exception as E:
                logger.error(f"НЕ СМОГ ОТПРАВИТЬ СООБЩЕНИЕ {character.name}")
        else:
            try:
                await bot.send_message(
                    chat_id=character.characters_user_id,
                    text="<b>На жаль</b>, ваш персонаж не зміг прокачати параметр {type_characteristics}, спробуйте ще раз!".format(
                        type_characteristics = const_name_characteristics[type_characteristics]
                    )
                )
            except Exception as E:
                logger.error(f"НЕ СМОГ ОТПРАВИТЬ СООБЩЕНИЕ {character.name}")
                            
        await RemiderCharacterService.toggle_character_training_status(character_id=character.id)
        await RemiderCharacterService.update_training_info(character_id=character.id)
    
    async def add_job_gym(self, character: Character, time_job_gym: timedelta, type_characteristics: str):
        self.scheduler.add_job(
            self.gym_spread_character, 
            trigger='date', 
            run_date=datetime.now() + time_job_gym,
            args=[character, time_job_gym, type_characteristics]
        )

        self.scheduler.start()


    async def cheking_job_gym(self):
        all_character_in_gym = await RemiderCharacterService.get_characters_in_training()
        for character in all_character_in_gym:
            if character.reminder.end_time_training < datetime.now():
                await self.gym_spread_character(
                    character            = character,
                    time_job_gym         = character.reminder.time_training,
                    type_characteristics = character.reminder.training_stats
                )
            else:
                self.scheduler.add_job(
                    self.gym_spread_character, 
                    trigger='date', 
                    run_date=character.reminder.end_time_training,
                    args=[character, character.reminder.time_training, character.reminder.training_stats]
                )
                

        self.scheduler.start()
            