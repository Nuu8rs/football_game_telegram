import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models.character import Character

from services.character_service import CharacterService
from services.club_service import ClubService

from constants import TIME_RESET_ENERGY_CHARACTER, TIME_RESET_ENERGY_CLUB
from logging_config import logger
from loader import bot


class EnergyResetScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def __send_message_bot(self, characters: list[Character]):
        for character in characters:
            try:
                await asyncio.sleep(0.15)
                await bot.send_message(
                    chat_id=character.characters_user_id,
                    text="<b>Ваша енергія ⚡️ повністю відновлена 🔋</b>"
                )
            except Exception as E:
                logger.error(f"Не смог отправить сообщение {character.name}")


    async def reset_energy_character(self):
        all_characters = await CharacterService.get_character_how_update_energy()
        await CharacterService.update_energy_for_non_bots()
        asyncio.create_task(self.__send_message_bot(all_characters))
        
        logger.info("Обновил енергию для пользователей")
        
        
    async def start_reset_energy(self):
        self.scheduler.add_job(self.reset_energy_character, 
                               TIME_RESET_ENERGY_CHARACTER,
                               misfire_grace_time = 10
)
        self.scheduler.start()

        
        
class EnergyApliedClubResetScheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        
    async def reset_energy_aplied(self):
        await ClubService.reset_energy_aplied_not_bot_clubs()
        logger.info("Убрал усиление с команд")

    async def start_reset_energy(self):
        self.scheduler.add_job(self.reset_energy_aplied, 
                               TIME_RESET_ENERGY_CLUB,
                                misfire_grace_time = 10
)
        self.scheduler.start()
