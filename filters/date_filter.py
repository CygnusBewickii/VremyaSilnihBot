from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message


class DateFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        try:
            if 1 <= int(message.text) <= 31:
                return True
            else:
                False
        except:
            return False

