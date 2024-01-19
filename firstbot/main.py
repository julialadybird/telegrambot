from aiogram import Bot, Dispatcher, F
import asyncio

from handlers import bot_messages, user_commands, questionaire


HELP_TEXT = """
<b>/start</b> - <em>start bot</em>
<b>/sticker</b> - <em>send stiker</em>
<b>/help</b> - <em>show all commands</em>
"""


async def main():
    TOKEN_API= "6706585845:AAET38gtbHZPNnz8gFeHj4Qc4nMI11MKhsk"
    bot = Bot(token=TOKEN_API, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        questionaire.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())