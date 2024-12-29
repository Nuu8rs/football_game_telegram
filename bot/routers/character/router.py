from aiogram import Router
from .create_character import create_character_router
from .menu_character import menu_character_router
from .items_character import items_character_router

character_router = Router()
character_router.include_routers(
    create_character_router,
    menu_character_router,
    items_character_router
)