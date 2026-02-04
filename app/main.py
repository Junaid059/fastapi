from dbm import error
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import posts, users,auth
from . import models
from .database import engine



# class Post(BaseModel):
#    title: str
#    content: str
#    published: bool = True


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", 
#                            password = "NewStrongPassword123", cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Database connection failed!")
#         print("Error:", error)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)