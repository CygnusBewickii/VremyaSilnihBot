import datetime

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.management import get_regular_clients_panel, get_choose_regular_appointments_kb, get_trainers_kb, \
    get_main_management_panel, get_regular_clients_kb, get_regular_client_appointments_kb
from middlewares.authorization import IsAdminMiddleware
from states.client import RegularClientState, DeletingRegularClientState
from states.appointment import DeltetingRegularAppointment
from utils.db_queries import fill_days_with_regular_client, get_trainer_by_name, add_new_regular_appointment_to_client,\
    delete_regular_client as delete_regular_client_db, get_regular_appointment_by_day_and_time, \
    delete_regular_appointment as delete_regular_appointment_db
from utils.time import split_time
from filters.date_filter import WeekDayFilter, TimeFilter
from filters.user_filter import TrainerExistsFilter
from filters.client_filter import RegularClientExistsFilter

router = Router()


days = {
        "Пн": 1,
        "Вт": 2,
        "Ср": 3,
        "Чт": 4,
        "Пт": 5,
        "Сб": 6,
        "Вс": 0
    }


@router.message(Text(text="Система постоянных клиентов"))
async def get_clients_panel(message: Message, state: FSMContext):
    await message.reply("Переход на панель управления", reply_markup=get_regular_clients_panel())
    await state.clear()


@router.message(Text(text="Удалить клиента"))
async def choose_client_to_delete(message: Message, state: FSMContext):
    await message.reply("Напишите или выберите имя клиента, записи которого хотите удалить", reply_markup=get_regular_clients_kb())
    await state.set_state(DeletingRegularClientState.choosing_name)


@router.message(DeletingRegularClientState.choosing_name, RegularClientExistsFilter())
async def delete_regular_client(message: Message, state: FSMContext):
    delete_regular_client_db(message.text)
    await message.reply("Клиент и его записи удалены", reply_markup=get_main_management_panel(message.from_user.username))
    await state.clear()


@router.message(Text(text="Добавить постоянную запись"))
async def add_client(message: Message, state: FSMContext):
    await message.reply("Напишите имя клиента")
    await state.set_state(RegularClientState.choosing_client_name)


@router.message(RegularClientState.choosing_client_name)
async def choose_date(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("Выберите день", reply_markup=get_choose_regular_appointments_kb())
    await state.set_state(RegularClientState.choosing_day)


@router.message(RegularClientState.choosing_day, WeekDayFilter())
async def choose_time(message: Message, state: FSMContext):
    day_number = days[message.text]
    await state.update_data(day_number=day_number)
    await message.reply("Напишите время, на которое надо записать", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegularClientState.choosing_time)


@router.message(RegularClientState.choosing_time, TimeFilter())
async def choosing_trainer(message: Message, state: FSMContext):
    splitted_time = split_time(message.text)
    await state.update_data(hour=int(splitted_time[0]))
    await state.update_data(minutes=int(splitted_time[1]))
    await message.reply("Какой тренер будет вести тренировку?", reply_markup=get_trainers_kb())
    await state.set_state(RegularClientState.choosing_trainer_name)


@router.message(RegularClientState.choosing_trainer_name, TrainerExistsFilter())
async def add_regular_appointment_to_array(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        appointments_array = user_data["appointments_array"]
        appointments_array: list
        appointments_array.append({
            'day_number': user_data["day_number"],
            'time': datetime.time(user_data["hour"], user_data["minutes"]),
            'trainer_id': get_trainer_by_name(message.text).id,
            'client_name': user_data["client_name"]
        })
        await state.update_data(appointments_array=appointments_array)
    except:
        await state.update_data(appointments_array=[{
            'day_number': user_data["day_number"],
            'time': datetime.time(user_data["hour"], user_data["minutes"]),
            'trainer_id': get_trainer_by_name(message.text).id,
            'client_name': user_data["client_name"]
        }])
    await message.reply("Выберите ещё записи для клиента, или нажмите продолжить", reply_markup=get_choose_regular_appointments_kb())
    await state.set_state(RegularClientState.choosing_day)


@router.message(Text(text="Утвердить записи"))
async def create_regular_appointments(message: Message, state: FSMContext):
    user_data = await state.get_data()
    regular_appointments = user_data["appointments_array"]
    for appointment in regular_appointments:
        day_number = appointment["day_number"]
        time = appointment["time"]
        trainer_id = appointment["trainer_id"]
        client_name = appointment["client_name"]
        add_new_regular_appointment_to_client(client_name, trainer_id, day_number, time)
        fill_days_with_regular_client(day_number, trainer_id, time, client_name)
    await message.reply("Новые постоянные записи добавлены", reply_markup=get_regular_clients_panel())
    await state.clear()


@router.message(Text(text="Удалить постоянную запись"))
async def choose_regular_client_appointment_to_delete(message: Message, state: FSMContext):
    await message.reply("Введите или выберите имя клиента, запись которого хотите удалить", reply_markup=get_regular_clients_kb())
    await state.set_state(DeltetingRegularAppointment.choosing_regular_appointment_name)


@router.message(DeltetingRegularAppointment.choosing_regular_appointment_name, RegularClientExistsFilter())
async def choose_regular_appointment_to_delete(message: Message, state: FSMContext):
    await message.reply("Выберите, какую запись хотите удалить?",
                        reply_markup=get_regular_client_appointments_kb(message.text))
    await state.set_state(DeltetingRegularAppointment.choosing_regular_appointment)

@router.message(DeltetingRegularAppointment.choosing_regular_appointment)
async def delete_regular_appointment(message: Message, state: FSMContext):
    appointment = get_regular_appointment_by_day_and_time(days[message.text[:2]], message.text[3:])
    delete_regular_appointment_db(appointment.id)
    await message.reply("Постоянная запись удалена", reply_markup=get_regular_clients_panel())
    await state.clear()

