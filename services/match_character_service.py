from database.models.match_character import MatchCharacter
from database.models.character import Character
from league.process_match.club_in_match import ClubsInMatch

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError

from database.session import get_session
from logging_config import logger

class MatchCharacterService:
    @classmethod
    async def get_character_in_match(
        self,
        match_id: str,
        group_id: str,
        club_id: int,
        character_id: int
    ) -> MatchCharacter | None:
        
        async for session in get_session():
            async with session.begin():
                stmt = (
                    select(MatchCharacter)
                    .where(MatchCharacter.match_id == match_id)
                    .where(MatchCharacter.group_id == group_id)
                    .where(MatchCharacter.club_id  == character_id)
                    .where(MatchCharacter.character_id  == character_id)
                )
                result = await session.execute(stmt)
                club = result.scalar_one_or_none()
                return club
                
    @classmethod
    async def add_character_in_match(
        cls,
        match_id: str,
        club_id: int,
        group_id: str, 
        character_id: int
    ) -> bool:
        async for session in get_session():
            async with session.begin():
                existing_entry = await session.execute(
                    select(MatchCharacter).filter_by(
                        character_id=character_id,
                        match_id=match_id,
                        club_id=club_id
                    )
                )
                if existing_entry.scalar():
                    logger.warning(f"Персонаж {character_id} уже существует в матче {match_id}")
                    return

                match_character_obj = MatchCharacter(
                    character_id=character_id,
                    match_id=match_id,
                    group_id=group_id,
                    club_id=club_id
                )
                
                session.add(match_character_obj)
                
                try:
                    await session.commit()
                    return True 
                except IntegrityError as e:
                    await session.rollback() 
                except Exception as e:
                    await session.rollback() 
        return False
    @classmethod
    async def get_characters_from_match(cls, match_id: str) -> list[MatchCharacter]:
        async for session in get_session():
            async with session.begin():
                stmt = (select(MatchCharacter)
                        .where(MatchCharacter.match_id == match_id)
                        )
                result = await session.execute(stmt)
                return result.scalars().all()
            
    
    @classmethod
    async def get_charaters_club_in_match(cls, match_id: str, club_id: int) -> list[MatchCharacter]:
        async for session in get_session():
            async with session.begin():
                stmt = (select(MatchCharacter)
                        .where(MatchCharacter.match_id == match_id)
                        .where(MatchCharacter.club_id == club_id)
                        
                        )
                result = await session.execute(stmt)
                return result.scalars().all()
            
            
    @classmethod
    async def add_goal_to_character(cls, match_id: str, character_id: int):
        async for session in get_session():
            async with session.begin():
                match_character = await session.execute(
                    select(MatchCharacter).where(MatchCharacter.match_id == match_id, MatchCharacter.character_id == character_id)
                )
                match_character = match_character.scalar_one_or_none()
                match_character.goals_count += 1
                await session.commit()
                
    @classmethod
    async def get_characters_by_group_id(cls, group_id: int):
        async for session in get_session():
            async with session.begin():
                matchs_character = await session.execute(
                    select(MatchCharacter).where(MatchCharacter.group_id == group_id)
                )
                return matchs_character.scalars().all()
            
            
    @classmethod
    async def delete_character_from_match(cls, character_id: int, match_id: str):
        async for session in get_session():
            async with session.begin():
                await session.execute(
                    delete(MatchCharacter)
                    .where(MatchCharacter.character_id == character_id)
                    .where(MatchCharacter.match_id == match_id)
                )
                await session.commit()
                
    @classmethod
    async def add_score_to_character(
        cls, 
        character_id: int, 
        match_id: str,
        add_score: int
    ) -> None:
        async for session in get_session():
            async with session.begin():
                stmt = (
                    update(MatchCharacter)
                    .where(MatchCharacter.character_id == character_id)
                    .where(MatchCharacter.match_id == match_id)
                    .values(count_score = MatchCharacter.count_score + add_score)
                )
                await session.execute(stmt)
                await session.commit()
                
                
    @classmethod
    async def get_match_mvp(
        cls,
        match_id: str,
        club_id: int
    ) -> MatchCharacter:
        async for session in get_session():
            async with session.begin():
                stmt = (
                    select(MatchCharacter)
                    .where(MatchCharacter.match_id == match_id)
                    .where(MatchCharacter.club_id == club_id)
                    .order_by(MatchCharacter.count_score.desc())
                    .limit(1)
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()