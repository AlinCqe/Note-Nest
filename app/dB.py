from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, and_, ForeignKey, or_, exists, select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

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

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='uploads')

class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    profile_picture_safe_filename = Column(String, nullable=False)

    uploads = relationship('Sheet', back_populates='user')


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

############# temp func
def db_get_users():
    with SessionLocal() as session:
        data = session.query(User).all()
    return 'x'


def db_load_user(user_id):
    with SessionLocal() as session:
        return session.query(User).get(int(user_id))

def db_check_user_exists(username):

    with SessionLocal() as session:
        data = session.query(User).filter_by(username=username).first()
        if data:

            return True
        else:
            return False

def db_check_password(username, password):
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()

        if user.check_password(password=password):
            return True
        else:
            return False

def db_get_user(username):
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        return user

def db_create_user(username, password):
    
    user = User(username=username, profile_picture_safe_filename='default_pf.jpg')
    user.set_password(password)

    with SessionLocal() as session:
        session.add(user)
        session.commit()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_sheets_from_dB(song_name=None, authors=None, categories=None, instruments=None, q=None, safe_filename=None, user_id=None):
    filters = []
    
    if song_name:
        filters.append(Sheet.song_name.ilike(f"%{song_name}%"))
        
    if authors:
        filters.append(Sheet.authors.contains(authors))
        
    if categories:
        filters.append(Sheet.categories.contains(categories))
 
    if instruments:
        filters.append(Sheet.instruments.contains(instruments))

    if safe_filename:
        filters.append(Sheet.safe_filename.contains(safe_filename))

    if user_id:
        filters.append(Sheet.user_id.contains(user_id))


    if q:
        q_lower = q.lower()
        filters.append(
            or_(
                Sheet.song_name.ilike(f"%{q}%"),
                func.lower(func.array_to_string(Sheet.authors, ' ')).ilike(f"%{q_lower}%"),
                func.lower(func.array_to_string(Sheet.categories, ' ')).ilike(f"%{q_lower}%"),
                func.lower(func.array_to_string(Sheet.instruments, ' ')).ilike(f"%{q_lower}%")
            )
        )

    with SessionLocal() as session:
        if filters:
            data = session.query(Sheet).options(joinedload(Sheet.user)).filter(and_(*filters)).all()

        else:
            data = session.query(Sheet).options(joinedload(Sheet.user)).all()

        sheets = [    
            {
                "id": sheet.id,
                "song_name": sheet.song_name,
                "authors": sheet.authors,
                "categories": sheet.categories,
                "instruments": sheet.instruments,   
                "user_id": sheet.user_id,
                "safe_filename": sheet.safe_filename,
                "username": sheet.user.username,
                "profile_picture": sheet.user.profile_picture_safe_filename
            }
            for sheet in data
        ]

        authors_check_box = []
        instruments_check_box = []
        categories_check_box = []

        for sheet in data:
            for a in sheet.authors:
                authors_check_box.append(a)

            for i in sheet.instruments:
                instruments_check_box.append(i)

            for c in sheet.categories:
                categories_check_box.append(c)

        authors_check_box = list(set(authors_check_box))
        instruments_check_box = list(set(instruments_check_box))
        categories_check_box = list(set(categories_check_box))

        filters = {
            'authors': authors_check_box,
            'instruments': instruments_check_box,
            'categories':categories_check_box
        }

        return {'sheets': sheets, 'filters': filters}



def insert_sheet(safe_filename, song_name, authors, categories, instruments, user_id):
 
    with SessionLocal() as session:
        session.add(Sheet(safe_filename=safe_filename,song_name=song_name,authors=authors,categories=categories,instruments=instruments,user_id=user_id))
        session.commit()


def get_filters_from_db():

    authors = []
    instruments = []
    categories = []

    with SessionLocal() as session:
        for sheet in session.query(Sheet).all():
            for a in sheet.authors:
                authors.append(a)

            for i in sheet.instruments:
                instruments.append(a)

            for c in sheet.categories:
                categories.append(a)

    authors = list(set(authors))
    instruments = list(set(instruments))
    categories = list(set(categories))

    print(authors, instruments, categories)

    return authors, instruments, categories



def get_song_name(filename):

    with SessionLocal() as session:
        song_name = session.query(Sheet.song_name).filter(Sheet.safe_filename == filename).scalar()
        print(song_name)
        return song_name


def get_user_data(user_id):

    with SessionLocal() as session:
        sheets_data = session.query(Sheet).filter(Sheet.user_id == user_id).all()
        sheets = [    
            {
                "id": sheet.id,
                "song_name": sheet.song_name,
                "authors": sheet.authors,
                "categories": sheet.categories,
                "instruments": sheet.instruments,   
                "user_id": sheet.user_id,
                "safe_filename": sheet.safe_filename
            }
            for sheet in sheets_data
        ]

        profile_query = session.query(User).filter(User.id == user_id).with_entities(User.username, User.profile_picture_safe_filename).all()
        profile_data = [
            {"username": username, "profile_picture": profile_picture}
            for username, profile_picture in profile_query
        ]


    return sheets, profile_data

def db_update_profile_picture(user_id, new_safe_filename):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()

        if user:
            user.profile_picture_safe_filename = new_safe_filename
            session.commit() 
    

def db_edit_sheet(safe_filename,song_name, authors, categories, instruments):
    
    print(safe_filename,song_name,authors,categories,instruments)
    with SessionLocal() as session:
        
        sheet = session.query(Sheet).filter(Sheet.safe_filename == safe_filename).first()

        if sheet:
            
            sheet.song_name = song_name   
            sheet.authors = authors 
            sheet.categories = categories 
            sheet.instruments = instruments 

        session.commit()

    
def db_delete_sheet(safe_filename):
    with SessionLocal() as session:
        sheet = session.query(Sheet).filter(Sheet.safe_filename == safe_filename).first()

        if sheet:
            session.delete(sheet)
            session.commit()
            return True
        else:
            return False
        

def get_current_profile_picture(user_id):
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        
        if user:
            return user.profile_picture_safe_filename
        