from aiogram import Router
from .start import start_router
from .instruction import send_instruction_router
from .admins_functional.get_logging_file import get_logger_router

commands_router = Router()
commands_router.include_routers(
    start_router,
    send_instruction_router,
    get_logger_router

)