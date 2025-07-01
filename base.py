from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///vandata.db")
Session = sessionmaker(bind=engine)
Base = DeclarativeBase()

class Base(DeclarativeBase):
    pass