from aiogram import Router
from .join_to_fight_handler import join_to_fight_router
from .league_handler import league_router
from .add_energy_in_match import add_energy_in_match_router

league_main_router = Router()
league_main_router.include_routers(
    join_to_fight_router,
    league_router,
    add_energy_in_match_router
)