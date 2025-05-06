from aiogram import Router

from .routers.statistic_club_league import menu_choice_league_club_router
from .routers.menu_choice_statistic import menu_statistic_router

statistic_router = Router()
statistic_router.include_routers(
    menu_statistic_router,
    menu_choice_league_club_router
)