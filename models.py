from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///words.db')
Session = sessionmaker(bind=engine)
session = Session()

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    definition = Column(String)
    example = Column(String)
    date_added = Column(DateTime, default=datetime.now)

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)