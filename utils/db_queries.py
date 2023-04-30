import datetime

from models import User, Appointment, Client
from database import session
from calendar import monthrange

def get_user_by_telegram_id(user_id: int) -> User or None:
    with session() as db:
        return db.query(User).where(User.telegram_id == user_id).one_or_none()

def get_date_free_time(year: int, month: int, day: int) -> list[Appointment]:
    start_of_day = datetime.datetime(year, month, day)
    end_of_day = start_of_day + datetime.timedelta(hours=23)
    with session() as db:
        free_time = db.query(Appointment).filter(start_of_day < Appointment.date).filter(Appointment.date < end_of_day).where(Appointment.client_id == None).all()
        return free_time

def get_date_appointments(year: int, month: int, day: int) -> list[Appointment]:
    start_of_day = datetime.datetime(year, month, day)
    end_of_day = start_of_day + datetime.timedelta(hours=23)
    with session() as db:
        appointments = db.query(Appointment).filter(start_of_day < Appointment.date).filter(Appointment.date < end_of_day).all()
        return appointments

def get_clients() -> list[Client]:
    with session() as db:
        return db.query(Client).all()

def get_client_by_id(id: int) -> Client:
    with session() as db:
        return db.get(Client, id)

def get_trainer_by_id(id: int) -> User:
    with session() as db:
        return db.get(User, id)

def get_client_by_name(name: str) -> Client:
    with session() as db:
        return db.query(Client).where(Client.name == name).one_or_none()

def get_trainer_by_name(name: str) -> User:
    with session() as db:
        return db.query(User).where(User.name == name).one_or_none()

def create_new_appointment(date: datetime.datetime, client_id: int, trainer_id: int):
    with session() as db:
        new_appointment = db.query(Appointment).where(Appointment.date == date).one()
        new_appointment.client_id = client_id
        new_appointment.trainer_id = trainer_id
        db.commit()

def get_trainers() -> list[User]:
    with session() as db:
        return db.query(User).all()

def get_week_appointments() -> list[Appointment]:
    today = datetime.date.today()
    week_later = today + datetime.timedelta(weeks=1)
    create_empty_appointments(today.year, today.month)
    create_empty_appointments(week_later.year, week_later.month)
    with session() as db:
        trainings = db.query(Appointment).filter(Appointment.date >= today).filter(Appointment.date < week_later).all()
        return trainings

def create_empty_appointments(year: int, month: int):
    with session() as db:
        test_appointment = db.query(Appointment).filter(Appointment.date == datetime.datetime(year, month, 1, 12)).one_or_none()
        if test_appointment == None:
            for day in range(1, monthrange(year, month)[1]+1):
                for hour in range(6, 22):
                    new_appointment = Appointment(
                        date=datetime.datetime(year, month, day, hour),
                        client_id=None,
                        trainer_id=None,
                    )
                    db.add(new_appointment)
                    db.commit()

def set_empty_appointment(date: datetime.datetime):
    with session() as db:
        appointment = db.query(Appointment).filter(Appointment.date == date).one()
        appointment.client_id = None
        appointment.trainer_id = None
        db.commit()

def is_appointment_empty(date: datetime.datetime) ->  bool:
    with session() as db:
        appointment = db.query(Appointment).where(Appointment.date == date).one()
        return True if appointment.client_id == None else False

def create_new_client(name: str, phone: str):
    with session() as db:
        new_client = Client(
            name=name,
            phone_number=phone
        )
        db.add(new_client)
        db.commit()