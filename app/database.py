from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:qwerty123$@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessinLocal()
    try:
        yield db
    finally:
        db.close()


    
# try:
#     conn = psycopg2.connect(host='localhost', 
#                             database='fastapi', 
#                             user='postgres',
#                             password='qwerty123$',
#                             cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was successfull")

# except Exception as error:
#     print("Connection to database failed")
#     print("Error:  ", error)
#     time.sleep(2)