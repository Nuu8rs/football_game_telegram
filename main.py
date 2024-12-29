from aiohttp import web
import asyncio

from bot.routers.router import main_router
from loader import bot, dp, app

from config import (
    WEBAPP_HOST, 
    WEBAPP_PORT, 

)

dp.include_router(main_router)


async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
async def start_weebhook():

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)    
    await site.start()
    
async def main():
    await asyncio.gather(
        start_weebhook(),
        start_polling()
    )
    
if __name__ == "__main__":
    asyncio.run(main())


"""
alembic revision --autogenerate -m "add new realship to Item"
alembic upgrade head
"""