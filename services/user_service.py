from database.models.user_bot import UserBot
from database.session import get_session
from sqlalchemy import select, update
from config import DatabaseType

class UserService:

    @classmethod
    async def create_user(cls, **kwargs) -> UserBot:
        async for session in get_session():
            async with session.begin(): 
                obj = UserBot(**kwargs)
                session.add(obj)
                return obj

    @classmethod
    async def get_user(cls, user_id) -> UserBot:
        async for session in get_session():
            async with session.begin(): 
                stmt = select(UserBot).filter_by(user_id=user_id)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                return user
            
    @classmethod
    async def get_all_users(cls) -> list[UserBot]:
        async for session in get_session():
            async with session.begin(): 
                stmt = select(UserBot)
                result = await session.execute(stmt)
                return result.scalars().all()
            
    @classmethod
    async def add_referal_user_id(cls, my_user_id: int, referal_user_id: int):
        async for session in get_session():
            async with session.begin(): 
                try:
                    stmt = (
                        update(UserBot)
                        .where(UserBot.user_id == my_user_id)
                        .values(referal_user_id = referal_user_id)
                    )
                    await session.execute(stmt)
                    await session.commit()
                except Exception as e:
                    raise e
        