from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import validates

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
    
    @validates('age')
    def validate_age(self, key, value):
        if value < 1 or value > 99:
            raise ValueError('Age must be between 18 and 99')
        return value

    @validates('name')
    def validate_name(self, key, value):
        db = SessionLocal()
        does_user_exist = db.query(User).filter(User.name == value).first()
        if does_user_exist:
            raise ValueError('User with this name already exists')
            
        if len(value) < 2 or len(value) > 20:
            raise ValueError('Name must be less than 20 characters')
        return value