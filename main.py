import asyncio
from aiohttp import web

from loader import bot, dp
from bot.routers.router import main_router

from webhook_api.handlers import MonoResult
from config import WEBAPP_HOST, WEBAPP_PORT

dp.include_router(main_router)


async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
async def start_weebhook():
    app = web.Application()
    app.router.add_post("/mono-result", MonoResult.router)
    
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