from aiogram import Router
from .items.items_store import items_store_router
from .items.exclusive_item_store import luxe_items_store_router
from .menu_stores import menu_magazine_router
from .box.box_handler import open_box_roter

magazine_main_router = Router()
magazine_main_router.include_routers(
    menu_magazine_router,
    items_store_router,
    open_box_roter,
    luxe_items_store_router
)