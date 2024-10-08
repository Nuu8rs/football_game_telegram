from database.models.league_fight import LeagueFight
from database.session import get_session
from sqlalchemy import update
from sqlalchemy import select, or_, and_, func
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

class LeagueFightService:
    @classmethod
    async def create_league_fight(cls, 
                                  match_id: int, 
                                  first_club_id: int, 
                                  second_club_id: int, 
                                  time_to_start: datetime,
                                  group_id: int) -> LeagueFight:
        league_fight = LeagueFight(
            match_id=match_id,
            first_club_id=first_club_id,
            second_club_id=second_club_id,
            time_to_start=time_to_start,
            group_id=group_id
        )
        
        async for session in get_session():
            async with session.begin():
                try:
                    session.add(league_fight)
                    merged_obj = await session.merge(league_fight)
                    await session.commit()
                    return merged_obj
                except SQLAlchemyError as e:
                    await session.rollback()
                    print(f"Ошибка при создании битвы: {e}")
                    return None
                
    @classmethod
    async def get_league_fights_current_month(cls) -> list[LeagueFight]:
        current_date = datetime.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        async for session in get_session():
            async with session.begin():
                try:
                    league_fights = await session.execute(
                        select(LeagueFight).where(
                            LeagueFight.time_to_start >= start_of_month,
                            LeagueFight.time_to_start <= end_of_month
                        )
                    )
                    return league_fights.scalars().all()
                except SQLAlchemyError as e:
                    print(f"Ошибка при получении битв за текущий месяц: {e}")
                    return []
                
    @classmethod
    async def get_next_league_fight_by_club(cls, club_id: int) -> LeagueFight | None:
        today = datetime.now()

        async for session in get_session():
            async with session.begin():
                try:
                    next_fight = await session.execute(
                        select(LeagueFight)
                        .where(
                            LeagueFight.time_to_start > today,
                            or_(
                                LeagueFight.first_club_id == club_id,
                                LeagueFight.second_club_id == club_id
                            )
                        )
                        .order_by(LeagueFight.time_to_start.asc())
                        .limit(1)
                    )
                    result = next_fight.scalars().first()
                    return result
                except SQLAlchemyError as e:
                    print(f"Ошибка при получении следующего матча для клуба {club_id}: {e}")
                    return None
                
                
    @classmethod
    async def get_the_monthly_matches_by_club(cls, club_id: int) -> LeagueFight | None:
        today = datetime.now().date().replace(day=1)
        async for session in get_session():
            async with session.begin():
                try:
                    league_fights = await session.execute(
                        select(LeagueFight)
                        .where(
                                LeagueFight.time_to_start >= today,
                            or_(
                                LeagueFight.first_club_id == club_id,
                                LeagueFight.second_club_id == club_id
                            )
                        )
                        .order_by(LeagueFight.time_to_start.asc())
                    )
                    return league_fights.scalars().all()
                except SQLAlchemyError as e:
                    print(f"Ошибка при получении следующего матча для клуба {club_id}: {e}")
                    return None
                
    @classmethod
    async def get_the_monthly_matches_by_group(cls, group_id: str) -> list[LeagueFight] | None:
        today = datetime.now().date().replace(day=1)
        async for session in get_session():
            async with session.begin():
                try:
                    league_fights = await session.execute(
                        select(LeagueFight)
                        .where(
                            LeagueFight.time_to_start >= today
                        ).where(    
                            LeagueFight.group_id == group_id
                        )
                        .order_by(LeagueFight.time_to_start.asc())
                    )
                    return league_fights.scalars().all()
                except SQLAlchemyError as e:
                    print(f"Ошибка при получении матчей для группы {group_id} за текущий месяц: {e}")
                    return None
                
    @classmethod
    async def get_group_id_by_club(cls, club_id: int) -> str | None:
        now = datetime.now()
        start_of_month = now.replace(day=1)
        next_month = (start_of_month + timedelta(days=32)).replace(day=1)

        async for session in get_session():
            async with session.begin():
                try:
                    league_fight = await session.execute(
                        select(LeagueFight.group_id)
                        .where(
                            or_(
                                LeagueFight.first_club_id == club_id,
                                LeagueFight.second_club_id == club_id
                            ),
                            # Добавляем условие на дату
                            LeagueFight.time_to_start >= start_of_month,
                            LeagueFight.time_to_start < next_month
                        )
                        .limit(1)
                    )
                    group_id = league_fight.scalar()
                    return group_id
                except SQLAlchemyError as e:
                    print(f"Ошибка при получении group_id для клуба {club_id}: {e}")
                    return None
                
    @classmethod
    async def increment_goal(cls, match_id: str, club_id: int, add_goal: int = 1) -> LeagueFight:
        async for session in get_session():
            async with session.begin():
                try:
                    league_fight = await session.execute(
                        select(LeagueFight).where(LeagueFight.match_id == match_id)
                    )
                    league_fight_obj = league_fight.scalars().first()

                    if not league_fight_obj:
                        print(f"Матч с ID {match_id} не найден.")
                        return None

                    if league_fight_obj.first_club_id == club_id:
                        league_fight_obj.goal_first_club += add_goal
                    elif league_fight_obj.second_club_id == club_id:
                        league_fight_obj.goal_second_club += add_goal
                    else:
                        print(f"Клуб с ID {club_id} не участвует в матче с ID {match_id}.")
                        return None

                    session.add(league_fight_obj)
                    await session.commit()
                    return league_fight_obj
                except SQLAlchemyError as e:
                    print(f"Ошибка при увеличении счета в матче {match_id}: {e}")
                    return None
                
                
    @classmethod
    async def get_league_fight(cls, match_id: str) -> LeagueFight:
        async for session in get_session():
            async with session.begin():
                stmt = select(LeagueFight).filter_by(match_id = match_id)
                result = await session.execute(stmt)
                club = result.scalar_one_or_none()
                return club
            
            
    @classmethod
    async def get_match_today(cls, club_id: int) -> LeagueFight:
        current_date = datetime.now().date()
        async for session in get_session():
            async with session.begin():
                stmt = select(LeagueFight).where(
                    and_(
                        func.date(LeagueFight.time_to_start) == current_date, 
                        or_(
                            LeagueFight.first_club_id == club_id,  
                            LeagueFight.second_club_id == club_id 
                        )
                    )
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()