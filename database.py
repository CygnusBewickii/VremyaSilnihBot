from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(getenv("DB_URL"))

Base.metadata.create_all(bind=engine)

Session = scoped_session(sessionmaker(bind=engine))
