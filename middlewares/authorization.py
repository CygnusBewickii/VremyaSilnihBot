from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from keyboards.authorization import get_login_kb
from utils.db_queries import get_trainer_by_username, is_user_admin

class IsRegisteredMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = get_trainer_by_username(event.from_user.username)
        if user != None:
            return await handler(event, data)
        else:
            return await event.reply('Вы не имеете доступа к данной функции', reply_markup=get_login_kb())

class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if is_user_admin(event.from_user.username):
            return await handler(event, data)
        else:
            return await event.reply("К данной функции доступ имеет только администратор")