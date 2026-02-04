from dbm import error
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
import psycopg2
from pydantic import BaseModel
from typing import Optional, Annotated
from psycopg2.extras import RealDictCursor
from fastapi import Depends

from app.routers import Oauth
from .. import models, schemas
from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session, joinedload
import app

router = APIRouter()

@router.get("/allPosts")
def getAll(db: Session = Depends(get_db), current_user: models.User = Depends(Oauth.get_current_user),limit: int = 10,skip: int = 0):
    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()
    # return {"data": posts}
    posts = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    return posts
   

@router.post("/createPost", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def createPost(post: schemas.PostCreate, db: Annotated[Session, Depends(get_db)], current_user: models.User = Depends(Oauth.get_current_user)):
   new_post = models.Post(
       title=post.title,
       content=post.content, 
       published=post.published,
       owner_id=current_user.id
   )
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post

  

@router.get("/getPost/{id}", response_model=schemas.Post)
def getPost(id: int, db: Annotated[Session, Depends(get_db)], current_user: models.User = Depends(Oauth.get_current_user)):
    post = db.query(models.Post).options(joinedload(models.Post.owner)).filter(
        models.Post.id == id,
        models.Post.owner_id == current_user.id
    ).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found or you don't have permission")
    
    return post


@router.delete("/deletePost/{id}")
def deletePost(id: int, db: Annotated[Session, Depends(get_db)], current_user: models.User = Depends(Oauth.get_current_user)):
    post = db.query(models.Post).filter(
        models.Post.id == id, 
        models.Post.owner_id == current_user.id
    ).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist or you don't have permission")
    
    db.delete(post)
    db.commit()
    
    return {"message": f"Post with id {id} was deleted successfully"}


@router.put("/updatePost/{id}", response_model=schemas.Post)
def updatePost(id: int, post: schemas.PostCreate, db: Annotated[Session, Depends(get_db)], current_user: models.User = Depends(Oauth.get_current_user)):
    post_query = db.query(models.Post).filter(
        models.Post.id == id,
        models.Post.owner_id == current_user.id
    )
    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist or you don't have permission")
    
    post_query.update({"title": post.title, "content": post.content, "published": post.published}, synchronize_session=False)
    db.commit()
    
    return post_query.first()