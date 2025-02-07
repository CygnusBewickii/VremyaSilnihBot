import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from utils.db_queries import get_trainers, is_user_admin, get_regular_clients, get_regular_appointments_by_client, \
    get_regular_clients_for_trainer, get_regular_clients_appointment_for_trainer

def get_main_management_panel(username: str) -> ReplyKeyboardMarkup:
    is_admin = is_user_admin(username)
    kb = ReplyKeyboardBuilder()
    kb.button(text="Расписание на неделю")
    kb.button(text="Изменение записей")
    kb.button(text="Система постоянных клиентов")
    if is_admin:
        kb.button(text="Тренеры")
    kb.adjust(1)
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
    kb.button(text="Добавить постоянную запись")
    kb.button(text="Удалить постоянную запись")
    kb.button(text="Удалить клиента")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_regular_client_appointments_kb(trainer_username: str, client_name: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    regular_appointments = get_regular_appointments_by_client(client_name) if is_user_admin(trainer_username) \
        else get_regular_clients_appointment_for_trainer(trainer_username, client_name)
    for appointment in regular_appointments:
        days = {
            1: "Пн",
            2: "Вт",
            3: "Ср",
            4: "Чт",
            5: "Пт",
            6: "Сб",
            0: "Вс"
        }
        kb.button(text=f'{days[appointment.week_day_num]} {appointment.time}')
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
    kb.button(text="Утвердить записи")
    kb.adjust(7)
    return kb.as_markup(resize_keyboard=True)


def get_regular_clients_kb(trainer_username: str):
    kb = ReplyKeyboardBuilder()
    if is_user_admin(trainer_username):
        regular_clients = get_regular_clients()
        for client in regular_clients:
            kb.button(text=client.name)
    else:
        regular_clients = get_regular_clients_for_trainer(trainer_username)
        client_names = set()
        for client in regular_clients:
            client_names.add(client.name)
        for client_name in client_names:
            kb.button(text=client_name)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)