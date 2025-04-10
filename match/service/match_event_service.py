from database.session import get_session
from sqlalchemy.future import select
from sqlalchemy import func, update

from database.models.match_event import MatchEvent
from datetime import datetime

class MatchEventService:
    
    @classmethod
    async def add_event(
        cls,
        match_event: MatchEvent
    ):
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(match_event)
                except:
                    pass
                await session.commit()
                return
    
    
        async def get_