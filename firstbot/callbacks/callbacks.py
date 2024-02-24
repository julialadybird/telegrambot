from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import re
import database


router = Router()


# @router.callback_query(F.data == "save_book")
# async def callback_save_book(query: CallbackQuery, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     book = data["book"]
#     await state.clear()

#     print(book)

#     user_id = query.from_user.id
#     saved = await database.save_to_user_books(user_id, book)

#     if saved:
#         await bot.send_message(chat_id=query.from_user.id, text="Книгу збережено!") 
#     else:
#         await bot.send_message(chat_id=query.from_user.id, text="Книга вже була збережена!")


@router.callback_query(F.data.startswith("delete_"))
async def callback_del_book(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    book_id = re.findall(r'\d+', query.data)
    book_id = int(book_id[0])

    title = await database.delete_book(user_id, book_id)
    await bot.send_message(chat_id=query.from_user.id, text=f"Книгу {title} видалено!") 
      
    
@router.callback_query(F.data.startswith("save_book_"))
async def callback_save_book(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    book_id = re.findall(r'\d+', query.data)
    book_id = int(book_id[0])

    title = await database.save_to_user_books(user_id, book_id)

    if title:
        await bot.send_message(chat_id=query.from_user.id, text=f"Книгу {title} збережено!") 
    else:
        await bot.send_message(chat_id=query.from_user.id, text=f"Книга вже була збережена!")
    
