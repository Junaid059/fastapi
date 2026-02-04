from fastapi import APIRouter, Depends, HTTPException, status
from ..routers import votes
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
import Oauth

router = APIRouter()

@router.post("/newVotes",status_code=status.HTTP_201_CREATED)
def Vote(vote: schemas.Vote,db: Session = Depends(get_db),current_user: models.User = Depends(votes.Oauth.get_current_user)):
  
  found_vote = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id).first()
  if vote.dir ==1:
    if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
       
    new_vote = models.Votes(post_id = vote.post_id,user_id = current_user.id)
    db.add(new_vote)
    db.commit()

    return {"message":"successfully added vote"}
  
  else:
      if not found_vote:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
      db.delete(found_vote)
      db.commit()
      return {"message":"successfully deleted vote"}