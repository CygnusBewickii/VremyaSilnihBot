import datetime

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.management import get_regular_clients_panel, get_choose_regular_appointments_kb, get_trainers_kb
from middlewares.authorization import IsAdminMiddleware
from states.client import RegularClientState
# from callbackFactories.regualar_clients import DaysCallbackFactory
from utils.db_queries import fill_days_with_regular_clients
from filters.date_filter import WeekDayFilter, TimeFilter
from filters.user_filter import TrainerExistsFilter

router = Router()
router.message.middleware(IsAdminMiddleware())


@router.message(Text(text="Система постоянных клиентов"))
async def get_clients_panel(message: Message, state: FSMContext):
    await message.reply("Переход на панель управления", reply_markup=get_regular_clients_panel())
    await state.clear()


@router.message(Text(text="Добавить клиента"))
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
    days = {
        "Пн": 1,
        "Вт": 2,
        "Ср": 3,
        "Чт": 4,
        "Пт": 5,
        "Сб": 6,
        "Вс": 0
    }
    day_number = days[message.text]
    await state.update_data(day_number=day_number)
    await message.reply("Напишите время, на которое надо записать")
    await state.set_state(RegularClientState.choosing_time)


@router.message(RegularClientState.choosing_time, TimeFilter())
async def choosing_trainer(message: Message, state: FSMContext):
    await state.update_data(hour=int(message.text[:2]))
    await state.update_data(minutes=int(message.text[3:]))
    await message.reply("Какой тренер будет вести тренировку?", reply_markup=get_trainers_kb())
    await state.set_state(RegularClientState.choosing_trainer_name)


@router.message(RegularClientState.choosing_trainer_name, TrainerExistsFilter())
async def create_regular_appointments(message: Message, state: FSMContext):
    await state.update_data(trainer_name=message.text)
    user_data = await state.get_data()
    time = datetime.time(user_data["hour"], user_data["minutes"])
    fill_days_with_regular_clients(user_data["day_number"], user_data["trainer_name"], time, user_data["client_name"])

