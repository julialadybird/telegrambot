from aiogram import Router, F, Bot
from aiogram.types import Message
from keyboards import reply, inline, builders
from data.subloader import get_json
import random 

router = Router()


@router.message(F.text.lower() == "hello")
async def send_heart(message: Message):
    await message.answer("❤️")


@router.message()
async def echo(message: Message, bot: Bot):
    msg = message.text.lower()
    images = await get_json("img.json")

    if msg == "links":
        await message.answer("Your links: ", reply_markup=inline.links_kb)

    elif msg == "special":
        await message.answer("Special: ", reply_markup=reply.special_kb)

    elif msg == "calc":
        await message.answer("Calc: ", reply_markup=builders.calc_kb())

    elif msg == "images":
        image = random.choice(images)
        await bot.send_photo(message.from_user.id, photo=image)
