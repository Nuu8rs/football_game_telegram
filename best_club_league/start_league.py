from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from datetime import datetime

from best_club_league.service.get_best_league_match import BestClubLeagueMatchService

from database.models.league_fight import LeagueFight

from league.user_sender import UserSender
from league.club_fight import ClubMatch

class BestClubLeague:
    
    def __init__(self) -> None:
        self.scheduler_best_league =  AsyncIOScheduler()
        self.best_league_service = BestClubLeagueMatchService()
    async def start_best_league(self):
        await self._start_league()
        
    async def _start_league(self):
        league_matchs = await self.best_league_service.get_matches()

        for match in league_matchs:
            await self.start_match(match)

        self.scheduler_best_league.start()

    async def start_match(self, match: LeagueFight) -> None:
        if match.time_to_start < datetime.now():
            return
        
        match_club = ClubMatch(
            first_club_id  = match.first_club.id  ,
            second_club_id = match.second_club.id ,
            start_time     = match.time_to_start,
            match_id       = match.match_id,
            group_id       = match.group_id
        )
    
        time_send_join_match_text = match.time_to_start.replace(
            minute = 20,
            hour = 20
        )
        time_start_match = match.time_to_start.replace(
            hour = 21,
            minute = 0
            
        )
        
        user_sender = UserSender(
            match_id = match.match_id
        )
        self.scheduler_best_league.add_job(
            func = user_sender.send_messages_to_users,
            trigger = DateTrigger(time_send_join_match_text),
            misfire_grace_time = 10
        )
        
        self.scheduler_best_league.add_job(
            func    = match_club.start_match,
            trigger = DateTrigger(time_start_match),
            misfire_grace_time = 10
        )