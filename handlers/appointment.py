import datetime

from aiogram import Router
from aiogram.types import Message
from filters.date_filter import DateFilter
from aiogram.fsm.context import FSMContext
from states.appointment import Appointment as AppointmentState
from utils.db_queries import get_date_free_time, create_new_appointment, get_client_by_name
from keyboards.management import get_select_free_time_kb, get_clients_kb
from filters.user_filter import UserExistsFilter
from re import match

router = Router()

@router.message(lambda m: ('Этот месяц' in m.text) or ('Следующий месяц' in m.text))
async def select_date(message: Message, state: FSMContext):
    current_date = datetime.date.today()
    if 'Этот месяц' in message.text:
        await state.update_data(year=current_date.year)
        await state.update_data(month=current_date.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {current_date.strftime('%B')}")
        await state.set_state(AppointmentState.choosing_appointment_date)
    if 'Следующий месяц' in message.text:
        next_month = current_date + datetime.timedelta(days=31)
        await state.update_data(year=next_month.year)
        await state.update_data(month=next_month.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {next_month.strftime('%B')}")
        await state.set_state(AppointmentState.choosing_appointment_date)

@router.message(AppointmentState.choosing_appointment_date, DateFilter())
async def select_time(message: Message, state: FSMContext):
    user_data = await state.get_data()
    year = user_data["year"]
    month = user_data["month"]
    day = int(message.text)
    await state.update_data(day=day)
    free_time = get_date_free_time(year, month, day)
    await message.reply("Выберите свободное время, на которое хотите записать клиента", reply_markup=get_select_free_time_kb(free_time))
    await state.set_state(AppointmentState.choosing_appointment_time)

@router.message(AppointmentState.choosing_appointment_date)
async def show_wrong_month_message(message: Message):
    await message.reply("Данные введены некорректо. Введите дату (число от 1 до 31)")

@router.message(AppointmentState.choosing_appointment_time, lambda m: match(r"[0-9][0-9]:00", m.text))
async def choose_client(message: Message, state: FSMContext):
    await state.update_data(hour=message.text[:2])
    await message.reply("Выберите клиента на время", reply_markup=get_clients_kb())
    await state.set_state(AppointmentState.choosing_client_name)

@router.message(AppointmentState.choosing_appointment_time)
async def show_wrong_client_message(message: Message):
    await message.reply("Данные введены неправильно. Воспользуйтесь кнопками")

@router.message(AppointmentState.choosing_client_name, UserExistsFilter())
async def create_appointment(message: Message, state: FSMContext):
    client = get_client_by_name(message.text)
    user_data = await state.get_data()
    year = user_data["year"]
    month = user_data["month"]
    day = user_data["day"]
    hour = user_data["hour"]
    date = datetime.datetime(year, month, day, hour)
    create_new_appointment(date, client.id, message.from_user.id)

