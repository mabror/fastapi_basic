from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool
    

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
