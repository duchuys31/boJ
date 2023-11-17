from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()

class Major(Base):
    __tablename__ = 'major'
    name = Column(String, primary_key=True)

class Area(Base):
    __tablename__ = 'area'
    name = Column(String, primary_key=True)

class JD(Base):
    __tablename__ = 'jd'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    major = Column(String, ForeignKey('major.name'))
    experience = Column(Integer)
    area = Column(String, ForeignKey('area.name'))
    address = Column(String)
    salary = Column(String)
    company = Column(String)
    describe = Column(Text)
    benefit = Column(Text)
    skill = Column(Text)
    contact = Column(Text)
    tags = Column(Text)

class User(Base):
    __tablename__ = 'user'
    chat_id = Column(String, primary_key=True)
    major = Column(String, ForeignKey('major.name'), nullable=True, default=None)
    experience = Column(Integer, nullable=True, default=None)
    area = Column(String, ForeignKey('area.name'), nullable=True, default=None)

class Skill(Base):
    __tablename__ = 'skill'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = Column(String, ForeignKey('user.chat_id'))
    describe = Column(Text)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
