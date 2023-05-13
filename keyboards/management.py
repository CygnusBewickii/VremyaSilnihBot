import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from utils.db_queries import get_trainers, is_user_admin, get_regular_clients

def get_main_management_panel(username: str) -> ReplyKeyboardMarkup:
    is_admin = is_user_admin(username)
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменение записей")
    kb.button(text="Расписание на неделю")
    if is_admin:
        kb.button(text="Тренеры")
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

def get_trainers_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить нового тренера")
    kb.button(text="Удалить тренера")
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
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пн")
    kb.button(text="Вт")
    kb.button(text="Ср")
    kb.button(text="Чт")
    kb.button(text="Пт")
    kb.button(text="Сб")
    kb.button(text="Вс")
    kb.adjust(7)
    return kb.as_markup(resize_keyboard=True)


def get_regular_clients_kb():
    kb = ReplyKeyboardBuilder()
    regular_clients = get_regular_clients()
    for client in regular_clients:
        kb.button(text=client.name)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)