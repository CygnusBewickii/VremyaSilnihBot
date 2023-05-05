from aiogram.fsm.state import State, StatesGroup


class RegularClientState(StatesGroup):
    choosing_day: State()
    choosing_time: State()
    choosing_client_name: State()
    choosint_trainer_name: State()