from fastapi import FastAPI, APIRouter,Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..routers import Oauth
from app import schemas
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags =['Authentication'])

@router.post("/login")
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    
    ## create a token and return
    access_token = Oauth.create_access_token(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}