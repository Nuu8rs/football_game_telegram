from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from services.club_service import ClubService
from services.league_service import LeagueFightService

from database.models.club import Club
from database.models.league_fight import LeagueFight

from utils.randomaizer import check_chance
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
from copy import deepcopy
from .create_bots import BOTS
from .club_fight import ClubFight
from .user_sender import UserSender
from logging_config import logger
import uuid, random

LIMIT_CLUB = 20



class LeagueService:
    async def setup_leagues(self) -> List[List['Club']]:
        clubs_by_league = await ClubService.get_clubs_by_league()
        all_groups = await self.divide_clubs(clubs_by_league)
        return all_groups

    async def divide_clubs(self, clubs_by_league: Dict[str, List['Club']]) -> List[List['Club']]:
        all_groups = []
        for league, clubs in clubs_by_league.items():
            sublists = [clubs[i:i + LIMIT_CLUB] for i in range(0, len(clubs), LIMIT_CLUB)]
            for sublist in sublists:
                if len(sublist) < LIMIT_CLUB:
                    bots_menu = BOTS(
                        average_club_strength=(sum([club.total_power for club in sublist])+ random.randint(1,50)),
                        name_league=league
                    )
                    bots_clubs = await bots_menu.create_bot_clubs(LIMIT_CLUB - len(sublist))
                    sublist.extend(bots_clubs)
                all_groups.append(sublist)
        return all_groups

    @staticmethod
    def generate_round_robin_schedule(clubs: List['Club']) -> List[List[Tuple['Club', 'Club']]]:
        num_clubs = len(clubs)
        if num_clubs % 2 != 0:
            clubs.append(None)

        num_days = num_clubs - 1
        half_size = num_clubs // 2

        schedule = []

        for day in range(num_days):
            daily_matches = []
            for i in range(half_size):
                club1 = clubs[i]
                club2 = clubs[num_clubs - i - 1]
                if club1 is not None and club2 is not None:
                    daily_matches.append((club1, club2))
            schedule.append(daily_matches)
            clubs = [clubs[0]] + [clubs[-1]] + clubs[1:-1]

        return schedule

class CORE_LEAGUE:
    def __init__(self, league_service: LeagueService):
        self.league_service = league_service
        self.scheduler_league = AsyncIOScheduler()

    async def setup_league(self) -> None:
        matches = await LeagueFightService.get_league_fights_current_month()
        if not matches:
            groups = await self.league_service.setup_leagues()
            await self.generate_and_schedule_new_fights(groups)
        else:
            await self.starting_matches(matches)
        self.scheduler_league.start()

    async def generate_and_schedule_new_fights(self, groups: List[List['Club']]) -> None:
        start_date = datetime(2024, 9, 7) 
        for group in groups:
            group_id = random.randint(1,100000)
            matches = self.league_service.generate_round_robin_schedule(group) 
            await self.create_and_save_fights(group_id, matches, start_date)

        matches = await LeagueFightService.get_league_fights_current_month()
        await self.starting_matches(matches)

    async def create_and_save_fights(self, group_id: int, matches: List[List[Tuple['Club', 'Club']]], start_date: datetime) -> None:
        num_days = len(matches) 
        match_dates = [start_date + timedelta(days=i) for i in range(num_days)]
        for day, match_date in enumerate(match_dates):
            current_day_matches = matches[day]
            for j, (first_club, second_club) in enumerate(current_day_matches):
                start_time_fight = datetime.combine(match_date, datetime.min.time()).replace(hour=21, minute=0, second=(j % 60), microsecond=0)

                await LeagueFightService.create_league_fight(
                    match_id=str(uuid.uuid4()),
                    first_club_id=first_club.id,
                    second_club_id=second_club.id,
                    time_to_start=start_time_fight,
                    group_id = group_id
                )

    async def starting_matches(self, matches: List['LeagueFight']) -> None:
        for i, match in enumerate(matches):
            # if match.first_club_id == 228 or match.second_club_id == 228:
                self.schedule_match_start(i, match)
                # break
    def schedule_match_start(self, index: int, match: 'LeagueFight') -> None:
        
        match_date = match.time_to_start
        start_time_fight = datetime.combine(match_date, datetime.min.time()).replace(hour=21, minute=0, second=index % 60, microsecond=0)
        start_time_sender = datetime.combine(match_date, datetime.min.time()).replace(hour=20, minute=15, second=index % 60, microsecond=0)
        
        # current_time = datetime.now()
        # start_time_sender = current_time + timedelta(seconds=1)
        # start_time_fight = current_time + timedelta(seconds=10)

        fight = ClubFight(match.first_club, match.second_club, start_time_fight, match.match_id)
        user_sender = UserSender(match.first_club, match.second_club, match_id=fight.match_id)

        self.scheduler_league.add_job(user_sender.send_messages_to_users, trigger=DateTrigger(start_time_sender))
        self.scheduler_league.add_job(fight.start, trigger=DateTrigger(start_time_fight))

