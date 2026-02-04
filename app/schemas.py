import datetime
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr 
    
    class Config:
        from_attributes = True 

class Post(PostBase):
    id: int
    owner_id: int
    owner: 'UserOut'
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str
 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str    
    
class TokenData(BaseModel):
    id: int | None = None


    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id:int
    user_id:int
    dir: Annotated[int, Field(le=1)]



