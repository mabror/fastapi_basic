from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from .routers import post, users, auth, vote






# models.Base.metadata.create_all(bind=engine) sql aclhemmy create databse without alembic


app = FastAPI()

# site to send api
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world"}