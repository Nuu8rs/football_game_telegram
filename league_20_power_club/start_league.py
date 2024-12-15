from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from datetime import datetime

from league_20_power_club.service.get_best_club_match import BestClubLeagueMatchService
from league_20_power_club.service.generate_last_match import GenerateLastMatchService
from league_20_power_club.utils.sender_info import SendEndMatch, SendCongratulationEndMatch

from database.models.league_fight import LeagueFight

from services.league_service import LeagueFightService

from league.user_sender import UserSender
from league.club_fight import ClubMatch

from constants import END_MATCH_TOP_20_CLUB, SEND_GONGRATULATION_END_BEST_MATCH

class Best20ClubLeague:
    
    def __init__(self) -> None:
        self.scheduler_best_league =  AsyncIOScheduler()
        self.best_league_service = BestClubLeagueMatchService()
        self.last_match_service = GenerateLastMatchService()
        
    async def start_best_league(self):
        await self._start_league()
        
        self.scheduler_best_league.add_job(
            func = self._start_end_match,
            trigger = END_MATCH_TOP_20_CLUB
        )
        
        await self._start_end_match()
        self.scheduler_best_league.start()

        
    async def _start_end_match(self):
        end_match: LeagueFight = await self.last_match_service.get_last_match()
        end_match: LeagueFight = await LeagueFightService.get_league_fight(
            match_id = end_match.match_id
        )
        sender_end_match = SendEndMatch(
            clubs = self.last_match_service.all_clubs,
            best_2_clubs = [
                end_match.first_club,
                end_match.second_club
            ]
        )
        await sender_end_match.send_info_to_clubs()
        


        send_congratulation = SendCongratulationEndMatch()
        self.scheduler_best_league.add_job(
            func = send_congratulation.send_info_to_clubs,
            trigger = SEND_GONGRATULATION_END_BEST_MATCH
            )
        
        await self.start_match(end_match)
        
    async def _start_league(self):
        league_matchs = await self.best_league_service.get_matches()

        for match in league_matchs:
            await self.start_match(match)


    
    async def start_match(self, match: LeagueFight) -> None:
        if match.time_to_start < datetime.now():
            return
        
        match_club = ClubMatch(
            first_club_id  = match.first_club.id,
            second_club_id = match.second_club.id,
            start_time     = match.time_to_start,
            match_id       = match.match_id,
            group_id       = match.group_id
        )

        time_send_join_match_text = match.time_to_start.replace(
            hour = 15,
            minute = 0
        )

        
        time_start_match = match.time_to_start.replace(
            hour = 16,
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