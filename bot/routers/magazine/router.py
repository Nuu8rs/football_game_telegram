from aiogram import Router
from .magazine import magazine_router


magazine_main_router = Router()
magazine_main_router.include_routers(
    magazine_router
)