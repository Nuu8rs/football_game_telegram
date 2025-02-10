from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

from services.league_service import LeagueFightService
from database.models.league_fight import LeagueFight

from league.process_match.club_fight import ClubMatch
from league.user_sender import UserSender
from league.create_league.create_league_match import CreateDefaultLeagueMatches
from constants import START_DAY_DEFAULT_LEAGUE

class StartDefaultLeague:
    
    def __init__(self):
        self.scheduler_league = AsyncIOScheduler()

    
    async def setup_matches(self) -> None:
        matches = await LeagueFightService.get_league_fights_current_month()
        if not matches:
            await CreateDefaultLeagueMatches().create_default_league_matches()
            matches = await LeagueFightService.get_league_fights_current_month()
        await self._start_match(matches)
        
        self.scheduler_league.start()
            
    async def _start_match(
        self, 
        matches: list[LeagueFight]
    ) -> None:
    
        for match in matches:
            await self.schedule_match_start(match)
            
            
    async def schedule_match_start(self, match: LeagueFight):
        match_date = match.time_to_start
        
        start_time_fight = datetime.combine(match_date, datetime.min.time()).replace(hour=21)
        start_time_sender = datetime.combine(match_date, datetime.min.time()).replace(hour=20, minute=15)
        
        
        if start_time_fight < datetime.now():
            return
        
        club_match = ClubMatch(
            first_club_id  = match.first_club.id  ,
            second_club_id = match.second_club.id ,
            start_time     = start_time_fight,
            match_id       = match.match_id,
            group_id       = match.group_id
        )
        
        user_sender = UserSender(match_id=club_match.clubs_in_match.match_id)

        self.scheduler_league.add_job(user_sender.send_messages_to_users, 
                                      trigger=DateTrigger(start_time_sender),
                                      misfire_grace_time = 10,
                                      
                                      )
        self.scheduler_league.add_job(club_match.start_match, 
                                      trigger=DateTrigger(start_time_fight),
                                      misfire_grace_time = 10
                                      )
        
class SchedulerDefaultLeague:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start_scheduler(self):
        self.scheduler.add_job(
            func=StartDefaultLeague().setup_matches,
            trigger=CronTrigger(day=START_DAY_DEFAULT_LEAGUE, hour=8, minute=0),
            misfire_grace_time=10
        )
        self.scheduler.start()