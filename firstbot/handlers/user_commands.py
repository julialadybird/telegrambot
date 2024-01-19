from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from main import *
import random

from keyboards import reply

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, <b>{message.from_user.first_name}!</b>\n\nYou can use commands:\n/sticker\n/help\n/start", reply_markup=reply.main_kb)


@router.message(Command(commands=["sticker"]))
async def send_sticker(message: Message, bot: Bot):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAELGvxlmZRxjdh1xqYaaOPXCNTOjsVp1QAC8iwAAnDW4UuITBkIiCOD3zQE")
    await message.delete()


@router.message(Command(commands=["help"])) 
async def help(message: Message):
    await message.reply(text=HELP_TEXT)


@router.message(Command(commands=["rn", "random-number"]))
async def get_random_num(message: Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split("-")]
    rnum = random.randint(a, b)
    await message.reply(f"Random number: {rnum}")