import asyncio
import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram import Dispatcher, Bot

from bot.handler import start
from bot.handler.admin import admin_router
from config import conf

from db import database


async def on_start(bot: Bot):
    await database.create_all()
    command_user = [BotCommand(command='start', description="Bo'tni ishga tushirish")]
    await bot.set_my_commands(commands=command_user)


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()


# async def main():
#     dp = Dispatcher()
#     dp.include_routers(start.start_router, admin_router)
#     dp.startup.register(on_start)
#     dp.shutdown.register(on_shutdown)
#     bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
#     await dp.start_polling(bot)


async def main():
    dp = Dispatcher()
    dp.include_routers(start.start_router, admin_router)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# 1065  docker login
# 1068  docker build -t nickname/name .
# 1071  docker push nickname/name

# docker run --name db_mysql -e MYSQL_ROOT_PASSWORD=1 -d mysql
