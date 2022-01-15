from os import get_inheritable
from pydantic import env_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost',database='fastapi', user='postgres',
#         password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error ", error)
#         time.sleep(2)

