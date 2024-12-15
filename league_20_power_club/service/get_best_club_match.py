from datetime import datetime, timedelta
from uuid import uuid4

from database.models.league_fight import LeagueFight
from database.models.club import Club

from league_20_power_club.types import LeagueBestClubRanking
from league_20_power_club.utils.best_club_create_match import (
    generate_matches_club, 
    generate_club_group,
    get_top_20_club
) 

from services.best_20_club_league_service import Best20ClubLeagueService
from services.league_service import LeagueFightService


class BestClubLeagueMatchService:
 
    async def get_matches(self) -> list[LeagueFight]:    
        best_top_20_club_league = await Best20ClubLeagueService.get_top_20_club_matches()
        if not best_top_20_club_league:
            await self.generate_top_20_club_matches()
            best_top_20_club_league = await Best20ClubLeagueService.get_top_20_club_matches()
        
        return best_top_20_club_league
        

        
    async def generate_top_20_club_matches(self):
        top_20_clubs = await get_top_20_club()
        group_generator = generate_club_group(top_20_clubs)
        for group in LeagueBestClubRanking:
            group_clubs = next(group_generator)
            await self.create_matches(
                group_clubs = group_clubs,
                group       = group
            )   
    
    async def create_matches(
        self, 
        group_clubs: list[Club],
        group: LeagueBestClubRanking
    ) -> None:
        
        matches_group:list[list[Club]] = generate_matches_club(clubs = group_clubs)
        start_date_match = datetime.now().replace(hour = 16, minute = 0, second= 0 )
        for match in matches_group:
            await self.create_matches_day(
                clubs_match_day = match,
                date_match      = start_date_match,
                group           = group
            )
            start_date_match = start_date_match + timedelta(days=1)

            
        
    async def create_matches_day(
        self, 
        clubs_match_day: list[list[Club]],
        date_match: datetime,
        group: LeagueBestClubRanking
    ) -> None:
        
        for match in clubs_match_day:
            match_id = str(uuid4())
            
            await LeagueFightService.create_league_fight(
                match_id = match_id,
                first_club_id  = match[0].id,
                second_club_id = match[1].id,
                time_to_start = date_match,
                group_id = group.value,
                is_top_20_club = True
            )
            

