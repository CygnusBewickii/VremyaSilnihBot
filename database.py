import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

engine = create_engine(url=os.getenv("DB_URL"))

Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)



