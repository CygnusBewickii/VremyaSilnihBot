from aiogram.fsm.state import State, StatesGroup

class TrainerState(StatesGroup):
    choosing_trainer_name = State()
    choosing_trainer_username = State()
    choosing_trainer_role = State()
