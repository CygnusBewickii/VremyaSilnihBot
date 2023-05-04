import random

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.management import get_regular_clients_panel, get_choose_regular_appointments_kb
from middlewares.authorization import IsAdminMiddleware
from states.client import ClientState


router = Router()
router.message.middleware(IsAdminMiddleware())

@router.message(Text(text="Система постоянных клиентов"))
async def get_clients_panel(message: Message, state: FSMContext):
    await message.reply("Переход на панель управления", reply_markup=get_regular_clients_panel())
    await state.clear()


@router.message(Text(text="Добавить клиента"))
async def add_client(message: Message, state: FSMContext):
    await message.reply("Напишите имя клиента")
    await state.set_state(ClientState.choosing_client_name)

@router.message(ClientState.choosing_client_name)
async def choose_date(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("Выберите день", reply_markup=get_choose_regular_appointments_kb())

@router.callback_query(Text(text="choose_day"))
async def choose_datetime(callback: CallbackQuery):
    # match callback.
    await callback.answer()