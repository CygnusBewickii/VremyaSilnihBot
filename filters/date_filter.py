from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from re import match

class DateFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        try:
            if 1 <= int(message.text) <= 31:
                return True
            else:
                False
        except:
            return False


class TimeFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if match(r"[0-9]?[0-9][.:][0-9][0-9]", message.text):
            return True
        else:
            return False

class WeekDayFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        return message.text in days

