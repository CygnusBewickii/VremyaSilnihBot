from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message
from utils.db_queries import get_user_by_telegram_id, set_chat_id
from keyboards.management import get_main_management_panel


router = Router()

@router.message(Text(text="Войти", ignore_case=True))
async def login(message: Message):
    user_id = message.from_user.id
    user = get_user_by_telegram_id(user_id)
    if user == None:
        await message.reply('Вы не являетесь членом клуба')
    else:
        set_chat_id(user_id, message.chat.id)
        await message.reply(f'Здравствуйте, {user.name}. Вы удачно авторизованы', reply_markup=get_main_management_panel())
