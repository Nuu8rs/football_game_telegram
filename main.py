import asyncio

from loader import bot, dp
from bot.routers.router import main_router


dp.include_router(main_router)


async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
