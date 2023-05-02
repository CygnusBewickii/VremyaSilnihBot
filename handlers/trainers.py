from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.trainer import TrainerState
from keyboards.management import get_roles_kb

router = Router()

@router.message(Text(text="Добавить нового тренеа"))
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
    await message.reply("Выберите роль нового тренера", reply_markup=)