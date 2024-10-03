from aiogram import Bot

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.character_service import CharacterService
from services.club_service import ClubService

from constants import TIME_RESET_ENERGY_CHARACTER, TIME_RESET_ENERGY_CLUB
from logging_config import logger
from datetime import timedelta
import random

class EnergyResetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()


    async def reset_energy_character(self):
        await CharacterService.update_energy_for_non_bots() 
        logger.info("Обновил енергию для пользователей")
        
        
    async def start_reset_energy(self):
        self.scheduler.add_job(self.reset_energy_character, TIME_RESET_ENERGY_CHARACTER)
        self.scheduler.start()

        
        
class EnergyApliedClubResetScheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        
    async def reset_energy_aplied(self):
        await ClubService.reset_energy_aplied_not_bot_clubs()
        logger.info("Убрал усиление с клубов")

    async def start_reset_energy(self):
        self.scheduler.add_job(self.reset_energy_aplied, TIME_RESET_ENERGY_CLUB)
        self.scheduler.start()
