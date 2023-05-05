import datetime
import random

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.management import get_regular_clients_panel, get_choose_regular_appointments_kb, get_trainers_kb
from middlewares.authorization import IsAdminMiddleware
from states.client import RegularClientState
from callbackFactories.regualar_clients import DaysCallbackFactory
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
        "Пн": 0,
        "Вт": 1,
        "Ср": 2,
        "Чт": 3,
        "Пт": 4,
        "Сб": 5,
        "Вс": 6
    }
    day_number = days[message.text]
    await state.update_data(day_number=day_number)
    await message.reply("Напишите время, на которое надо записать")
    await state.set_state(RegularClientState.choosing_time)

@router.message(RegularClientState.choosing_time, TimeFilter())
async def choosing_trainer(message: Message, state: FSMContext):
    await state.update_data(hour=message.text[:2])
    await state.update_data(minutes=message.text[3:])
    await message.reply("Какой тренер будет вести тренировку?", reply_markup=get_trainers_kb())
    await state.set_state(RegularClientState.choosint_trainer_name)

@router.message(RegularClientState.choosint_trainer_name, TrainerExistsFilter())
async def create_regular_appointments(message: Message, state: FSMContext):
    await state.update_data(trainer_name=message.text)


