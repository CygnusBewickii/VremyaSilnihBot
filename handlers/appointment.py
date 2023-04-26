from aiogram import Router
from aiogram.types import Message
from aiogram.filters.text import Text

router = Router()

@router.message(Text())