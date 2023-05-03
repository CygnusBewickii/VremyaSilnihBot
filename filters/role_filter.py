from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_queries import get_trainer_by_username

class RoleExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        roles = ["Администратор", "Тренер"]
        return True if message.text in roles else False

class IsUserAdmin(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        user = get_trainer_by_username(message.from_user.username)
        if user.role == "admin":
            True