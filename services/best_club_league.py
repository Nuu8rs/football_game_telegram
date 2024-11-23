from datetime import datetime


from database.models.league_fight import LeagueFight
from database.session import get_session
from sqlalchemy import select, or_, and_, func, case, desc

from database.models.club import Club


class BestLeagueService:

    @classmethod
    async def get_top_24_clubs(cls) -> list[Club]:
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0)
        end_of_month_20th = now.replace(day=20, hour=0)

        
        async for session in get_session():
            async with session.begin():
                points_query = (
                    select(
                        LeagueFight.first_club_id.label("club_id"),
                        func.sum(
                            case(
                                (LeagueFight.goal_first_club > LeagueFight.goal_second_club, 3),
                                (LeagueFight.goal_first_club == LeagueFight.goal_second_club, 1),
                                else_=0,
                            )
                        ).label("total_points")
                    )
                    .filter(LeagueFight.time_to_start >= start_of_month)
                    .filter(LeagueFight.time_to_start <= end_of_month_20th)
                    .group_by(LeagueFight.first_club_id)
                    .union_all(
                        select(
                            LeagueFight.second_club_id.label("club_id"),
                            func.sum(
                                case(
                                    (LeagueFight.goal_second_club > LeagueFight.goal_first_club, 3),
                                    (LeagueFight.goal_second_club == LeagueFight.goal_first_club, 1),
                                    else_=0,
                                )
                            ).label("total_points")
                        )
                        .filter(LeagueFight.time_to_start >= start_of_month)
                        .filter(LeagueFight.time_to_start <= end_of_month_20th)
                        .group_by(LeagueFight.second_club_id)
                    )
                ).subquery()

                final_points_query = (
                    select(
                        points_query.c.club_id,
                        func.sum(points_query.c.total_points).label("total_points")
                    )
                    .group_by(points_query.c.club_id)
                    .subquery()
                )

                final_query = (
                    select(Club, final_points_query.c.total_points)
                    .join(final_points_query, final_points_query.c.club_id == Club.id)
                    .group_by(Club.id)
                    .order_by(func.sum(final_points_query.c.total_points).desc())
                    .limit(24)
                )

                top_clubs = await session.execute(final_query)
                return [(club, total_points) for club, total_points in top_clubs]
                        
                
    @classmethod
    async def get_best_league(cls) -> list[LeagueFight]:
        now = datetime.now()
        start_date = now.replace(day=21, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=30, hour=23, minute=59, second=59, microsecond=999999)

        
        async for session in get_session():
            async with session.begin():
                stmt =  (
                    select(LeagueFight)
                    .filter(LeagueFight.time_to_start >= start_date)
                    .filter(LeagueFight.time_to_start <= end_date)
                )
                
                result = await session.execute(stmt)
                return result.scalars().all()
            
            
    @classmethod
    async def my_club_in_beast_league(cls, club_id: int):
        async for session in get_session():
            async with session.begin():             
                now = datetime.now()
                start_date = now.replace(day=21, hour=0, minute=0, second=0, microsecond=0)
                end_date = now.replace(day=30, hour=23, minute=59, second=59, microsecond=999999)
                
                stmt = select(LeagueFight).filter(
                    (LeagueFight.first_club_id == club_id) | 
                    (LeagueFight.second_club_id == club_id),
                    LeagueFight.is_beast_league == True,
                    LeagueFight.time_to_start >= start_date,
                    LeagueFight.time_to_start <= end_date
                )
                result = await session.execute(stmt)
                return result.scalars().first()
                
        
    