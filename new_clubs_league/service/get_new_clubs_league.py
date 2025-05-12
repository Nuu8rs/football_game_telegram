from datetime import datetime, timedelta

from database.models.league_fight import LeagueFight
from database.models.club import Club

from bot.club_infrastructure.distribute_points.add_points_from_league import AddPointsToClub
from bot.club_infrastructure.distribute_points.scheduler_distribute_points import ShedulerdistributePoints

from bot.utils.get_top_24_club_by_league import get_top_24_clubs
from best_club_league.types import LeagueRanking
from best_club_league.utils.league_create_match import (
    generate_club_group,
    generate_matches_club
)

from services.league_services.new_clubs_league_service import NewClubsLeagueService
from services.league_service import LeagueFightService

from constants_leagues import config_new_club_league

# from league.service.types import TypeLeague

from uuid import uuid4

class NewClubLeaguRepository:
        
    async def get_matches(self) -> list[LeagueFight]:    
        best_club_league = await NewClubsLeagueService.get_league()
        if not best_club_league:
            await self.generate_matches()
            best_club_league = await NewClubsLeagueService.get_league()
        
        return best_club_league
        
    async def get_clubs(self) -> list[Club]:
        fights = await LeagueFightService.get_league_fights_current_month()
        sorted_rankings = get_top_24_clubs(fights)
        return [club['club'] for club in sorted_rankings][:24]
        
    async def generate_matches(self):
        all_clubs = await self.get_top_clubs()
        for num_group in config_new_club_league.COUNT_GROUP:
            clubs = 
        # group_generator = generate_club_group(top_clubs)
        # for group in LeagueRanking:
        #     group_clubs = next(group_generator)
        #     await self.create_matches(
        #         group_clubs = group_clubs,
        #         group       = group
        #     )   
    
    async def create_matches(
        self, 
        group_clubs: list[Club],
        group: LeagueRanking
    ) -> None:
        
        matches_group:list[list[Club]] = generate_matches_club(clubs = group_clubs)
        start_date_match = datetime.now().replace(hour = 21, minute = 0, second= 0 )
        for match in matches_group:
            await self.create_matches_day(
                clubs_match_day = match,
                date_match      = start_date_match,
                group           = group
            )
            start_date_match = start_date_match + timedelta(days=1)
        else:
            points_manager = AddPointsToClub(
                group_ids      = [group],
                type_league    = TypeLeague.BEST_LEAGUE,
                league_ranking = group
            )
            sheduler = ShedulerdistributePoints(
                time_distribute= start_date_match + timedelta(days=1, minutes = 5),
                points_manager  = points_manager
            )
            await sheduler.start_wait_distribute_points()
            
        
    async def create_matches_day(
        self, 
        clubs_match_day: list[list[Club]],
        date_match: datetime,
        group: LeagueRanking
    ) -> None:
        
        for match in clubs_match_day:
            match_id = str(uuid4())
            
            await LeagueFightService.create_league_fight(
                match_id = match_id,
                first_club_id  = match[0].id,
                second_club_id = match[1].id,
                time_to_start = date_match,
                group_id = group.value,
                is_beast_league = True
            )
            

