from dbm import error
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
import psycopg2
from pydantic import BaseModel
from typing import Optional, Annotated
from psycopg2.extras import RealDictCursor
from .. import models, schemas
from ..database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from ..utils import hash_password


router = APIRouter()

@router.post("/createUser",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate, db:Annotated[Session, Depends(get_db)]):
    hashed_password = hash_password(user.password)
    new_user = models.User(email = user.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/getUser/{id}",response_model=schemas.UserOut)
def getUser(id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    
    return user
