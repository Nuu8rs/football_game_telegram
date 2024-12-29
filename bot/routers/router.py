from aiogram import Router
from .commands.router import commands_router
from .character.router import character_router
from .gym.router import gym_main_router
from .club.router import club_router
from .league.router import league_main_router
from .stores.router import magazine_main_router
from .hall_fame.router import hall_fame_main_router
from .pvp_duels.router import duel_main_router
from .communication.router import communication_main_router
from .commands.admins_functional.newsletter import admin_newsletter_commands
from .commands.admins_functional.info_new_members import admin_info_new_member_router
from .сhristmas_tree.router import christmas_tree_router


main_router = Router()
main_router.include_routers(
    commands_router,
    character_router,
    gym_main_router,
    club_router,
    league_main_router,
    magazine_main_router,
    duel_main_router,
    hall_fame_main_router,
    communication_main_router,
    admin_newsletter_commands,
    admin_info_new_member_router,
    christmas_tree_router
)
