from database.models.match_character import MatchCharacter
from database.models.character import Character
from league.club_in_match import ClubsInMatch

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.session import get_session
from loader import logger

class MatchCharacterService:
    @classmethod
    async def get_character_in_match(self,
                            club_in_match   : ClubsInMatch,
                            character    : Character
                                    ) -> MatchCharacter | None:
        async for session in get_session():
            async with session.begin():
                stmt = (select(MatchCharacter)
                        .where(MatchCharacter.match_id == club_in_match.match_id)
                        .where(MatchCharacter.group_id == club_in_match.group_id)
                        .where(MatchCharacter.club_id  == character.club_id)
                        .where(MatchCharacter.character_id  == character.id)
                        )
                result = await session.execute(stmt)
                club = result.scalar_one_or_none()
                return club
                
    @classmethod
    async def add_character_in_match(cls, club_in_match: ClubsInMatch, character: Character) -> None:
        async for session in get_session():
            async with session.begin():
                existing_entry = await session.execute(
                    select(MatchCharacter).filter_by(
                        character_id=character.id,
                        match_id=club_in_match.match_id,
                        club_id=character.club_id
                    )
                )
                if existing_entry.scalar():
                    logger.warning(f"Персонаж {character.id} уже существует в матче {club_in_match.match_id}")
                    return

                match_character_obj = MatchCharacter(
                    character_id=character.id,
                    match_id=club_in_match.match_id,
                    group_id=club_in_match.group_id,
                    club_id=character.club_id
                )
                
                session.add(match_character_obj)
                
                try:
                    await session.commit() 
                except IntegrityError as e:
                    print(e)
                    await session.rollback() 
                except Exception as e:
                    await session.rollback() 
                
    @classmethod
    async def get_characters_from_match(cls, match_id: str):
        async for session in get_session():
            async with session.begin():
                stmt = (select(MatchCharacter)
                        .where(MatchCharacter.match_id == match_id)
                        )
                result = await session.execute(stmt)
                return result.scalars().all()
            
    
    @classmethod
    async def get_charaters_club_in_match(cls, match_id: str, club_id: int):
        async for session in get_session():
            async with session.begin():
                stmt = (select(MatchCharacter)
                        .where(MatchCharacter.match_id == match_id)
                        .where(MatchCharacter.club_id == club_id)
                        
                        )
                result = await session.execute(stmt)
                return result.scalars().all()