from typing import Optional
from aiogram.filters.callback_data import CallbackData


class DaysCallbackFactory(CallbackData):
    action: str
    value: Optional[int]