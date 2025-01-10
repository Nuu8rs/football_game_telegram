import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from datetime import datetime
from database.session import engine
from database.model_base import Base
from config import (
    BOT_TOKEN, 
    ADMINS, 
    CALLBACK_URL_WEBHOOK_ENERGY, 
    CALLBACK_URL_WEBHOOK_BOX,
    CALLBACK_URL_WEBHOOK_CHANGE_POSITION,
    CALLBACK_URL_WEBHOOK_MONEY,
    CALLBACK_URL_WEBHOOK_VIP_PASS
)

from constants import (
    START_DAY_BEST_LEAGUE, 
    END_DAY_BEST_LEAGUE,
    
    START_DAY_BEST_20_CLUB_LEAGUE,
    END_DAY_BEST_20_CLUB_LEAGUE
)


from webhook_api.handlers.energy_handler import MonoResultEnergy
from webhook_api.handlers.box_handler import MonoResultBox
from webhook_api.handlers.change_position_handler import MonoResultChangePosition
from webhook_api.handlers.money_handler import MonoResultMoney
from webhook_api.handlers.vip_pass_handler import MonoResultVipPass

async def init_bot_command():
    commands = [
        BotCommand(command="send_message", description="Отправить сообщение всем пользователям")]

    for admin_id in ADMINS:
        await bot.set_my_commands(commands,
                              scope=BotCommandScopeChat(chat_id=admin_id))


async def init_leagues():
    await core_league.setup_league()
    current_data = datetime.now() 
    if current_data.day >= START_DAY_BEST_LEAGUE and current_data.day <= END_DAY_BEST_LEAGUE:
        await best_club_league.start_best_league()
    
    if current_data.day >= START_DAY_BEST_20_CLUB_LEAGUE and current_data.day <= END_DAY_BEST_20_CLUB_LEAGUE:
        await best_20_club_league.start_best_league()
        

async def start_functional():
    await init_bot_command()
    await init_db()
    await init_leagues()
    
    await reset_energy_characters.start_reset_energy()
    await reset_aplied_energy_club.start_reset_energy()
    await education_reward_reminder.start_reminder()
    await gym_reminder.start_iniatialization_gym()
    await end_beast_league.wait_to_end_season_best_league()
    await end_duel_season.wait_to_end_season_duel()
    await league_ranking_update.start()
    await reminder_buy_energy.start()
    await reminder_go_to_training.start()
    asyncio.create_task(core_duel._waiting_users())


async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.startup.register(start_functional)

app = web.Application()
app.router.add_post("/" + CALLBACK_URL_WEBHOOK_ENERGY.split("/")[-1], MonoResultEnergy.router)
app.router.add_post("/" + CALLBACK_URL_WEBHOOK_BOX.split("/")[-1], MonoResultBox.router)
app.router.add_post("/" + CALLBACK_URL_WEBHOOK_CHANGE_POSITION.split("/")[-1], MonoResultChangePosition.router)
app.router.add_post("/" + CALLBACK_URL_WEBHOOK_MONEY.split("/")[-1], MonoResultMoney.router)
app.router.add_post("/" + CALLBACK_URL_WEBHOOK_VIP_PASS.split("/")[-1], MonoResultVipPass.router)



from league.core_leauge import CORE_LEAGUE, LeagueService
from schedulers.scheduler_energy import EnergyResetScheduler, EnergyApliedClubResetScheduler
from schedulers.scheduler_education import EducationRewardReminderScheduler
from schedulers.scheduler_gym_rasks import GymStartReseter
from schedulers.scheduler_season_duels import SchedulerSesonDuels
from schedulers.scheduler_season_beast_league import SchedulerSesonBeastLeague
from schedulers.scheduler_buy_energy import ReminderBuyEnergy
from schedulers.scheduler_training import ReminderTraning

from pvp_duels.duel_core import CoreDuel
from best_club_league.start_league import BestClubLeague
from league_20_power_club.start_league import Best20ClubLeague

from schedulers.scheduler_league_rankings_update import UpdateLeagueRaiting

reset_energy_characters   = EnergyResetScheduler()
reset_aplied_energy_club  = EnergyApliedClubResetScheduler()
education_reward_reminder = EducationRewardReminderScheduler()
gym_reminder              = GymStartReseter()
end_duel_season           = SchedulerSesonDuels()
end_beast_league          = SchedulerSesonBeastLeague()
best_club_league          = BestClubLeague()
best_20_club_league       = Best20ClubLeague()
reminder_buy_energy       = ReminderBuyEnergy()
reminder_go_to_training   = ReminderTraning()

league_service = LeagueService()

core_duel    = CoreDuel()
core_league  = CORE_LEAGUE(league_service)

league_ranking_update = UpdateLeagueRaiting()