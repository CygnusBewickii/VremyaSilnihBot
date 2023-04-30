import datetime

from aiogram import Router
from middlewares.authorization import isRegisteredMiddleware
from aiogram.filters.text import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers import appointment as appointment_handler
from handlers import clients
from keyboards.management import get_main_management_panel
from utils.db_queries import get_week_appointments, get_client_by_id, get_trainer_by_id, set_chat_id

router = Router()
router.message.middleware(isRegisteredMiddleware())
router.include_routers(appointment_handler.router, clients.router)


@router.message(Command("menu"))
async def return_to_panel(message: Message, state: FSMContext):
    set_chat_id(message.from_user.id, message.chat.id)
    await message.answer(text='Возвращение в меню', reply_markup=get_main_management_panel())
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
                client = get_client_by_id(appointment.client_id)
                trainer = get_trainer_by_id(appointment.trainer_id)
                reply_message += f'{appointment.date.strftime("%H:%M")} - {client.name if appointment.client_id != None else "Нет"} - {trainer.name if appointment.trainer_id != None else "Нет"}' + '\n'
        reply_message += '\n'
    await message.reply(reply_message)

