from aiogram.types import Message
from aiogram import Router

router = Router()


@router.message()
async def not_recognized_message(message: Message):
    await message.reply("Бот не знает такой команды")

