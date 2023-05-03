from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.client import ClientState
from keyboards.management import get_main_management_panel


router = Router()

@router.message(Text(text="Добавить клиента"))
async def choose_client_name(message: Message, state: FSMContext):
    await message.reply("Напишите имя нового клиента")
    await state.set_state(ClientState.choosing_client_name)

@router.message(ClientState.choosing_client_name)
async def choose_client_phone(message: Message, state: FSMContext):
    await state.update_data(client_name = message.text)
    await message.reply("Напишите номер телефона клиента")
    await state.set_state(ClientState.choosing_client_phone)

@router.message(ClientState.choosing_client_phone)
async def add_client(message: Message, state: FSMContext):
    await state.update_data(client_phone= message.text)
    user_data = await state.get_data()
    client_name = user_data["client_name"]
    client_phone = user_data["client_phone"]
    create_new_client(client_name, client_phone)
    await message.reply(f"Добавлен пользователь {client_name}  (телефон {client_phone})", reply_markup=get_main_management_panel(message.from_user.username))
    await state.clear()