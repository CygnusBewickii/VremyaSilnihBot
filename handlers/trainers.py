from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.trainer import TrainerState
from keyboards.management import get_roles_kb, get_main_management_panel
from utils.db_queries import create_trainer
from filters.role_filter import RoleExistsFilter

router = Router()

@router.message(Text(text="Добавить нового тренера"))
async def choose_trainer_name(message: Message, state: FSMContext):
    await message.reply("Введите имя нового тренера")
    await state.set_state(TrainerState.choosing_trainer_name)

@router.message(TrainerState.choosing_trainer_name)
async def choose_trainer_username(message: Message, state: FSMContext):
    await state.update_data(trainer_name=message.text)
    await message.reply("Введите username нового тренера \nОн находится в профиле у нужного человека и предоставлен в виде @username. Скопируйте и вставьте сюда")
    await state.set_state(TrainerState.choosing_trainer_username)

@router.message(TrainerState.choosing_trainer_username)
async def choose_trainer_role(message: Message, state: FSMContext):
    await state.update_data(trainer_username=message.text.lstrip("@"))
    await message.reply("Выберите роль нового тренера", reply_markup=get_roles_kb())
    await state.set_state(TrainerState.choosing_trainer_role)

@router.message(TrainerState.choosing_trainer_role, RoleExistsFilter())
async def add_trainer(message: Message, state: FSMContext):
    if message.text == "Администратор":
        await state.update_data(trainer_role="admin")
    if message.text == "Тренер":
        await state.update_data(trainer_role="trainer")
    user_data = await state.get_data()
    create_trainer(user_data["trainer_name"], user_data["trainer_username"], user_data["trainer_role"])
    await message.reply("Новый тренер добавлен в систему", reply_markup=get_main_management_panel())
    await state.clear()

@router.message(TrainerState.choosing_trainer_role)
async def show_wrong_role(message: Message):
    await message.reply("Такой роли не существует. Выберите из имеющихся при помощи кнопок")
