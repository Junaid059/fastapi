from dbm import error
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import posts, users, auth, votes, comments, follow, feed, search, chat
from . import models
from .database import engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comments.router)
app.include_router(follow.router)
app.include_router(feed.router)
app.include_router(search.router)
app.include_router(chat.router)