from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .Oauth import get_current_user
from typing import List

router = APIRouter()

@router.get("/searchUser",response_model=List[schemas.UserOut])
def search_user(query: str, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.email.ilike(f"%{query}%")).all()

    return users

@router.get("searchPost",response_model=List[schemas.PostResponse])
def searchPost(query: str, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{query}%") | models.Post.content.ilike(f"%{query}%")).all()

    return posts
