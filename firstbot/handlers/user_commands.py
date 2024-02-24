from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import reply
from utils.states import Weather_by_city, Book
from data.subloader import get_json
from typing import Any, Dict
from config import weather_token

from main import *
from utils.helpers import get_weather_text, translator
import database
import requests
import random


router = Router()


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    await bot.send_sticker(message.from_user.id, 
                           sticker="CAACAgIAAxkBAAELGvxlmZRxjdh1xqYaaOPXCNTOjsVp1QAC8iwAAnDW4UuITBkIiCOD3zQE")
    await message.answer(f"Привіт, <b>{message.from_user.first_name}!</b>\n\n"
                         f"Цей бот допоможе тобі обрати книгу\nдля гарного проведення дoзвілля,\n"
                         f"а також розповість погоду у будь-якому куточку світу\n\n", reply_markup=reply.main_kb)
    await message.delete()
    

@router.message(F.text.lower() == "картинка")
async def images(message: Message, bot: Bot):
        images = await get_json("img.json")
        image = random.choice(images)
        await bot.send_photo(message.from_user.id, photo=image)


@router.message(F.text.lower() == "назва міста")
async def weather_by_city(message: Message, bot: Bot, state: FSMContext):
        await state.set_state(Weather_by_city.city)
        send_msg = await message.answer("Вкажіть назву міста...")
        msg_id = send_msg.message_id
        await asyncio.sleep(5)
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)


@router.message(Weather_by_city.city)
async def city_name(message: Message, state: FSMContext):
    data = await state.update_data(city=message.text)
    await state.clear()
    await show_weather(message=message, data=data)        


@router.message(F.location)
async def weather_by_location(message: Message):
    weather_by_location = {}
    weather_by_location["latitude"] = message.location.latitude
    weather_by_location["longitude"] = message.location.longitude
    await show_weather(message=message, data=weather_by_location)


@router.message(F.text.lower() == "рекомендована книга")
async def recommended_book(message: Message, state: FSMContext, bot: Bot):
    all_books = await database.get_books()
    books = [{"id": book[0], 'link': book[1], 'title': book[2], "author": book[3], "image": book[4], "description": book[5]} for book in all_books]

    book = random.choice(books)

    await state.update_data(book=book, state=Book.book)

    info_book = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_book_{book["id"]}")],
        [InlineKeyboardButton(text="Детальніше", url=book["link"])]
    ])

    await bot.send_photo(message.from_user.id, photo=book["image"], reply_markup=info_book)
    await message.answer(f"<b>{book["title"]}</b>\n\n<em>{book["author"]}</em>\n\n"
                        f"<b>Анотація:</b>\n\n{book["description"]}", reply_markup=reply.book_category)
    
    

@router.message(F.text.lower() == "збережені книги")
async def saved_book(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    data = await database.get_user_books(user_id)

    user_book_kb = InlineKeyboardMarkup(inline_keyboard=[
         [InlineKeyboardButton(text=book["title"], url=book["links"])]  for book in data
    ])
    
    await message.answer(f"<b>Ваші збережені книги!</b>", reply_markup=user_book_kb)
    await message.delete()


@router.message(F.text.lower() == "видалити книгу")
async def delete_book(message: Message):
    user_id = message.from_user.id
    data = await database.get_user_books(user_id)

    user_book_kb = InlineKeyboardMarkup(inline_keyboard=[
         [InlineKeyboardButton(text=book["title"], callback_data=f"delete_{book["id"]}")]  for book in data
    ])
    
    await message.answer("Натисніть на книгу, щоб видалити!", reply_markup=user_book_kb)
    
    

@router.message(F.text.lower() == "назад")
async def back_btn(message: Message):
    await message.answer("Ви повернулися у головне меню!", reply_markup=reply.main_kb)
    await message.delete()


async def show_weather(message: Message, data: Dict[str, Any]):
    try: 
        if "city" in data:
            city_name = translator(data["city"])

            resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_token}&units=metric")
            data = resp.json()
                
            text = await get_weather_text(data)
            await message.answer(text=text)

        else:
            lat = data["latitude"]
            lon = data["longitude"]

            resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}&units=metric")
            data = resp.json()

            text = await get_weather_text(data)
            await message.answer(text=text)

    except:
        await message.answer("Перевір назву міста або спробуй латиницею", reply_markup=reply.main_kb)
        await message.delete()

