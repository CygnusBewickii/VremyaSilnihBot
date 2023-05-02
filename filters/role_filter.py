from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

class RoleExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        roles = ["Администратор", "Тренер"]
        return True if message.text in roles else False