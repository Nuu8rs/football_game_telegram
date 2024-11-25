import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from database.session import engine
from database.model_base import Base
from logging_config import logger
from config import BOT_TOKEN, ADMINS
from constants import START_DAY_BEST_LEAGUE, END_DAY_BEST_LEAGUE

async def init_bot_command():
    commands = [
        BotCommand(command="send_message", description="Отправить сообщение всем пользователям")]

    for admin_id in ADMINS:
        await bot.set_my_commands(commands,
                              scope=BotCommandScopeChat(chat_id=admin_id))


async def init_leagues():
    # await core_league.setup_league()
    current_data = datetime.now() 
    if current_data.day >= START_DAY_BEST_LEAGUE and current_data.day <= END_DAY_BEST_LEAGUE:
        await best_club_league.start_best_league()
        

async def start_functional():
    await init_bot_command()
    await init_db()
    await init_leagues()
    
    await reset_energy_characters.start_reset_energy()

    await reset_aplied_energy_club.start_reset_energy()
    # await education_reward_reminder.start_reminder()
    await gym_reminder.start_iniatialization_gym()
    asyncio.create_task(core_duel._waiting_users())
    await end_duel_season.wait_to_end_season_duel()


async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.startup.register(start_functional)


             


from league.core_leauge import CORE_LEAGUE, LeagueService
from schedulers.scheduler_energy import EnergyResetScheduler, EnergyApliedClubResetScheduler
from schedulers.scheduler_education import EducationRewardReminderScheduler
from schedulers.scheduler_gym_rasks import GymStartReseter
from schedulers.scheduler_season_duels import SchedulerSesonDuels
from pvp_duels.duel_core import CoreDuel
from best_club_league.start_league import BestClubLeague

reset_energy_characters   = EnergyResetScheduler()
reset_aplied_energy_club  = EnergyApliedClubResetScheduler()
education_reward_reminder = EducationRewardReminderScheduler()
gym_reminder              = GymStartReseter()
end_duel_season           = SchedulerSesonDuels()
best_club_league          = BestClubLeague()

league_service = LeagueService()

core_duel    = CoreDuel()
core_league  = CORE_LEAGUE(league_service)
