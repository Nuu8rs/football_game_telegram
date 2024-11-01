from database.models.character import Character
from database.models.item import Item

from database.session import get_session
from sqlalchemy import select, desc


class AdminFunctionalService:
    
    @classmethod
    async def get_characters_by_exp(cls, min_exp: int,max_exp:int):
        async for session in get_session():
            async with session.begin():
                try:
                    stmt = select(Character).where(
                        Character.exp >= min_exp,
                        Character.exp <= max_exp,
                        Character.is_bot == False
                    )
                    result = await session.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    print(E)
                    
    @classmethod
    async def get_new_members_character(cls, count_members: int) -> list[Character]:
        async for session in get_session():
            async with session.begin():
                try:
                    stmt = (
                        select(Character)
                        .where(Character.is_bot == False)
                        .order_by(desc(Character.created_at))
                        .limit(count_members)
                    )
                    result = await session.execute(stmt)
                    return result.scalars().all()
                except Exception as E:
                    print(E)