import asyncio

import logging
import sys
from aiogram import Bot, Dispatcher, types
# from aiogram.client.session.aiohttp import AiohttpSession
from config import private, TOKEN_API
from handlers import bot_messages, user_commands
from callbacks import callbacks
# import database
import dbpostgres

logging.basicConfig(level=logging.INFO)

async def main():
    # session = AiohttpSession(proxy="http://proxy.server:3128")
    bot = Bot(token=TOKEN_API, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        callbacks.router,
        bot_messages.router
    )
 
    # await database.db_connect()
    await dbpostgres.db_connect()
    # await dbpostgres.insert_movies()
    # await dbpostgres.insert_books()
    # await database.insert_movies()
    # await database.insert_books()
   
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 