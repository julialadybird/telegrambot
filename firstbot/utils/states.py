from aiogram.fsm.state import StatesGroup, State


class Weather_by_city(StatesGroup):
    city = State()


class Book(StatesGroup):
    book = State()