import sqlite3
from data.subloader import get_json

async def db_connect():
    db = sqlite3.connect('db_books.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()


    cur.execute("CREATE TABLE IF NOT EXISTS books("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "links TEXT, "
                "title TEXT, "
                "author TEXT, "
                "image TEXT, "
                "description TEXT)")
    
    
    cur.execute("CREATE TABLE IF NOT EXISTS user("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "user_id TEXT, "
                "user_name TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS user_books("
                "user_id TEXT, "
                "book_id TEXT)")
    
    db.commit()

    return cur, db


async def insert_books():
    cur, db = await db_connect()
    books = await get_json("books.json")
   
    for book in books:
        cur.execute("INSERT INTO books(links, title, author, image, description)"
                    "VALUES (?, ?, ?, ?, ?)", (book["link"], book["title"], book["author"], book["image"], book["description"]))

    db.commit()
    db.close()


async def get_books():
    cur, db = await db_connect()
    
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    db.close()
    return books


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
        return False
   

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

    

    



