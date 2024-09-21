from aiogram import Router
from .start import start_router
from .instruction import send_instruction_router
from .admin_comands import admin_comands_router

commands_router = Router()
commands_router.include_routers(
    start_router,
    send_instruction_router,
    admin_comands_router
)