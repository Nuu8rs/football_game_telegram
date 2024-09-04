from database.models import UserBot
from database.session import get_session
from sqlalchemy.future import select
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