                                                                                                 main.py
import logging
import os
import sys

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.handler import start
from bot.handler.admin import admin_router
from config import conf
from db import database

TOKEN = os.getenv("BOT_TOKEN")


async def on_start(bot: Bot):
    await database.create_all()
    command_user = [BotCommand(command='start', description="Bo'tni ishga tushirish")]
    await bot.set_my_commands(commands=command_user)
    await bot.set_webhook(f"{conf.bot.BASE_WEBHOOK_URL}{conf.bot.WEBHOOK_PATH}", secret_token=conf.bot.WEBHOOK_SECRET)


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()


async def main():
    dp = Dispatcher()
    dp.include_routers(start.start_router, admin_router)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)


def main_webhook() -> None:
    dp = Dispatcher()
    dp.include_routers(start.start_router, admin_router)

    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=conf.bot.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=conf.bot.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=conf.bot.WEB_SERVER_HOST, port=conf.bot.WEB_SERVER_PORT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # asyncio.run(main())
    main_webhook()
