from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_queries import get_regular_client_by_name


class RegularClientExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return True if get_regular_client_by_name(message.text) is not None else False