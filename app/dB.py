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
    uploaed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)



def create_tables():
    with sqlite3.connect('note_nest.db') as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sheets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                safe_filename TEXT NOT NULL,
                song_name filename TEXT NOT NULL,
                author TEXT ,
                category TEXT,
                instrument TEXT,
                uploaded_at DATETIME default CURRENT_TIMESTAMP
            )
        """)    



def get_sheets_from_dB(song_name,authors,categories,instruments):

    filters = []

    if song_name:
        filters.append(Sheet.song_name == song_name)

    if authors:
        if isinstance(authors, list):
            filters.append(Sheet.authors.contains(authors))
        else:    
            filters.append(authors == any_(Sheet.authors))

    if categories:
        if isinstance(categories, list):
            filters.append(Sheet.categories.contains(categories))
        else:
            filters.append(instruments == any_(Sheet.categories))

    if instruments:
        if isinstance(instruments, list):
            filters.append(Sheet.instruments.contains(instruments))
        else:
            filters.append(instruments == any_(Sheet.instruments))


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

    with sqlite3.connect('note_nest.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query, params)
        rows = cursor.fetchall()        
        data = [dict(row) for row in rows]
        
        
    

def insert_sheet(safe_filename, song_name, authors, categories, instruments):

    with sqlite3.connect('note_nest.db') as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO sheets (safe_filename,song_name, author, category, instrument) VALUES (?,?,?,?,?)", (safe_filename,song_name,  authors, categories, instruments))
        conn.commit()

    with SessionLocal() as session:
        session.add(Sheet(safe_filename=safe_filename,song_name=song_name,authors=[authors],categories=[categories],instruments=[instruments]))
        session.commit()



#works, return right safe filename
def get_safe_file_name(song_name):

    with SessionLocal() as session:
        safe_filename = session.query(Sheet.safe_filename).filter(Sheet.song_name == song_name).scalar()
        return safe_filename





    with sqlite3.connect('note_nest.db') as conn:

        cursor = conn.cursor()

        cursor.execute('SELECT safe_filename FROM sheets WHERE song_name = ?', (song_name,))

        result  = cursor.fetchone()

