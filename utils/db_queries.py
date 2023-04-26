import datetime

from models import User, Appointment
from database import session
def get_user_by_telegram_id(user_id: int) -> User or None:
    with session() as db:
        return db.query(User).where(User.telegram_id == user_id).one_or_none()

def get_date_free_time(month: int, day: int) -> [Appointment]:
    with session() as db:
        db.query(Appointment).where(Appointment.date = )