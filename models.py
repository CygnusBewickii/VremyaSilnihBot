from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, index=True, unique=True)
    name = Column(String(64))
    role = Column(String(32))
    username = Column(String(64), unique=True)
    trainings = relationship("Appointment", back_populates="trainer")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True, unique=True)
    trainer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    trainer = relationship("User", back_populates="trainings")
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)
    client = relationship("Client", back_populates="appointments")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    phone_number = Column(String(32))
    appointments = relationship("Appointment", back_populates="client")
