from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models import Character
from services.character_service import CharacterService
from datetime import datetime, timedelta

from constants import chance_add_point, const_name_characteristics, TIME_RESET_ENERGY
from logging_config import logger
from utils.randomaizer import check_chance


class EnergyResetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()


    async def reset_energy_character(self):
        await CharacterService.update_energy_for_non_bots() 
        
    async def start_reset_energy(self):
        self.scheduler.add_job(self.reset_energy_character, TIME_RESET_ENERGY)
        self.scheduler.start()

        
        
