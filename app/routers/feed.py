from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .Oauth import get_current_user
import random

router = APIRouter()


@router.get("/feed",response_model=list[schemas.PostResponse])
def get_feed(db: Session= Depends(get_db),current_user = Depends(get_current_user)):
    ## get ids of users that the current user is following

    following_id = db.query(models.Follow.following_id).filter(models.Follow.follower_id == current_user.id).all()
    following_id = [id[0] for id in following_id]
    ## get posts of users that the current user is following    
    posts_from_following = db.query(models.Post).filter(models.Post.owner_id.in_(following_id)).all()
    ## Random Posts to fill the feed
    all_post_ids = db.query(models.Post.id).all()
    all_post_ids = [pid[0] for pid in all_post_ids]
    random_ids = random.sample(all_post_ids, min(10, len(all_post_ids)))
    random_posts = db.query(models.Post).filter(models.Post.id.in_(random_ids)).all()

    # Combine and remove duplicates
    feed_posts = posts_from_following + random_posts
    unique_feed = {post.id: post for post in feed_posts}.values()

    return list(unique_feed)