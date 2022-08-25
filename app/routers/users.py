from . . import models, schema, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from . . database import engine, get_db
from sqlalchemy.orm import Session
from . . utils import hash


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user:  schema.UserCreate ,db: Session = Depends(get_db)):

    # hash password - user password
    hashed_password = hash.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/users/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    
    return user