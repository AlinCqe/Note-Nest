import sqlite3

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, and_, any_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Sheet(Base):
    __tablename__ = 'sheets'
    
    id = Column(Integer, primary_key=True, index=True)
    safe_filename = Column(String, nullable=False)
    song_name = Column(String, nullable=False)
    authors = Column(ARRAY(String))
    categories = Column(ARRAY(String))
    instruments = Column(ARRAY(String))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)

def get_sheets_from_dB(song_name,authors,categories,instruments):

    filters = []
    print(song_name,authors,categories,instruments)

    if song_name:
        filters.append(Sheet.song_name.ilike(f"%{song_name}%"))
        
    if authors:
        filters.append(Sheet.authors.contains(authors))

    if categories:
        filters.append(Sheet.categories.contains(categories))
 
    if instruments:
        filters.append(Sheet.instruments.contains(instruments))

    print(filters)
    with SessionLocal() as session:
        if filters:
            data = session.query(Sheet).filter(and_(*filters)).all()
        else:
            data =  data = session.query(Sheet).all()

        sheets = [    {
        "id": sheet.id,
        "song_name": sheet.song_name,
        "authors": sheet.authors,
        "categories": sheet.categories,
        "instruments": sheet.instruments
        }
        for sheet in data

    ]
        print(sheets)
        return sheets

    

def insert_sheet(safe_filename, song_name, authors, categories, instruments):
 
    with SessionLocal() as session:
        session.add(Sheet(safe_filename=safe_filename,song_name=song_name,authors=authors,categories=categories,instruments=instruments))
        session.commit()



def get_safe_file_name(song_name):

    with SessionLocal() as session:
        safe_filename = session.query(Sheet.safe_filename).filter(Sheet.song_name == song_name).scalar()
        return safe_filename



    