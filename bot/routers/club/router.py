from aiogram import Router
from .my_club import my_club_router
from .create_club import create_club_router
from .find_club import find_club_router

club_router = Router()
club_router.include_routers(
    my_club_router,
    create_club_router,
    find_club_router
    
)