import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from database import Session
from models import User

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6042261982:AAET_m7H5TRK2tux4JuR2LLG3G_8z5V3tkc")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    new_user = User(telegram_id=321313, username='dsada')
    with Session.begin() as db:
        db.session.add(new_user)
        db.commit()
    await message.answer("Привет, я телеграм бот зала тайского бокса \"Время сильных\"")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())