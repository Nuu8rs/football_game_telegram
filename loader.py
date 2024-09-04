from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.session import engine
from database.models import Base

from config import BOT_TOKEN
from logging_config import logger

async def start_functional():
    await init_db()
    await reset_energy_characters.reset_energy_character()
    await core_league.setup_league()


async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.startup.register(start_functional)



from league.core_leauge import CORE_LEAGUE, LeagueService
from schedulers.scheduler_energy import EnergyResetScheduler
reset_energy_characters = EnergyResetScheduler()
league_service = LeagueService()
core_league  = CORE_LEAGUE(league_service)
