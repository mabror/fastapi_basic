from operator import mod
from re import I
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import models
from .schema import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from  .database import engine, get_db
from sqlalchemy.orm import Session 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# tokken activ minute
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials", 
    headers={"WWW-Authnticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user