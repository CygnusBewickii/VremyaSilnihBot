import datetime

from models import User, Appointment, RegularClient, RegularAppointment
from database import session
from calendar import monthrange
from sqlalchemy import func

def set_chat_id(username, user_chat_id: int):
    with session() as db:
        user = db.query(User).where(User.username == username).one()
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
        trainings = db.query(Appointment).filter(Appointment.date >= today).filter(Appointment.date < week_later).\
            order_by(Appointment.date).all()
        return trainings

def create_empty_appointments(year: int, month: int):
    with session() as db:
        test_appointment = db.query(Appointment).where(func.extract("MONTH", Appointment.date) == month).all()
        if len(test_appointment) == 0:
            for day in range(1, monthrange(year, month)[1]+1):
                for hour in range(6, 22):
                    new_appointment = Appointment(
                        date=datetime.datetime(year, month, day, hour),
                        client_name=None,
                        trainer_id=None,
                    )
                    db.add(new_appointment)
                    db.commit()
            fill_days_with_regular_clients()


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
        appointment = get_appointment_by_datetime(date)
        return True if appointment == None or appointment.client_name == None else False


def get_appointment_by_datetime(date: datetime.datetime) -> Appointment:
    with session() as db:
        appointment = db.query(Appointment).where(Appointment.date == date).one_or_none()
        return appointment

def create_trainer(name: str, username: str, role: str):
    with session() as db:
        new_trainer = User(
            name=name,
            username=username,
            role=role
        )
        db.add(new_trainer)
        db.commit()


def delete_trainer(name: str):
    with session() as db:
        trainer = get_trainer_by_name(name)
        delete_regular_appointments_for_trainer(trainer.id)
        set_empty_appointments_for_trainer(trainer.id)
        db.delete(trainer)
        db.commit()

def set_empty_appointments_for_trainer(trainer_id: int):
    with session() as db:
        appointments = db.query(Appointment).where(Appointment.trainer_id == trainer_id).all()
        for appointment in appointments:
            set_empty_appointment(appointment.date)

def is_user_admin(username: str) -> bool:
    trainer = get_trainer_by_username(username)
    return trainer.role == "admin"


def fill_days_with_regular_client(day_of_the_week: int, trainer_id: int, time: datetime.time, client_name: str):
    with session() as db:
        appointments = db.query(Appointment).where(func.extract("DOW", Appointment.date) == day_of_the_week)\
            .filter(Appointment.date > datetime.datetime.now())\
            .filter(Appointment.client_name is None)\
            .filter(func.extract("MINUTE", Appointment.date) == time.minute)\
            .filter(func.extract("HOUR", Appointment.date) == time.hour)\
            .all()
        if len(appointments) != 0:
            for appointment in appointments:
                appointment: Appointment
                appointment.client_name = client_name
                appointment.trainer_id = trainer_id
                db.commit()
        else:
            correct_datetimes = db.query(Appointment).where(func.extract("DOW", Appointment.date) == day_of_the_week).all()
            dates_set = set()
            for correct_datetime in correct_datetimes:
                dates_set.add(datetime.datetime(year=correct_datetime.date.year,
                                                month=correct_datetime.date.month,
                                                day=correct_datetime.date.day,
                                                hour=time.hour,
                                                minute=time.minute))
            for date in dates_set:
                create_new_appointment(date, client_name, trainer_id)

def fill_days_with_regular_clients():
    with session() as db:
        regular_appointments = db.query(RegularAppointment).all()
        for regular_appointment in regular_appointments:
            client_name = get_regular_client_by_id(regular_appointment.client_id).name
            fill_days_with_regular_client(regular_appointment.week_day_num, regular_appointment.trainer_id, regular_appointment.time, client_name)

def add_regular_client(client_name: str):
    with session() as db:
        new_regular_client = RegularClient(
            name=client_name
        )
        db.add(new_regular_client)
        db.commit()


def get_regular_client_by_name(name: str) -> RegularClient or None:
    with session() as db:
        return db.query(RegularClient).where(RegularClient.name == name).one_or_none()


def get_regular_client_by_id(id: int) -> RegularClient or None:
    with session() as db:
        return db.get(RegularClient, id)


def get_regular_clients() -> list[RegularClient]:
    with session() as db:
        return db.query(RegularClient).all()


def add_new_regular_appointment_to_client(client_name: str, trainer_id: int, week_day_num: int, time: datetime.time):
    with session() as db:
        client = get_regular_client_by_name(client_name)
        if client is None:
            add_regular_client(client_name)
            client = get_regular_client_by_name(client_name)
        new_regular_appointment = RegularAppointment(
            week_day_num=week_day_num,
            time=time,
            client_id=client.id,
            trainer_id=trainer_id
        )
        db.add(new_regular_appointment)
        db.commit()


def get_regular_appointments_by_client(client_name: str) -> list[RegularAppointment]:
    with session() as db:
        client = get_regular_client_by_name(client_name)
        return db.query(RegularAppointment).where(RegularAppointment.client_id == client.id).all()


def delete_regular_appointments_for_trainer(trainer_id: int):
    with session() as db:
        regular_appointments = db.query(RegularAppointment).where(RegularAppointment.trainer_id == trainer_id).all()
        for appointment in regular_appointments:
            db.delete(appointment)
            db.commit()


def get_regular_appointment_by_day_and_time(day_num: int, time: datetime.time) -> RegularClient or None:
    with session() as db:
        return db.query(RegularAppointment).where(RegularAppointment.week_day_num == day_num)\
            .where(RegularAppointment.time == time)\
            .one_or_none()


def delete_regular_appointment(id: int):
    with session() as db:
        appointment = db.get(RegularAppointment, id)
        db.delete(appointment)
        db.commit()


def delete_regular_client(name: str):
    with session() as db:
        regular_client = get_regular_client_by_name(name)
        regular_appointments_of_client = db.query(RegularAppointment).where(RegularAppointment.client_id == regular_client.id).all()
        for appointment in regular_appointments_of_client:
            db.delete(appointment)
            db.commit()
        appointments_of_client = db.query(Appointment).where(Appointment.client_name == regular_client.name).all()
        for appointment in appointments_of_client:
            set_empty_appointment(appointment.date)
            db.commit()
        db.delete(regular_client)
        db.commit()