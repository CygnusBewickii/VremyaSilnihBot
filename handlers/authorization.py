from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message

router = Router()

@router.message(Text(text="Войти", ignore_case=True))
async def login(message: Message):
    pass