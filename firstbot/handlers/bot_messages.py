from aiogram import Router
from aiogram.types import Message
from keyboards import reply

router = Router()

@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    
    if msg == "погода":
        await message.answer("Ви обрали Погоду!", reply_markup=reply.weather_category)
        await message.delete()

    elif msg == "книги":
       await message.answer("Ви обрали Книги!", reply_markup=reply.book_category)
       await message.delete()
       
    elif msg == "назад":
        await message.answer("Ви повернулися у головне меню!", reply_markup=reply.main_kb)
        await message.delete()
       
    
        


