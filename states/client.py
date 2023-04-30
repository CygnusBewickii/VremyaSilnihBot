from aiogram.fsm.state import State, StatesGroup

class ClientState(StatesGroup):
    choosing_client_name = State()
    choosing_client_phone = State()