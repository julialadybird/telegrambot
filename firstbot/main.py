import asyncio

from aiogram import Bot, Dispatcher, types
from config import private, TOKEN_API
from handlers import bot_messages, user_commands
from callbacks import callbacks
import database


async def main():
    bot = Bot(token=TOKEN_API, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        callbacks.router,
        bot_messages.router
    )
    await database.db_connect()
    # await database.insert_books()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, )


if __name__ == "__main__":
    asyncio.run(main()) 