from enum import auto
from sqlite3 import connect
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from .utils import hash
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from app import schema
from .routers import post, users

models.Base.metadata.create_all(bind=engine)




app = FastAPI()



try:
    conn = psycopg2.connect(host='localhost', 
                            database='fastapi', 
                            user='postgres',
                            password='qwerty123$',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successfull")

except Exception as error:
    print("Connection to database failed")
    print("Error:  ", error)
   
    


app.include_router(post.router)
app.include_router(users.router)