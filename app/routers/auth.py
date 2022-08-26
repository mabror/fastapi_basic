from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import database, schema, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return a token
    return {"access_token": access_token, "token_type": "bearyer"}
