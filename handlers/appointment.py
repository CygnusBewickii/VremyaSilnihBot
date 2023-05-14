import datetime

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from filters.date_filter import DateFilter, TimeFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.text import Text
from states.appointment import AppointmentState
from utils.db_queries import *
from utils.time import split_time
from keyboards.management import get_main_management_panel, get_trainers_kb, get_select_month_kb, get_cancel_training_kb
from filters.user_filter import TrainerExistsFilter
from filters.role_filter import IsUserAdmin
from main import bot

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
    day = int(message.text)
    await state.update_data(day=day)
    await message.reply("Введите время, на которое хотите изменить запись клиента")
    await state.set_state(AppointmentState.choosing_appointment_time)


@router.message(AppointmentState.choosing_appointment_date)
async def show_wrong_month_message(message: Message):
    await message.reply("Данные введены некорректо. Введите дату (число от 1 до 31)")


@router.message(AppointmentState.choosing_appointment_time, TimeFilter(), IsUserAdmin())
async def admin_choose_client(message: Message, state: FSMContext):
    splitted_time = split_time(message.text)
    await state.update_data(hour=int(splitted_time[0]))
    await state.update_data(minutes=int(splitted_time[1]))
    user_data = await state.get_data()
    appointment_date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"], user_data["minutes"])
    if not is_appointment_empty(appointment_date):
        appointment = get_appointment_by_datetime(appointment_date)
        trainer = get_trainer_by_id(appointment.trainer_id)
        if trainer.username == message.from_user.username:
            await message.reply("<b>На данное время у вас уже есть запись! Если хотите записать другого клиента, то введите его имя. Если хотите убрать запись, то воспользуйтесь соответствующей кнопкой</b>", reply_markup=get_cancel_training_kb())
        else:
            await message.reply(f"На данное время есть запись у {trainer.name}. Если хотите записать другого клиента, то введите его имя. Если хотите убрать запись, то воспользуйтесь соответствующей кнопкой", reply_markup=get_cancel_training_kb())
    else:
        await message.reply("Введите имя клиента")
    await state.set_state(AppointmentState.choosing_client_name)


@router.message(AppointmentState.choosing_appointment_time, TimeFilter())
async def trainer_choose_client(message: Message, state: FSMContext):
    splitted_time = split_time(message.text)
    await state.update_data(hour=int(splitted_time[0]))
    await state.update_data(minutes=int(splitted_time[1]))
    user_data = await state.get_data()
    appointment_date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"], user_data["minutes"])
    if not is_appointment_empty(appointment_date):
        appointment = get_appointment_by_datetime(appointment_date)
        trainer = get_trainer_by_id(appointment.trainer_id)
        if trainer.username == message.from_user.username:
            await message.reply("<b>На данное время у вас уже есть запись! Если хотите записать другого клиента, то введите его имя. Если хотите убрать запись, то воспользуйтесь соответствующей кнопкой</b>", reply_markup=get_cancel_training_kb())
            await state.set_state(AppointmentState.choosing_client_name)
        else:
            await message.reply(f"<b>На данное время есть запись у {trainer.name}. Изменить запись может только этот тренер или администратор. Выберите другое время</b>")
    else:
        await message.reply("Введите имя клиента")
        await state.set_state(AppointmentState.choosing_client_name)


@router.message(AppointmentState.choosing_appointment_time)
async def show_wrong_client_message(message: Message):
    await message.reply("Данные введены неправильно. Воспользуйтесь кнопками")


@router.message(AppointmentState.choosing_client_name, Text(text="Убрать клиента"))
async def remove_client(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = datetime.datetime(user_data["year"], user_data["month"], user_data["day"], user_data["hour"], user_data["minutes"])
    set_empty_appointment(date)
    await message.reply("Клиент убран с записи", reply_markup=get_main_management_panel(message.from_user.username))
    await state.clear()


@router.message(AppointmentState.choosing_client_name)
async def choose_trainer(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.reply("Выберите тренера", reply_markup=get_trainers_kb())
    await state.set_state(AppointmentState.choosing_trainer_name)


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
        try:
            await bot.send_message(trainer.chat_id, f"<b>Новая тренировка</b> \nКлиент: {client_name}\nВремя: {date.strftime('%d-%m-%y %H:%M')}")
        except:
            await message.answer("Не удалось отправить тренеру сообщение о тренировке. Возможно он не начал чат с ботом")
    await message.reply(f"Клиент {client_name} записан к тренеру {trainer.name} на {date.strftime('%d-%m-%y %H:%M')}", reply_markup=get_main_management_panel(message.from_user.username))
    await state.clear()


@router.message(AppointmentState.choosing_trainer_name)
async def show_wrong_trainer(message: Message):
    await message.reply("Такого тренера не существует. Выберите из имеющихся")

