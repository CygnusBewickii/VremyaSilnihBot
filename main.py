import asyncio
import locale
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from os import getenv
from dotenv import load_dotenv
from keyboards.authorization import get_login_kb
from handlers import authorization, management, wrongs
from aiogram.fsm.storage.memory import MemoryStorage
from locale import setlocale


setlocale(locale.LC_ALL, "ru_RU.UTF-8")
load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv("BOT_TOKEN"), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я телеграм бот зала тайского бокса \"Время сильных\"",
                         reply_markup=get_login_kb())


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_routers(authorization.router, management.router)
    dp.include_router(wrongs.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())