from aiogram import Router
from .join_to_fight_handler import join_to_fight_router
from .league_handler import league_router

league_main_router = Router()
league_main_router.include_routers(
    join_to_fight_router,
    league_router
)