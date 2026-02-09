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
    role: str
    
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
    role: str | None = None


    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(le=1)]

    class config:
        from_attributes = True


class CommentBase(BaseModel):
    content:str
    post_id:int

class CommentCreate(CommentBase):
    pass 

class CommentOut(CommentBase):
    id: int
    user_id:int 
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class FollowBase(BaseModel):
    following_id: int

class FollowOut(BaseModel):
    id: int
    follower_id: int
    following_id: int

    class Config:
        from_attributes = True
