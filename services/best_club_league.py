import calendar
from datetime import datetime

from database.models.league_fight import LeagueFight
from database.session import get_session
from sqlalchemy import select, or_, and_, func, case, desc

from database.models.club import Club


class BestLeagueService:

    @classmethod
    async def get_top_24_clubs(cls) -> list[Club]:
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month_20th = now.replace(day=20, hour=0, minute=0, second=0, microsecond=0)

        async for session in get_session():
            async with session.begin():
                # Подзапрос для очков, забитых и пропущенных голов для первой и второй команды
                first_team_points = (
                    select(
                        LeagueFight.first_club_id.label("club_id"),
                        func.sum(
                            case(
                                (LeagueFight.goal_first_club > LeagueFight.goal_second_club, 3),
                                (LeagueFight.goal_first_club == LeagueFight.goal_second_club, 1),
                                else_=0,
                            )
                        ).label("points"),
                        func.sum(LeagueFight.goal_first_club).label("goals_scored"),
                        func.sum(LeagueFight.goal_second_club).label("goals_conceded")
                    )
                    .where(LeagueFight.time_to_start >= start_of_month)
                    .where(LeagueFight.time_to_start <= end_of_month_20th)
                    .group_by(LeagueFight.first_club_id)
                )

                second_team_points = (
                    select(
                        LeagueFight.second_club_id.label("club_id"),
                        func.sum(
                            case(
                                (LeagueFight.goal_second_club > LeagueFight.goal_first_club, 3),
                                (LeagueFight.goal_second_club == LeagueFight.goal_first_club, 1),
                                else_=0,
                            )
                        ).label("points"),
                        func.sum(LeagueFight.goal_second_club).label("goals_scored"),
                        func.sum(LeagueFight.goal_first_club).label("goals_conceded")
                    )
                    .where(LeagueFight.time_to_start >= start_of_month)
                    .where(LeagueFight.time_to_start <= end_of_month_20th)
                    .group_by(LeagueFight.second_club_id)
                )

                # Объединяем результаты для первой и второй команды
                combined_points = first_team_points.union_all(second_team_points).subquery()

                # Агрегируем данные по клубам
                aggregated_points = (
                    select(
                        combined_points.c.club_id,
                        func.sum(combined_points.c.points).label("total_points"),
                        func.sum(combined_points.c.goals_scored).label("total_goals_scored"),
                        func.sum(combined_points.c.goals_conceded).label("total_goals_conceded"),
                        (func.sum(combined_points.c.goals_scored) - func.sum(combined_points.c.goals_conceded)).label("goal_difference")
                    )
                    .group_by(combined_points.c.club_id)
                    .subquery()
                )

                # Финальный запрос для получения клубов
                final_query = (
                    select(Club)
                    .join(aggregated_points, aggregated_points.c.club_id == Club.id)
                    .order_by(
                        aggregated_points.c.total_points.desc(),
                        aggregated_points.c.goal_difference.desc(),
                        aggregated_points.c.total_goals_scored.desc()
                    )
                    .limit(24)
                )

                result = await session.execute(final_query)
                return [club for club, in result]

                        
                
    @classmethod
    async def get_best_league(cls) -> list[LeagueFight]:
        now = datetime.now()
        last_day = calendar.monthrange(now.year, now.month)[1]

        start_date = now.replace(day=21, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        
        async for session in get_session():
            async with session.begin():
                stmt =  (
                    select(LeagueFight)
                    .filter(LeagueFight.time_to_start >= start_date)
                    .filter(LeagueFight.time_to_start <= end_date)
                    .filter(LeagueFight.is_beast_league == True)
                )
                
                result = await session.execute(stmt)
                return result.scalars().all()
            
            
    @classmethod
    async def my_club_in_beast_league(cls, club_id: int):
        async for session in get_session():
            async with session.begin():             
                now = datetime.now()
                last_day = calendar.monthrange(now.year, now.month)[1]
                start_date = now.replace(day=21, hour=0, minute=0, second=0, microsecond=0)
                end_date = now.replace(day=last_day, hour=23, minute=59)
                
                stmt = select(LeagueFight).filter(
                    (LeagueFight.first_club_id == club_id) | 
                    (LeagueFight.second_club_id == club_id),
                    LeagueFight.is_beast_league == True,
                    LeagueFight.time_to_start >= start_date,
                    LeagueFight.time_to_start <= end_date
                )
                result = await session.execute(stmt)
                return result.scalars().first()
                
        
    @classmethod
    async def get_next_league_fight_by_club(cls, club_id: int):
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
                        .where(LeagueFight.is_beast_league == True)
                        .order_by(LeagueFight.time_to_start.asc())
                        .limit(1)
                    )
                    result = next_fight.scalars().first()
                    return result
                except Exception as e:
                    print(f"Ошибка при получении следующего матча для команди {club_id}: {e}")
                    return None
                