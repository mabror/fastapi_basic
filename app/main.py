from sqlite3 import connect
from turtle import title
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .models import Post
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True



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
   
    

@app.get("/")
def root():
    return {"message": "Hello World"}



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.get("/post/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}
 

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id)))
                   
    # delete_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int,update_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    # (post.title, post.content, post.published, str(id)))
                   
    # updated_post = cursor.fetchone()
    # conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)

    post = query_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    query_post.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return {"data":  query_post.first()}
    


# @app.get("/sqlalchem")
# def test(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}
