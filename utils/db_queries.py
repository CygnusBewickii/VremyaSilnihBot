import datetime

from models import User, Appointment
from database import session
from calendar import monthrange

def set_chat_id(user_telegram_id: int, user_chat_id: int):
    with session() as db:
        user = db.query(User).where(User.telegram_id == user_telegram_id).one()
        user.chat_id = user_chat_id
        db.commit()

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


def get_trainer_by_id(id: int) -> User:
    with session() as db:
        return db.get(User, id)


def get_trainer_by_username(username: str) -> User or None:
    with session() as db:
        return db.query(User).where(User.username == username).one_or_none()

def get_trainer_by_name(name: str) -> User:
    with session() as db:
        return db.query(User).where(User.name == name).one_or_none()

def create_new_appointment(date: datetime.datetime, client_name: str, trainer_id: int):
    with session() as db:
        new_appointment = db.query(Appointment).where(Appointment.date == date).one_or_none()
        if new_appointment == None:
            previous_appointment = db.query(Appointment).where(Appointment.date == date - datetime.timedelta(minutes=date.minute)).one()
            db.delete(previous_appointment)
            next_appointment = db.query(Appointment).where(Appointment.date == date + datetime.timedelta(minutes=60-date.minute)).one()
            db.delete(next_appointment)
            new_appointment = Appointment(
                date=date,
                trainer_id=trainer_id,
                client_name=client_name
            )
            db.add(new_appointment)
            db.commit()
        else:
            new_appointment.client_name = client_name
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
                        client_name=None,
                        trainer_id=None,
                    )
                    db.add(new_appointment)
                    db.commit()

def set_empty_appointment(date: datetime.datetime):
    with session() as db:
        appointment = db.query(Appointment).filter(Appointment.date == date).one()
        appointment.client_name = None
        appointment.trainer_id = None
        if date.minute != 0:
            db.add(Appointment(
                date=date+datetime.timedelta(minutes=60-date.minute),
                trainer_id=None,
                client_name=None
            ))
            db.add(Appointment(
                date=date-datetime.timedelta(minutes=date.minute),
                trainer_id=None,
                client_name=None
            ))
            db.delete(appointment)
        db.commit()

def is_appointment_empty(date: datetime.datetime) ->  bool:
    with session() as db:
        appointment = db.query(Appointment).where(Appointment.date == date).one_or_none()
        return True if appointment == None or appointment.client_name == None else False


def create_trainer(name: str, username: str, role: str):
    with session() as db:
        new_trainer = User(
            name=name,
            username=username,
            role=role
        )
        db.add(new_trainer)
        db.commit()
