from aiogram import Router
from .gym_handler import gym_router
from .donate_club_energy_handler import donate_club_energy_router
from .education_center import education_center_router
from .massage_room import massage_room_router

gym_main_router = Router()
gym_main_router.include_routers(
    gym_router,
    donate_club_energy_router,
    education_center_router,
    massage_room_router
)