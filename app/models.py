import datetime
from .database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key = True,nullable = False,autoincrement=True)
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean, server_default='TRUE', nullable = False)
    owner_id = Column(Integer,ForeignKey("Users.id",ondelete = "CASCADE"),nullable=False)
    
    owner = relationship("User", lazy="joined", innerjoin=True)

class User(Base):
    __tablename__= "Users"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now()
)
    

class Votes(Base):
    __tablename__ = "Votes"

    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)    