from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
                   

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Книги")
        ],
        [
            KeyboardButton(text="Кіно")
        ]
    ],
    resize_keyboard=True, #дозволяє зробити кнопки менші, адаптувати до клавіатури 
    one_time_keyboard=True, #буде приховуватися до наступного викор
    input_field_placeholder="Оберіть категорію",
    selective=True
)

rmk = ReplyKeyboardRemove()