import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from models import Appointment
from utils.db_queries import get_clients

def get_main_management_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Записать клиента")
    kb.button(text="Расписание на неделю")
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)

def get_select_month_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Этот месяц ({datetime.date.today().strftime('%B')})")
    kb.button(text=f"Следующий месяц ({(datetime.date.today() + datetime.timedelta(days=31)).strftime('%B')})")
    return kb.as_markup(resize_keyboard=True)

def get_select_free_time_kb(free_time: [Appointment]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for appointment in free_time:
        time: datetime.datetime
        kb.button(text=appointment.date.strftime("%H:%M"))
    return kb.as_markup(resize_keyboard=True)

def get_clients_kb() -> ReplyKeyboardMarkup:
    clients = get_clients()
    print(clients)
    kb = ReplyKeyboardBuilder()
    for client in clients:
        kb.button(text=client.name)
    return kb.as_markup(resize_keyboard=True)