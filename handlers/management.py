from aiogram import Router
from middlewares.authorization import isRegisteredMiddleware
from aiogram.filters.text import Text
from aiogram.types import Message
from handlers import appointment
from keyboards.management import get_select_month_kb

router = Router()
router.message.middleware(isRegisteredMiddleware())
router.include_routers(appointment.router)

@router.message(Text(text="Записать клиента", ignore_case=True))
async def make_appointment(message: Message):
    await message.reply('Выберите месяц', reply_markup=get_select_month_kb())