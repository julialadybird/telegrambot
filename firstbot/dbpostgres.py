import psycopg2
from data.subloader import get_json
import re


async def db_connect():
    db = psycopg2.connect(host="localhost",
                        dbname="booksandfilms",
                        user="postgres",
                        password="124578",
                        port=5432)
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS books("
                "id SERIAL PRIMARY KEY, "
                "links TEXT, "
                "title TEXT, "
                "author TEXT, "
                "image TEXT, "
                "description TEXT)")
    
    
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id SERIAL PRIMARY KEY, "
                "user_id TEXT, "
                "user_name TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS user_books("
                "user_id TEXT, "
                "book_id TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS films("
                "id SERIAL PRIMARY KEY, "
                "title TEXT, "
                "director TEXT, "
                "description TEXT, "
                "genres TEXT, "
                "imdb TEXT, "
                "poster TEXT, "
                "link TEXT)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS serials("
                "id SERIAL PRIMARY KEY,"
                "title TEXT, "
                "director TEXT, "
                "description TEXT, "
                "genres TEXT, "
                "imdb TEXT, "
                "poster TEXT, "
                "link TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS user_films("
                "user_id TEXT, "
                "film_id TEXT, "
                "type TEXT)")
    
    
    db.commit()

    return cur, db

async def insert_books():
    cur, db = await db_connect()
    books = await get_json("books.json")
   
    for book in books:
        cur.execute("INSERT INTO books(links, title, author, image, description)"
                    "VALUES (%s, %s, %s, %s, %s)", (book["link"], book["title"], book["author"], book["image"], book["description"]))

    db.commit()
    db.close()


async def insert_movies():
    cur, db = await db_connect()
    movies = await get_json("movies.json")
    serials = await get_json("serials.json")
   
    for movie in movies:
        movie["genres"] = ', '.join(item for item in movie["genres"])
        cur.execute("INSERT INTO films(title, director, description, genres, imdb, poster, link)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", (movie["title"], movie["director"], movie["description"], movie["genres"], movie["imdb"], movie["poster"], movie["link"]))
    
    for serial in serials:
        serial["genres"] = ', '.join(item for item in serial["genres"])
        cur.execute("INSERT INTO serials(title, director, description, genres, imdb, poster, link)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", (serial["title"], serial["director"], serial["description"], serial["genres"], serial["imdb"], serial["poster"], serial["link"]))
    
    db.commit()
    db.close()


async def get_books():
    cur, db = await db_connect()
    
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    db.close()
    return books


async def get_movies(table):
    cur, db = await db_connect()
    
    cur.execute(f"SELECT * FROM {table}")
    movies = cur.fetchall()

    db.close()
    return movies


async def get_user_books(user_id):
    cur, db = await db_connect()

    all_books = cur.execute("SELECT book_id FROM user_books WHERE user_id == ?", (user_id, )).fetchall()
    books = [int(i[0]) for i in all_books]

    user_books = []

    for book_id in books:
        cur.execute("SELECT * FROM books WHERE id == ?", (book_id, ))
        user_book = cur.fetchone()
        user_books.append(dict(user_book))
    
    db.close()
    return user_books


async def show_user_films(user_id, type_of):
    cur, db = await db_connect()

    all_films = cur.execute("SELECT film_id FROM user_films WHERE user_id == ? AND type == ?", (user_id, type_of)).fetchall()
    films = [int(i[0]) for i in all_films]

    user_films = []

    for film_id in films:
        cur.execute(f"SELECT * FROM {type_of} WHERE id == ?", (film_id, ))
        user_film = cur.fetchone()
        user_films.append(dict(user_film))

    db.commit()
    db.close()
    return user_films


async def delete_book(user_id, book_id):
    cur, db = await db_connect()

    user_books = cur.execute("SELECT book_id FROM user_books WHERE user_id == ?", (user_id,)).fetchall()
    books = [int(i[0]) for i in user_books]
    
    if book_id in books:
        cur.execute("DELETE FROM user_books WHERE book_id == ? AND user_id == ?", (book_id, user_id))
        title = cur.execute("SELECT title FROM books WHERE id == ?", (book_id, )).fetchone()
        title = dict(title)

        db.commit()
        db.close()
        return title["title"]
    else:
        db.close()


async def delete_film(user_id, film_id, type_of):
    cur, db = await db_connect()

    user_films = cur.execute("SELECT film_id FROM user_films WHERE user_id == ? AND type == ?", (user_id, type_of)).fetchall()
    films = [int(i[0]) for i in user_films]
    
    if film_id in films:
        cur.execute("DELETE FROM user_films WHERE film_id == ? AND user_id == ? AND type == ?", (film_id, user_id, type_of))
        title = cur.execute(f"SELECT title FROM {type_of} WHERE id == ?", (film_id, )).fetchone()
        title = dict(title)

        db.commit()
        db.close()
        return title["title"]
    else:
        db.close()
   

async def save_to_user_books(user_id, book_id):
    cur, db = await db_connect()

    user_books = cur.execute("SELECT book_id FROM user_books WHERE user_id == ?", (user_id,)).fetchall()
    books = [int(i[0]) for i in user_books]

    if not book_id in books:
        cur.execute("INSERT INTO user_books(user_id, book_id)"
                    "VALUES (?, ?)", (user_id, book_id))
        title = cur.execute("SELECT title FROM books WHERE id == ?", (book_id, )).fetchone()
        title = dict(title)
        
        db.commit()
        db.close()
        return title["title"]

    else:
        db.close()
        return False


async def save_to_user_films(user_id, movie_id, type_of):
    cur, db = await db_connect()

    user_films = cur.execute("SELECT film_id FROM user_films WHERE user_id == ? AND type == ?", (user_id, type_of)).fetchall()
    films = [int(i[0]) for i in user_films]

    if not movie_id in films:
        cur.execute("INSERT INTO user_films(user_id, film_id, type)"
                    "VALUES (%s, %s, %s)", (user_id, movie_id, type_of))
        title = cur.execute(f"SELECT title FROM {type_of} WHERE id == ?", (movie_id, )).fetchone()
        title = dict(title)
        title = [text.strip() for text in (re.split(r'(\(.*?\))', (title['title'])))]

        db.commit()
        db.close()
        return title[0]

    else:
        db.close()
        return False
    

async def show_film(film_id, type_of):
    cur, db = await db_connect()

    film = cur.execute(f"SELECT * FROM {type_of} WHERE id == ?", (film_id, )).fetchone()
    film = dict(film)

    db.commit()
    db.close()
    return film

    
async def show_book(book_id):
    cur, db = await db_connect()

    book = cur.execute(f"SELECT * FROM books WHERE id == ?", (book_id, )).fetchone()
    book = dict(book)

    db.commit()
    db.close()
    return book