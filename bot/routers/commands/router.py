from aiogram import Router
from .start import start_router
from .instruction import send_instruction_router
from .admins_functional.newsletter import admin_newsletter_commands
from .admins_functional.info_new_members import admin_info_new_member_router

commands_router = Router()
commands_router.include_routers(
    start_router,
    send_instruction_router,
    admin_newsletter_commands,
    admin_info_new_member_router
)