from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
                   

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Погода")
        ],
        [
            KeyboardButton(text="Книги")
        ]
    ],
    resize_keyboard=True, #дозволяє зробити кнопки менші, адаптувати до клавіатури 
    one_time_keyboard=True, #буде приховуватися до наступного викор
    input_field_placeholder="Оберіть категорію",
    selective=True
)

weather_category = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назва міста")
        ],
        [
            KeyboardButton(text="Координати", request_location=True)
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True, #дозволяє зробити кнопки менші, адаптувати до клавіатури 
    one_time_keyboard=True, #буде приховуватися до наступного викор
    input_field_placeholder="Оберіть категорію",
    selective=True
)

book_category = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рекомендована книга")
        ],
        [
            KeyboardButton(text="Збережені книги")
        ],
        [
            KeyboardButton(text="Видалити книгу")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True, #дозволяє зробити кнопки менші, адаптувати до клавіатури 
    one_time_keyboard=True, #буде приховуватися до наступного викор
    input_field_placeholder="Оберіть категорію",
    selective=True
)

rmk = ReplyKeyboardRemove()