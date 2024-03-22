from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_category = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Книги", callback_data="books")],
        [InlineKeyboardButton(text="🎬 Кіно", callback_data="movies")]
        ])

book_category = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Рекомендована книга!", callback_data="recommended")],
        [InlineKeyboardButton(text="📚 Збережені книги!", callback_data="saved")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])

film_category = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Кінофільми", callback_data="films")],
        [InlineKeyboardButton(text="🍿 Серіали", callback_data="serials")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])

film_more = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Рекомендувати ще!", callback_data="films")],
        [InlineKeyboardButton(text="🎬 Показати збережені!", callback_data="show_films")],
        [InlineKeyboardButton(text="Назад", callback_data="back_films")]
        ])

serial_more = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Рекомендувати ще!", callback_data="serials")],
        [InlineKeyboardButton(text="🎬 Показати збережені!", callback_data="show_serials")],
        [InlineKeyboardButton(text="Назад", callback_data="back_films")]
        ])

book_more = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Рекомендувати ще!", callback_data="recommended")],
        [InlineKeyboardButton(text="Назад", callback_data="back_book")]
        ])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]
        ])
