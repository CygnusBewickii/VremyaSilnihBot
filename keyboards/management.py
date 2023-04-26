from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def get_main_management_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Записать клиента")
    kb.button(text="Расписание на неделю")
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)