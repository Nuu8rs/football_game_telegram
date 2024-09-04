from aiogram import Router
from .commands.router import commands_router
from .character.router import charecter_router
from .gym.router import gym_main_router
from .club.router import club_router
from .league.router import league_main_router
from .magazine.router import magazine_main_router


main_router = Router()
main_router.include_routers(
    commands_router,
    charecter_router,
    gym_main_router,
    club_router,
    league_main_router,
    magazine_main_router
)
