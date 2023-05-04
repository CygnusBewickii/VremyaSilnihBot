import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from utils.db_queries import get_trainers, is_user_admin

def get_main_management_panel(username: str) -> ReplyKeyboardMarkup:
    is_admin = is_user_admin(username)
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменение записей")
    kb.button(text="Расписание на неделю")
    if is_admin:
        kb.button(text="Добавить нового тренера")
        kb.button(text="Система постоянных клиентов")
    kb.adjust(1, 2)
    return kb.as_markup(resize_keyboard=True)

def get_select_month_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Этот месяц ({datetime.date.today().strftime('%B')})")
    kb.button(text=f"Следующий месяц ({(datetime.date.today() + datetime.timedelta(days=31)).strftime('%B')})")
    return kb.as_markup(resize_keyboard=True)

def get_cancel_training_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Убрать клиента")
    return kb.as_markup(resize_keyboard=True)

def get_trainers_kb() -> ReplyKeyboardMarkup:
    trainers = get_trainers()
    kb = ReplyKeyboardBuilder()
    for trainer in trainers:
        kb.button(text=trainer.name)
    return kb.as_markup(resize_keyboard=True)

def get_roles_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Администратор")
    kb.button(text="Тренер")
    return kb.as_markup(resize_keyboard=True)

def get_regular_clients_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить клиента")
    kb.button(text="Удалить клиента")
    return kb.as_markup(resize_keyboard=True)

def get_choose_regular_appointments_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="ПН", callback_data="choose_day")
    builder.button(text="ВТ", callback_data="choose_day")
    builder.button(text="СР", callback_data="choose_day")
    builder.button(text="ЧТ", callback_data="choose_day")
    builder.button(text="ПТ", callback_data="choose_day")
    builder.button(text="СБ", callback_data="choose_day")
    builder.button(text="ВС", callback_data="choose_day")
    builder.button(text="Продолжить", callback_data="accept")
    builder.adjust(7, 1)
    return builder.as_markup()

