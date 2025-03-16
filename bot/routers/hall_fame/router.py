from aiogram import Router
from .hall_fame import hall_fame_router
from .position_rating import hall_fame_position_rating_router


hall_fame_main_router = Router()
hall_fame_main_router.include_routers(
    hall_fame_router,
    hall_fame_position_rating_router
)