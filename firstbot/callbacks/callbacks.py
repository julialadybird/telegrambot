from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import reply, inline
import random
import re
import database
from data import subloader


router = Router()

@router.callback_query(F.data == "books")
async def start_books(query: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text=f"Ви обрали Книги!", reply_markup=inline.book_category) 


@router.callback_query(F.data == "movies")
async def start_movies(query: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text=f"Оберіть категорію!", reply_markup=inline.film_category) 


@router.callback_query(F.data.startswith("delete_"))
async def del_book_or_film(query: CallbackQuery, bot: Bot):
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
async def save_to_user_books(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    book_id = re.findall(r'\d+', query.data)
    book_id = int(book_id[0])

    title = await database.save_to_user_books(user_id, book_id)

    if title:
        await bot.send_message(chat_id=query.from_user.id, text=f"Книгу {title} збережено!") 
    else:
        await bot.send_message(chat_id=query.from_user.id, text=f"Книга вже була збережена!")
    

@router.callback_query(F.data.startswith("save_movie_"))
async def save_to_user_films(query: CallbackQuery, bot: Bot):
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
    if data:
        user_book_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=book["title"], callback_data=f"show_book_{book['id']}")]  for book in data])
        
        await bot.send_message(query.from_user.id, text=f"<b>Збережені книги для {user_name}!</b>", reply_markup=user_book_kb)
    else:
        await bot.send_message(query.from_user.id, text=f"<b>У вас ще немає збережених книг!</b>")


@router.callback_query(F.data == "recommended")
async def book_recommendation(query: CallbackQuery, bot: Bot):
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
async def recommend_film(query: CallbackQuery, bot: Bot):
    film_search = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="...за жанром", callback_data=f"genres_{query.data}")],
        [InlineKeyboardButton(text="...з усіх", callback_data=f"all_films_{query.data}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])
    await bot.send_message(chat_id=query.from_user.id, text="Рекомендувати...", reply_markup=film_search)


@router.callback_query(F.data == "serials")
async def serial_recommendation(query: CallbackQuery, bot: Bot):
    film_search = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="...за жанром", callback_data=f"genres_{query.data}")],
        [InlineKeyboardButton(text="...з усіх", callback_data=f"all_films_{query.data}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])
    await bot.send_message(chat_id=query.from_user.id, text="Рекомендувати...", reply_markup=film_search)


@router.callback_query(F.data.startswith("all_films_"))
async def film_recommendation(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    data = (query.data).split('_')
    type_of = data[2]
    user_films = await database.show_user_films(user_id, type_of)

    all_movies = await database.get_movies(f"{type_of}")
    all_movies = [movie for movie in all_movies if not movie in user_films]
    
    movie = random.choice(all_movies)
        
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (movie['title'])))]
    

    info_film = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_movie_{type_of}_{movie['id']}")],
        [InlineKeyboardButton(text="Детальніше", url=movie['link'])]])

    if type_of == "films":
        await bot.send_photo(chat_id=query.from_user.id, photo=movie["poster"], reply_markup=info_film)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                            f"<b>Рік:</b> {title[1]}\n\n"
                            f"<b>Режисер:</b> <em>{movie['director']}</em>\n\n"
                            f"<b>IMDb: {movie['imdb']}</b>\n\n"
                            f"<b>Сюжет:</b>\n{movie['description']}", reply_markup=inline.film_more)
    elif type_of == "serials":
        await bot.send_photo(chat_id=query.from_user.id, photo=movie["poster"], reply_markup=info_film)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                            f"<b>Рік:</b> {title[1]}\n\n"
                            f"<b>Режисер:</b> <em>{movie['director']}</em>\n\n"
                            f"<b>IMDb: {movie['imdb']}</b>\n\n"
                            f"<b>Сюжет:</b>\n{movie['description']}", reply_markup=inline.serial_more)
    

@router.callback_query(F.data.startswith("genres_"))
async def genre_list(query: CallbackQuery, bot: Bot):
    data = (query.data).split('_')
    type_of = data[1]
    
    all_genres = await subloader.get_json('genres.json')

    film_genres = InlineKeyboardBuilder()
    for genre in all_genres:
        film_genres.button(text=genre, callback_data=f"{type_of}_{genre}")
        film_genres.adjust(2)
    
    await bot.send_message(chat_id=query.from_user.id, text=f"Оберіть жанр!", reply_markup=film_genres.as_markup()) 


@router.callback_query(F.data.startswith("films_") | F.data.startswith("serials_"))
async def genre_recommendation(query: CallbackQuery, bot: Bot):
    data = (query.data).split('_')
    type_of = data[0]
    genre = data[1]

    all_movies = await database.get_movies(f"{type_of}")
    films = [dict(film) for film in all_movies if genre in film['genres']]

    movie = random.choice(films)
        
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (movie['title'])))]
    
    info_film = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Зберегти", callback_data=f"save_movie_{type_of}_{movie['id']}")],
        [InlineKeyboardButton(text="Детальніше", url=movie['link'])]
    ])
    if type_of == "films":
        await bot.send_photo(chat_id=query.from_user.id, photo=movie["poster"], reply_markup=info_film)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                            f"<b>Рік:</b> {title[1]}\n\n"
                            f"<b>Режисер:</b> <em>{movie['director']}</em>\n\n"
                            f"<b>IMDb: {movie['imdb']}</b>\n\n"
                            f"<b>Сюжет:</b>\n{movie['description']}", reply_markup=inline.film_more)
    elif type_of == "serials":
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
         [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_book_{book['id']}")],
         [InlineKeyboardButton(text="Детальніше", url=book['links'])]
        ])

    await bot.send_photo(query.from_user.id, photo=book["image"], reply_markup=del_book)
    await bot.send_message(query.from_user.id, text=f"<b>{book['title']} ({book['author']})</b>\n\n<em>{book['author']}</em>\n\n"
                           f"<b>Анотація:</b>\n\n{book['description']}", reply_markup=inline.book_more)


@router.callback_query(F.data.startswith("show_"))
async def all_saved_films(query: CallbackQuery, bot: Bot):
    user_id = query.from_user.id
    text = query.data.split('_')
    type_of = text[1]

    user_films = await database.show_user_films(user_id, type_of)

    if user_films:
        film_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=film["title"], callback_data=f"about_{type_of}_{film['id']}")]  for film in user_films])
        
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>Збережене кіно!</b>", reply_markup=film_kb)
    else:
        if type_of == "films":
            await bot.send_message(query.from_user.id, text=f"<b>У вас ще немає збереженого кіно!</b>")
        elif type_of == "serials":
            await bot.send_message(query.from_user.id, text=f"<b>У вас ще немає збережених серіалів!</b>")
            


@router.callback_query(F.data.startswith("about_"))
async def about_film(query: CallbackQuery, bot: Bot):
    movie = query.data.split('_')
    type_of = movie[1]
    film_id = movie[2]

    film = await database.show_film(film_id, type_of)
    title = [text.strip() for text in (re.split(r'(\(.*?\))', (film['title'])))]

    if type_of == "films":
        del_film = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_films_{film['id']}")],
            [InlineKeyboardButton(text="Детальніше", url=film['link'])]
            ])
        
        await bot.send_photo(chat_id=query.from_user.id, photo=film["poster"], reply_markup=del_film)
        await bot.send_message(chat_id=query.from_user.id, text=f"<b>{title[0]}</b>\n(<em>{title[2]}</em>)\n\n"
                                f"<b>Рік:</b> {title[1]}\n\n"
                                f"<b>Режисер:</b> <em>{film['director']}</em>\n\n"
                                f"<b>IMDb: {film['imdb']}</b>\n\n"
                                f"<b>Сюжет:</b>\n{film['description']}", reply_markup=inline.film_more)

    elif type_of == "serials":
        del_serial = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Видалити зі збереженого", callback_data=f"delete_serials_{film['id']}")],
            [InlineKeyboardButton(text="Детальніше", url=film['link'])]
            ])

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