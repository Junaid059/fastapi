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
from . import Oauth
from ..schemas import UserOut


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


@router.get("/allUsers",response_model = list[schemas.UserOut])
def getAllUsers(db:Annotated[Session,Depends(get_db)],current_user: models.User = Depends(Oauth.get_current_user)): 
     
    if getattr(current_user, 'role', None) != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to access this resource")

    users = db.query(models.User).all()
    return users


@router.delete("/deleteUser/{id}")
def delete_User(id: int, db: Annotated[Session,Depends(get_db)],current_user: models.User= Depends(Oauth.get_current_user)):
 print("DEBUG: Current user id:", getattr(current_user, 'id', None), "role:", getattr(current_user, 'role', None))
 user = db.query(models.User).filter(models.User.id == id).first()

 if getattr(current_user,'role', None) != "admin":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to perform this action")
 
 db.delete(user)
 db.commit()

 return {"message":f"User with id {id} has been deleted successfully"}
 
        
@router.post("/createAdmin",status_code = status.HTTP_201_CREATED,response_model=schemas.UserOut)
def createAdmin(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):

    hashed_password = hash_password(user.password)
    new_user = models.User(email = user.email,password = hashed_password, role = "Admin")
    db.add(new_user)
    db.commit()

    return new_user   