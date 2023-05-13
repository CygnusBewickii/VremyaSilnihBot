from aiogram.fsm.state import State, StatesGroup


class RegularClientState(StatesGroup):
    choosing_day = State()
    choosing_time = State()
    choosing_client_name = State()
    choosing_trainer_name = State()


class DeletingRegularClientState(StatesGroup):
    choosing_name = State()