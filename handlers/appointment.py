import datetime

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from filters.date_filter import DateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.text import Text
from states.appointment import AppointmentState
from utils.db_queries import *
from keyboards.management import get_main_management_panel, get_trainers_kb, get_select_month_kb, get_cancel_training_kb
from filters.user_filter import TrainerExistsFilter
from main import bot
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
        await message.reply(f"Напишите дату, на которую хотите изменить запись в месяце {current_date.strftime('%B')}", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AppointmentState.choosing_appointment_date)
    if 'Следующий месяц' in message.text:
        next_month = current_date + datetime.timedelta(days=31)
        await state.update_data(year=next_month.year)
        await state.update_data(month=next_month.month)
        create_empty_appointments(next_month.year, next_month.month)
        await message.reply(f"Напишите дату, на которую хотите изменить запись в месяце {next_month.strftime('%B')}", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AppointmentState.choosing_appointment_date)


@router.message(AppointmentState.choosing_appointment_date, DateFilter())
async def select_time(message: Message, state: FSMContext):
    user_data = await state.get_data()
    year = user_data["year"]
    month = user_data["month"]
    day = int(message.text)
    await state.update_data(day=day)
    await message.reply("Введите время, на которое хотите изменить запись клиента")
    await state.set_state(AppointmentState.choosing_appointment_time)


@router.message(AppointmentState.choosing_appointment_date)
async def show_wrong_month_message(message: Message):
    await message.reply("Данные введены некорректо. Введите дату (число от 1 до 31)")


@router.message(AppointmentState.choosing_appointment_time, lambda m: match(r"[0-9][0-9]:[0-9][0-9]", m.text))
async def choose_client(message: Message, state: FSMContext):
    await state.update_data(hour=int(message.text[:2]))
    await state.update_data(minutes=int(message.text[3:]))
    user_data = await state.get_data()
    if not is_appointment_empty(datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"], user_data["minutes"])):
        await message.reply("<b>На данное время уже есть запись! Если хотите записать другого клиента, то введите его имя. Если хотите убрать запись, то воспользуйтесь соответствующей кнопкой</b>", reply_markup=get_cancel_training_kb())
    else:
        await message.reply("Выберите клиента на время")
    await state.set_state(AppointmentState.choosing_client_name)


@router.message(AppointmentState.choosing_appointment_time)
async def show_wrong_client_message(message: Message):
    await message.reply("Данные введены неправильно. Воспользуйтесь кнопками")


@router.message(AppointmentState.choosing_client_name, Text(text="Убрать клиента"))
async def remove_client(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"], user_data["minutes"])
    set_empty_appointment(date)
    await message.reply("Клиент убран с записи", reply_markup=get_main_management_panel())
    await state.clear()


@router.message(AppointmentState.choosing_client_name)
async def choose_trainer(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.reply("Выберите тренера", reply_markup=get_trainers_kb())
    await state.set_state(AppointmentState.choosing_trainer_name)


@router.message(AppointmentState.choosing_client_name)
async def show_wrong_trainer(message: Message):
    await message.reply("Такого клиента пока не существует. Сначала создайте его в разделе \"Добавить клиента\" или выберите из имеющихся")


@router.message(AppointmentState.choosing_trainer_name, TrainerExistsFilter())
async def create_appointment(message: Message, state: FSMContext):
    trainer = get_trainer_by_name(message.text)
    user_data = await state.get_data()
    client_name = user_data["client_name"]
    year = user_data["year"]
    month = user_data["month"]
    day = user_data["day"]
    hour = user_data["hour"]
    minutes = user_data["minutes"]
    date = datetime.datetime(year, month, day, hour, minutes)
    create_new_appointment(date, client_name, trainer.id)
    if trainer.chat_id != message.chat.id:
        await bot.send_message(trainer.chat_id, f"<b>Новая тренировка</b> \nКлиент: {client_name}\nВремя: {date.strftime('%d-%m-%y %H:%M')}")
    await message.reply(f"Клиент {client_name} записан к тренеру {trainer.name} на {date.strftime('%d-%m-%y %H:%M')}", reply_markup=get_main_management_panel())
    await state.clear()


@router.message(AppointmentState.choosing_trainer_name)
async def show_wrong_trainer(message: Message):
    await message.reply("Такого тренера не существует. Выберите из имеющихся")

