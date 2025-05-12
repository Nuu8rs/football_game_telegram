from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from sqlalchemy import select, or_

from constants_leagues import TypeLeague, BaseConfigLeague

from database.models.league_fight import LeagueFight
from database.session import get_session


class BaseLeagueService(ABC):
    config: BaseConfigLeague

    @classmethod
    @abstractmethod
    async def get_league(
        cls, 
        type_league: TypeLeague
    ) -> Optional[list[LeagueFight]]:
        raise NotImplementedError("This method should be overridden in subclasses")

    @classmethod
    @abstractmethod
    async def my_club_in_league(
        cls,
        type_league: TypeLeague
    ) -> Optional[list[LeagueFight]]:
        raise NotImplementedError("This method should be overridden in subclasses")

    @classmethod
    @abstractmethod
    async def get_next_league_fight_by_club(
        cls, 
        club_id: int,
        type_league: TypeLeague
    ) -> Optional[LeagueFight]:
        raise NotImplementedError("This method should be overridden in subclasses")


class LeagueService(BaseLeagueService):
    config: BaseConfigLeague
    
    @classmethod
    async def get_league(
        cls, 
        type_league: TypeLeague,

    ) -> Optional[list[LeagueFight]]:
        async for session in get_session():
            async with session.begin():
                stmt = (
                    select(LeagueFight)
                    .where(LeagueFight.type_league == type_league)
                    .filter(LeagueFight.time_to_start >= cls.config.DATETIME_START_LEAGUE)
                    .filter(LeagueFight.time_to_start <= cls.config.DATETIME_END_LEAGUE)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
            
                

    async def my_club_in_league(
        cls,
        type_league: TypeLeague,
        club_id: int
    ) -> Optional[list[LeagueFight]]:
        async for session in get_session():
            async with session.begin():
                stmt = (
                    select(LeagueFight)
                    .filter(
                        (LeagueFight.first_club_id == club_id) | 
                        (LeagueFight.second_club_id == club_id),
                        LeagueFight.is_top_20_club == True,
                        LeagueFight.time_to_start >= cls.config.DATETIME_START_LEAGUE,
                        LeagueFight.time_to_start <= cls.config.DATETIME_END_LEAGUE
                    )
                )
                result = await session.execute(stmt)
                return result.scalars().first()

    async def get_next_league_fight_by_club(
        self, 
        club_id: int,
        type_league: TypeLeague
    ) -> Optional[LeagueFight]:
        
        async for session in get_session():
            async with session.begin():
                stmt = (
                    select(LeagueFight)
                    .where(
                        LeagueFight.time_to_start > datetime.now(),
                        LeagueFight.type_league == type_league,
                        or_(
                            LeagueFight.first_club_id == club_id,
                            LeagueFight.second_club_id == club_id
                        )
                    )
                    .order_by(LeagueFight.time_to_start.asc())
                    .limit(1)
                )
                result = await session.execute(stmt)
                return result.scalars().first()
