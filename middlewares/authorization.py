from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from keyboards.authorization import get_login_kb
from utils.db_queries import get_user_by_telegram_id
class isRegisteredMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = get_user_by_telegram_id(event.from_user.id)
        if user != None:
            return await handler(event, data)
        else:
            return await event.reply('Вы не имеете доступа к данной функции', reply_markup=get_login_kb())
