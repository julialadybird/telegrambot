from aiogram import Router
from aiogram.types import Message
from keyboards import inline

router = Router()

@router.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "книги":
        await message.answer("<b>Ви обрали Книги!</b>", reply_markup=inline.book_category)
        await message.delete()

    elif msg == "кіно":
        await message.answer("<b>Ви обрали Кіно!</b>", reply_markup=inline.film_category)
        await message.delete()

    
        


