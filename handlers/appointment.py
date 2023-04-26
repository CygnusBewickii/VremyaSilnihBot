import datetime

from aiogram import Router
from aiogram.types import Message
from filters.date_filter import DateFilter
from aiogram.fsm.context import FSMContext
from states.appointment import Appointment

router = Router()

@router.message(lambda m: ('Этот месяц' in m.text) or ('Следующий месяц' in m.text))
async def select_date(message: Message, state: FSMContext):
    current_date = datetime.date.today()
    if 'Этот месяц' in message.text:
        await state.update_data(month = current_date.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {current_date.strftime('%B')}")
        await state.set_state(Appointment.choosing_appointment_date)
    if 'Следующий месяц' in message.text:
        next_month = current_date + datetime.timedelta(days=31)
        await state.update_data(month = next_month.month)
        await message.reply(f"Напишите дату, на которую хотите записать в месяце {next_month.strftime('%B')}")
        await state.set_state(Appointment.choosing_appointment_date)

@router.message(Appointment.choosing_appointment_date, DateFilter())
async def select_time(message: Message, state: FSMContext):
    await state.update_data(day = int(message.text))
    free_time =
@router.message(Appointment.choosing_appointment_date)
async def show_wrong_month(message: Message):
    await message.reply("Данные введены некорректо. Введите дату (число от 1 до 31)")