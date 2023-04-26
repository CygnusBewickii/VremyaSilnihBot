from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    role = Column(String(32))
    telegram_id = Column(Integer, index=True, unique=True)
    username = Column(String(64), unique=True)
    trainings = relationship("Appointment")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True, unique=True)
    trainer = Column(Integer, ForeignKey('users.id'))

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True)