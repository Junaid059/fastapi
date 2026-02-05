from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from . import Oauth



router = APIRouter()

@router.post("/createComment",status_code=status.HTTP_201_CREATED,response_model=schemas.CommentOut)
def createComment(comment: schemas.CommentCreate,db: Session = Depends(get_db),current_user: models.User = Depends(Oauth.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {comment.post_id} does not exist")
     
    new_comment = models.Comment(content = comment.content,post_id = comment.post_id, user_id = current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

