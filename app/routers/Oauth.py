import dotenv
from jose import JWTError, jwt
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from ..schemas import TokenData
from .. import schemas,database,models
from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable is not set")
if ALGORITHM is None:
    raise ValueError("ALGORITHM environment variable is not set")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    assert SECRET_KEY is not None and ALGORITHM is not None
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    try:
        assert SECRET_KEY is not None and ALGORITHM is not None
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception 
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session  = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user