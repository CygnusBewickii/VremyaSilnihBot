import datetime

from models import User, Appointment, Client
from database import session

def get_user_by_telegram_id(user_id: int) -> User or None:
    with session() as db:
        return db.query(User).where(User.telegram_id == user_id).one_or_none()

def get_date_free_time(year: int, month: int, day: int) -> list[Appointment]:
    start_of_day = datetime.datetime(year, month, day)
    end_of_day = start_of_day + datetime.timedelta(hours=23)
    with session() as db:
        is_day_empty = True if db.query(Appointment).filter(start_of_day < Appointment.date).filter(Appointment.date < end_of_day).count() == 0 else False

        if is_day_empty:
            for hour in range(6, 22):
                new_appointment = Appointment(
                    date=datetime.datetime(year, month, day, hour),
                    client_id=None,
                    trainer_id=None
                )
                db.add(new_appointment)
                db.commit()
        free_time = db.query(Appointment).filter(start_of_day < Appointment.date).filter(Appointment.date < end_of_day).where(Appointment.client_id == None).all()
        return free_time

def get_clients() -> list[Client]:
    with session() as db:
        return db.query(Client).all()

def get_client_by_name(name: str) -> User:
    with session() as db:
        return db.query(Client).where(Client.name == name).one_or_none()

def create_new_appointment(date: datetime.datetime, client_id: int, trainer_id: int):
    with session() as db:
        new_appointment = db.query(Appointment).where(Appointment.date == date).one()
        new_appointment.client_id = client_id
        new_appointment.trainer_id = trainer_id
        db.add(new_appointment)
        db.commit()