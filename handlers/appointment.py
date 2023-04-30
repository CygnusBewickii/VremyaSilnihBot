import datetime

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from filters.date_filter import DateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.text import Text
from states.appointment import AppointmentState
from utils.db_queries import *
from keyboards.management import get_clients_kb, get_main_management_panel, get_trainers_kb, get_select_time_kb, get_select_month_kb
from filters.user_filter import TrainerExistsFilter, ClientExistsFilter
from re import match

router = Router()

@router.message(Text(text="Изменение записей", ignore_case=True))
async def make_appointment(message: Message):
    await message.reply('Выберите месяц', reply_markup=get_select_month_kb())

@router.message(lambda m: ('Этот месяц' in m.text) or ('Следующий месяц' in m.text))
async def select_date(message: Message, state: FSMContext):
    current_date = datetime.date.today()
    if 'Этот месяц' in message.text:
        await state.update_data(year=current_date.year)
        await state.update_data(month=current_date.month)
        create_empty_appointments(current_date.year, current_date.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {current_date.strftime('%B')}", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AppointmentState.choosing_appointment_date)
    if 'Следующий месяц' in message.text:
        next_month = current_date + datetime.timedelta(days=31)
        await state.update_data(year=next_month.year)
        await state.update_data(month=next_month.month)
        create_empty_appointments(next_month.year, next_month.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {next_month.strftime('%B')}", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AppointmentState.choosing_appointment_date)


@router.message(AppointmentState.choosing_appointment_date, DateFilter())
async def select_time(message: Message, state: FSMContext):
    user_data = await state.get_data()
    year = user_data["year"]
    month = user_data["month"]
    day = int(message.text)
    await state.update_data(day=day)
    appointments = get_date_appointments(year, month, day)
    await message.reply("Выберите свободное время, на которое хотите записать клиента", reply_markup=get_select_time_kb(appointments))
    await state.set_state(AppointmentState.choosing_appointment_time)


@router.message(AppointmentState.choosing_appointment_date)
async def show_wrong_month_message(message: Message):
    await message.reply("Данные введены некорректо. Введите дату (число от 1 до 31)")


@router.message(AppointmentState.choosing_appointment_time, lambda m: match(r"[0-9][0-9]:00", m.text))
async def choose_client(message: Message, state: FSMContext):
    await state.update_data(hour=int(message.text[:2]))
    user_data = await state.get_data()
    date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"])
    await message.reply("Выберите клиента на время", reply_markup=get_clients_kb(is_appointment_empty(date)))
    await state.set_state(AppointmentState.choosing_client_name)


@router.message(AppointmentState.choosing_appointment_time)
async def show_wrong_client_message(message: Message):
    await message.reply("Данные введены неправильно. Воспользуйтесь кнопками")


@router.message(AppointmentState.choosing_client_name, ClientExistsFilter())
async def choose_trainer(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.reply("Выберите тренера", reply_markup=get_trainers_kb())
    await state.set_state(AppointmentState.choosing_trainer_name)

@router.message(AppointmentState.choosing_client_name, Text(text="Убрать клиента"))
async def remove_client(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"])
    set_empty_appointment(date)
    await message.reply("Клиент убран с записи", reply_markup=get_main_management_panel())
    await state.clear()


@router.message(AppointmentState.choosing_client_name)
async def show_wrong_trainer(message: Message):
    await message.reply("Такого клиента пока не существует. Сначала создайте его в разделе \"Добавить клиента\" или выберите из имеющихся")


@router.message(AppointmentState.choosing_trainer_name, TrainerExistsFilter())
async def create_appointment(message: Message, state: FSMContext):
    trainer = get_trainer_by_name(message.text)
    user_data = await state.get_data()
    client_name = user_data["client_name"]
    client = get_client_by_name(client_name)
    year = user_data["year"]
    month = user_data["month"]
    day = user_data["day"]
    hour = user_data["hour"]
    date = datetime.datetime(year, month, day, hour)
    create_new_appointment(date, client.id, trainer.id)
    await message.reply(f"Клиент {client.name} записан к тренеру {trainer.name} на {date.strftime('%d-%m-%y %H:%M')}", reply_markup=get_main_management_panel())
    await state.clear()


@router.message(AppointmentState.choosing_trainer_name)
async def show_wrong_trainer(message: Message):
    await message.reply("Такого тренера не существует. Выберите из имеющихся")

