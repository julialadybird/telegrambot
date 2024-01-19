from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardRemove
                   

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Images"),
            KeyboardButton(text="Links")
        ],
        [
            KeyboardButton(text="Calc"),
            KeyboardButton(text="Special")
        ]
    ],
    resize_keyboard=True, #дозволяє зробити кнопки менші, адаптувати до клавіатури 
    one_time_keyboard=True, #буде приховуватися до наступного викор
    input_field_placeholder="Choose an action from menu",
    selective=True
)

special_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Your location", request_location=True),
            KeyboardButton(text="Contact", request_contact=True),
            KeyboardButton(text="Poll",request_poll=KeyboardButtonPollType())
        ],
        [
            KeyboardButton(text="Back")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

rmk = ReplyKeyboardRemove()