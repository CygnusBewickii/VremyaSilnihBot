from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_queries import get_client_by_name

class UserExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        client = get_client_by_name(message.text)
        return True if client != None else False
