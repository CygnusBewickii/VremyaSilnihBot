from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

engine = create_engine('mysql+pymysql://root:4322680Artem@localhost/vremyasilnihbot')

Base.metadata.create_all(bind=engine)

Session = scoped_session(sessionmaker(bind=engine))
