from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from .Oauth import get_current_user
from ..database import get_db

router = APIRouter()

@router.post("/follow/{user_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.FollowOut)
def followUser(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")
    user_to_follow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist")
    existing_follow = db.query(models.Follow).filter(models.Follow.follower_id == current_user.id, models.Follow.following_id == user_id).first()
    if existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You are already following user with id {user_id}")
    new_follow = models.Follow(follower_id=current_user.id, following_id=user_id)
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow

@router.delete("/unfollow/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.FollowOut)
def unfollowUser(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot unfollow yourself")
    user_to_unfollow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist")
    existing_follow = db.query(models.Follow).filter(models.Follow.follower_id == current_user.id, models.Follow.following_id == user_id).first()
    if not existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You are not following user with id {user_id}")
    db.delete(existing_follow)
    db.commit()
    return existing_follow

@router.get("/followers/{user_id}", response_model=List[schemas.FollowOut])
def getFollowers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(models.Follow).filter(models.Follow.following_id == user_id).all()
    return followers

@router.get("/following/{user_id}", response_model=List[schemas.FollowOut])
def getFollowing(user_id: int, db: Session = Depends(get_db)):
    following = db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()
    return following