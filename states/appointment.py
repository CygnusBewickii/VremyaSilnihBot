from aiogram.fsm.state import State, StatesGroup

class AppointmentState(StatesGroup):
    choosing_appointment_date = State()
    choosing_appointment_time = State()
    choosing_client_name = State()
    choosing_trainer_name = State()