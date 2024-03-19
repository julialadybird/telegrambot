from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import reply, inline
import random
import re
import database


router = Router()

# @router.callback_query()
# async def start_category(query: CallbackQuery, bot: Bot):
#     if query.data == "books":
#         await bot.send_message(chat_id=query.from_user.id, text=f"Ви обрали Книги!", reply_markup=inline.book_category) 

#     elif query.data == "movies":
#         await bot.send_message(chat_id=query.from_user.id, text=f"Оберіть категорію!", reply_markup=inline.film_category) 


@router.callback_query(F.data.startswith("delete_"))
async def callback_del_book(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    call = query.data.split('_')

    if call[1] == "book":
        book_id = int(call[2])
        title = await database.delete_book(user_id, book_id)

        if title:
            await bot.send_message(chat_id=query.from_user.id, text=f"Книгу {title} видалено!") 
        else:
            await bot.send_message(chat_id=query.from_user.id, text=f"Книгу вже було видалено!")
    
    else:
        film_id = int(call[2])
        type_of = call[1]

        title = await database.delete_film(user_id, film_id, type_of)

        if title:
            await bot.send_message(chat_id=query.from_user.id, text=f"Кіно {title} видалено!") 
        else:
            await bot.send_message(chat_id=query.from_user.id, text=f"Кіно вже було видалено!")


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
    

@router.callback_query(F.data.startswith("save_movie_"))
async def callback_save_films(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    movie = query.data.split('_')
    movie_id = int(movie[3])
    type_of = movie[2]
    
    title = await database.save_to_user_films(user_id, movie_id, type_of)

    if title:
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title}</b> збережено!") 
    else:
        await bot.send_message(chat_id=query.from_user.id, text=f"Кіно вже у збережених!")


@router.callback_query(F.data == "saved")
async def books_saved(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    data = await database.get_user_books(user_id)

    user_book_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=book["title"], callback_data=f"show_book_{book['id']}")]  for book in data])
    
    await bot.send_message(query.from_user.id, text=f"<b>Збережені книги для {user_name}!</b>", reply_markup=user_book_kb)


@router.callback_query(F.data == "recommended")
async def book_recommended(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    data = await database.get_user_books(user_id)
   
    all_books = await database.get_books()

    all_books = [{"id": book[0], "links": book[1], "title": book[2], "author": book[3], "image": book[4], "description": book[5]} for book in all_books]
    books =[book for book in all_books if not book in data]
        
    
    book = random.choice(books)

    info_book = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_book_{book['id']}")],
        [InlineKeyboardButton(text="Детальніше", url=book['links'])]
    ])

    await bot.send_photo(query.from_user.id, photo=book["image"], reply_markup=info_book)
    await bot.send_message(query.from_user.id, text=f"<b>{book['title']}</b>\n\n<em>{book['author']}</em>\n\n"
                           f"<b>Анотація:</b>\n\n{book['description']}", reply_markup=inline.book_more)


@router.callback_query(F.data == "films")
async def recommend_films(query: CallbackQuery, bot: Bot):
    all_movies = await database.get_movies("films")
    
    movie = random.choice(all_movies)
        
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (movie['title'])))]
    

    info_film = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_movie_films_{movie['id']}")],
        [InlineKeyboardButton(text="Детальніше", url=movie['link'])]])

    await bot.send_photo(chat_id=query.from_user.id, photo=movie["poster"], reply_markup=info_film)
    await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                            f"<b>Рік:</b> {title[1]}\n\n"
                            f"<b>Режисер:</b> <em>{movie['director']}</em>\n\n"
                            f"<b>IMDb: {movie['imdb']}</b>\n\n"
                            f"<b>Сюжет:</b>\n{movie['description']}", reply_markup=inline.film_more)
    
        
@router.callback_query(F.data == "serials")
async def recommend_serial(query: CallbackQuery, bot: Bot): 
    all_movies = await database.get_movies("serials")
    
    movie = random.choice(all_movies)
        
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (movie['title'])))]
    
    info_film = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_movie_serials_{movie['id']}")],
        [InlineKeyboardButton(text="Детальніше", url=movie['link'])]
    ])

    await bot.send_photo(chat_id=query.from_user.id, photo=movie["poster"], reply_markup=info_film)
    await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                            f"<b>Рік:</b> {title[1]}\n\n"
                            f"<b>Режисер:</b> <em>{movie['director']}</em>\n\n"
                            f"<b>IMDb: {movie['imdb']}</b>\n\n"
                            f"<b>Сюжет:</b>\n{movie['description']}", reply_markup=inline.serial_more)


@router.callback_query(F.data.startswith("show_book"))
async def show_book(query: CallbackQuery, bot: Bot):
    text = query.data.split('_')
    book_id = text[2]

    book = await database.show_book(book_id)

    del_book = InlineKeyboardMarkup(inline_keyboard=[
         [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_book_{book['id']}")]])

    await bot.send_photo(query.from_user.id, photo=book["image"], reply_markup=del_book)
    await bot.send_message(query.from_user.id, text=f"<b>{book['title']}</b>\n\n<em>{book['author']}</em>\n\n"
                           f"<b>Анотація:</b>\n\n{book['description']}", reply_markup=inline.book_more)


@router.callback_query(F.data.startswith("show_"))
async def all_saved_films(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    text = query.data.split('_')
    type_of = text[1]

    user_films = await database.show_user_films(user_id, type_of)

    film_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=film["title"], callback_data=f"about_{type_of}_{film['id']}")]  for film in user_films])
    
    await bot.send_message(chat_id=query.from_user.id, text=f"<b>Збережене кіно!</b>", reply_markup=film_kb)


@router.callback_query(F.data.startswith("about_"))
async def about_film(query: CallbackQuery, bot: Bot):
    movie = query.data.split('_')
    type_of = movie[1]
    film_id = movie[2]

    film = await database.show_film(film_id, type_of)
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (film['title'])))]

    if type_of == "films":
        del_film = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_films_{film['id']}")]])
        
        await bot.send_photo(chat_id=query.from_user.id, photo=film["poster"], reply_markup=del_film)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                                f"<b>Рік:</b> {title[1]}\n\n"
                                f"<b>Режисер:</b> <em>{film['director']}</em>\n\n"
                                f"<b>IMDb: {film['imdb']}</b>\n\n"
                                f"<b>Сюжет:</b>\n{film['description']}", reply_markup=inline.film_more)

    elif type_of == "serials":
        del_serial = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_serials_{film['id']}")]])

        await bot.send_photo(chat_id=query.from_user.id, photo=film["poster"], reply_markup=del_serial)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                                f"<b>Рік:</b> {title[1]}\n\n"
                                f"<b>Режисер:</b> <em>{film['director']}</em>\n\n"
                                f"<b>IMDb: {film['imdb']}</b>\n\n"
                                f"<b>Сюжет:</b>\n{film['description']}", reply_markup=inline.serial_more)



@router.callback_query(F.data == "back_films")
async def back_films(query: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Категорія Кіно!", reply_markup=inline.film_category)

@router.callback_query(F.data == "back_book")
async def back_books(query: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Категорія Книги!", reply_markup=inline.book_category)

@router.callback_query(F.data == "back")
async def back(query: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Головне меню!", reply_markup=reply.main_kb)