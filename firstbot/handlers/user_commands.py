from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import reply, inline
from main import *

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привіт, <b>{message.from_user.first_name}!</b>\n\n"
                         f"<em>Цей бот допоможе тобі обрати:</em>\n📚<b>Книгу</b> з позитивними відгуками для гарного проведення дoзвілля\n"
                         f"🎬<b>Кіно</b> з гарним рейтингом для цікавого перегляду у вільний час\n\n"
                         f"Також цей бот дає можливість <b>зберігати</b> обране та <b>видаляти</b> зі збереженого при необхідності!", reply_markup=inline.start_category)
    await message.delete()


