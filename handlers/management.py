import datetime

from aiogram import Router
from middlewares.authorization import IsRegisteredMiddleware
from aiogram.filters.text import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers import appointment as appointment_handler
from handlers import clients, trainers
from keyboards.management import get_main_management_panel
from utils.db_queries import get_week_appointments, get_trainer_by_id, set_chat_id

router = Router()
router.message.middleware(IsRegisteredMiddleware())
router.include_routers(appointment_handler.router, clients.router, trainers.router)


@router.message(Command("menu"))
async def return_to_panel(message: Message, state: FSMContext):
    set_chat_id(message.from_user.id, message.chat.id)
    await message.answer(text='Возвращение в меню', reply_markup=get_main_management_panel(message.from_user.username))
    await state.clear()

@router.message(Text(text="Расписание на неделю"))
async def get_week_schedule(message: Message):
    appointments = get_week_appointments()
    reply_message = '<b>Время - Клиент - Тренер</b> \n\n'
    for day in range(7):
        today = datetime.datetime.today()
        day_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=day)
        reply_message += (day_date.strftime('%A')) + '\n' + '\n'
        for appointment in appointments:
            if day_date < appointment.date < day_date + datetime.timedelta(days=1):
                trainer = get_trainer_by_id(appointment.trainer_id)
                reply_message += f'{appointment.date.strftime("%H:%M")} - {f"{appointment.client_name} - {trainer.name}" if appointment.client_name != None else "Никто не записан"}' + '\n'
        reply_message += '\n'
    await message.reply(reply_message)
