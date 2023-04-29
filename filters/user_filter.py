from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db_queries import get_client_by_name, get_trainer_by_name

class ClientExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        client = get_client_by_name(message.text)
        return True if client != None else False

class TrainerExistsFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        trainer = get_trainer_by_name(message.text)
        return True if trainer != None else False