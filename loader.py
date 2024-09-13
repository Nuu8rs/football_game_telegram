from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.session import engine
from database.model_base import Base

from config import BOT_TOKEN
from logging_config import logger

async def start_functional():
    await init_db()
    await reset_energy_characters.start_reset_energy()
    await reset_aplied_energy_club.start_reset_energy()
    await education_reward_reminder.start_reminder()
    await core_league.setup_league()


async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.startup.register(start_functional)



from league.core_leauge import CORE_LEAGUE, LeagueService
from schedulers.scheduler_energy import EnergyResetScheduler, EnergyApliedClubResetScheduler
from schedulers.scheduler_education import EducationRewardReminderScheduler

reset_energy_characters = EnergyResetScheduler()
reset_aplied_energy_club = EnergyApliedClubResetScheduler()
education_reward_reminder = EducationRewardReminderScheduler()

league_service = LeagueService()
core_league  = CORE_LEAGUE(league_service)
