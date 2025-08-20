import sqlite3

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, and_, any_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)

bcrypt = Bcrypt()
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

class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)


def db_load_user(user_id):
    with SessionLocal() as session:
        return session.query(User).get(int(user_id))

def db_check_user_exists(username):
    with SessionLocal() as session:
        data = session.query(User).filter_by(User.username==username)
        if data:
            return True
        else:
            return False

def db_create_user(username, password):
    
    user = User(username)
    user.set_password(password)

    with SessionLocal() as session:
        session.add(user)
        session.commit

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



    