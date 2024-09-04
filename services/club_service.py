from database.models import Club
from database.session import get_session
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from config import DatabaseType
from typing import Dict, List
from constants import MAX_LEN_MEMBERS_CLUB

class ClubService:
    @classmethod
    async def get_club(cls, club_id: int) -> Club:
        async for session in get_session():
            async with session.begin():
                stmt = select(Club).filter_by(id=club_id)
                result = await session.execute(stmt)
                club = result.scalar_one_or_none()
                return club
            
    @classmethod
    async def get_club_by_owner_id(cls, owner_id: int) -> Club:
        async for session in get_session():
            async with session.begin():
                stmt = select(Club).filter_by(owner_id=owner_id)
                result = await session.execute(stmt)
                club = result.scalar_one_or_none()
                return club


    @classmethod
    async def get_all_clubs(cls) -> list[Club]:
        async for session in get_session():
            async with session.begin():
                stmt = select(Club)
                result = await session.execute(stmt)
                clubs = result.scalars().all()
                return clubs
            
    @classmethod
    async def get_all_clubs_to_join(cls) -> list[Club]:
        async for session in get_session():
            async with session.begin():
   
                subquery = (
                    select(
                        Club.id.label('club_id'),
                        func.count().label('characters_count')
                    )
                    .select_from(Club)
                    .join(Club.characters)
                    .group_by(Club.id)
                    .subquery()
                )
                

                stmt = (
                    select(Club)
                    .join(subquery, Club.id == subquery.c.club_id)
                    .where(Club.is_fake_club == False)
                    .where(subquery.c.characters_count < MAX_LEN_MEMBERS_CLUB)
                )
                result = await session.execute(stmt)
                clubs = result.scalars().all()
                return clubs
            
    @classmethod
    async def create_club(cls, name_club: str, owner_id: int, fake_club = False, league:str  = "🟢 Ліга новачків") -> Club:
        async for session in get_session():
            async with session.begin(): 
                obj = Club(
                    owner_id  = owner_id,
                    name_club = name_club,
                    is_fake_club = fake_club,
                    league = league
                )
                session.add(obj)
                merged_obj = await session.merge(obj)
                return merged_obj
            
    @classmethod
    async def update_link_to_chat(cls, club: Club, new_link: str) -> None:
        async for session in get_session():
            async with session.begin():
                club.link_to_chat = new_link
                merged_obj = await session.merge(club)
                return merged_obj
            
    @classmethod
    async def get_clubs_by_league(cls) -> Dict[str, List['Club']]:
        async for session in get_session(): 
            async with session.begin():
                result = await session.execute(select(Club).order_by(Club.league))
                clubs = result.scalars().all()
                clubs_by_league = {}
                for club in clubs:
                    if club.league not in clubs_by_league:
                        clubs_by_league[club.league] = []
                    clubs_by_league[club.league].append(club)
                return clubs_by_league
            
    @classmethod
    async def donate_energy(cls, club: Club, count_energy: int) -> None:
        async for session in get_session():
            async with session.begin():
                club.energy_applied += count_energy
                merged_obj = await session.merge(club)
                return merged_obj