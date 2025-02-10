from database.models.league_fight import LeagueFight
from database.session import get_session
from sqlalchemy import update
from sqlalchemy import select, or_, and_, func
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

from constants import START_DAY_BEST_LEAGUE

from .types import TypeLeague

class CreateLeagueService:
    
    @staticmethod
    def first_day_last_month() -> datetime:
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)
        return last_day_last_month.replace(day=1)

    @staticmethod
    def last_day_last_month() -> datetime:
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        return first_day_current_month - timedelta(days=1)
    
    
    @classmethod
    async def get_last_months_matches(
        cls, 
        type_league: TypeLeague
    ) -> list[LeagueFight]:
        
        async for session in get_session():
            async with session.begin(): 
                
                query = select(LeagueFight).filter(
                    and_(
                        LeagueFight.time_to_start >= cls.first_day_last_month(),
                        LeagueFight.time_to_start <= cls.last_day_last_month()
                    )
                )
                if type_league == TypeLeague.BEST_LEAGUE:
                    query = query.filter(LeagueFight.is_beast_league == True)
                    
                elif type_league == TypeLeague.TOP_20_CLUB_LEAGUE:
                    query = query.filter(LeagueFight.is_top_20_club == True)
                    
                elif type_league == TypeLeague.DEFAULT_LEAGUE:
                    query = query.filter(
                        and_(
                            LeagueFight.is_beast_league == False,
                            LeagueFight.is_top_20_club == False
                        )
                    )
                    
                result = await session.execute(query)
                return result.scalars().all()