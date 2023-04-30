import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from models import Appointment
from utils.db_queries import get_clients, get_trainers

def get_main_management_panel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменение записей")
    kb.button(text="Расписание на неделю")
    kb.button(text="Добавить клиента")
    kb.adjust(1, 2)
    return kb.as_markup(resize_keyboard=True)

def get_select_month_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Этот месяц ({datetime.date.today().strftime('%B')})")
    kb.button(text=f"Следующий месяц ({(datetime.date.today() + datetime.timedelta(days=31)).strftime('%B')})")
    return kb.as_markup(resize_keyboard=True)

def get_select_time_kb(appointments: [Appointment]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for appointment in appointments:
        time: datetime.datetime
        kb.button(text=appointment.date.strftime("%H:%M") + f'({"свободно" if appointment.client_id == None else "Занято"})')
    kb.adjust(4, 4, 4, 4)
    return kb.as_markup(resize_keyboard=True)

def get_clients_kb(is_appointment_empty: bool) -> ReplyKeyboardMarkup:
    clients = get_clients()
    kb = ReplyKeyboardBuilder()
    if not is_appointment_empty:
        kb.button(text="Убрать клиента")
    for client in clients:
        kb.button(text=client.name)
    return kb.as_markup(resize_keyboard=True)

def get_trainers_kb() -> ReplyKeyboardMarkup:
    trainers = get_trainers()
    kb = ReplyKeyboardBuilder()
    for trainer in trainers:
        kb.button(text=trainer.name)
    return kb.as_markup(resize_keyboard=True)


