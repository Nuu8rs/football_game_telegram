import asyncio
from datetime import datetime

from league.core_leauge import CORE_LEAGUE, LeagueService
from schedulers.scheduler_energy import EnergyResetScheduler, EnergyApliedClubResetScheduler
from schedulers.scheduler_education import EducationRewardReminderScheduler
from schedulers.scheduler_gym_rasks import GymStartReseter
from schedulers.scheduler_season_duels import SchedulerSesonDuels
from schedulers.scheduler_season_beast_league import SchedulerSesonBeastLeague
from schedulers.scheduler_buy_energy import ReminderBuyEnergy
from schedulers.scheduler_training import ReminderTraning
from schedulers.scheduler_vip_pass import VipPassSchedulerService

from pvp_duels.duel_core import CoreDuel
from best_club_league.start_league import BestClubLeague
from league_20_power_club.start_league import Best20ClubLeague

from schedulers.scheduler_league_rankings_update import UpdateLeagueRaiting

from constants import (
    START_DAY_BEST_LEAGUE, 
    END_DAY_BEST_LEAGUE,
    
    START_DAY_BEST_20_CLUB_LEAGUE,
    END_DAY_BEST_20_CLUB_LEAGUE
)
from database.events.event_listener import (
    energy_listener,
    exp_listener
)

async def init_leagues():
    await core_league.setup_league()
    current_data = datetime.now() 
    if current_data.day >= START_DAY_BEST_LEAGUE and current_data.day <= END_DAY_BEST_LEAGUE:
        await best_club_league.start_best_league()
    
    if current_data.day >= START_DAY_BEST_20_CLUB_LEAGUE and current_data.day <= END_DAY_BEST_20_CLUB_LEAGUE:
        await best_20_club_league.start_best_league()
        

async def start_utils():
    await init_leagues()
    await energy_listener.start_listener()
    await exp_listener.start_listener()
    
    await reset_energy_characters.start_reset_energy()
    await reset_aplied_energy_club.start_reset_energy()
    await education_reward_reminder.start_reminder()
    await gym_reminder.start_iniatialization_gym()
    await end_beast_league.wait_to_end_season_best_league()
    await end_duel_season.wait_to_end_season_duel()
    await league_ranking_update.start()
    await reminder_buy_energy.start()
    await reminder_go_to_training.start()
    await reminder_vip_pass.start_timers()
    asyncio.create_task(core_duel._waiting_users())




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
reminder_vip_pass         = VipPassSchedulerService()

league_service = LeagueService()

core_duel    = CoreDuel()
core_league  = CORE_LEAGUE(league_service)

league_ranking_update = UpdateLeagueRaiting()