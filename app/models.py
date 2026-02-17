
from .database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func, UniqueConstraint
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
    role= Column(String,nullable = False,server_default = "user")
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    

class Votes(Base):
    __tablename__ = "Votes"

    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),primary_key=True)    


class Comment(Base):
    __tablename__ = "Comments"

    id = Column(Integer,primary_key= True,nullable=False,autoincrement=True)
    content = Column(String,nullable = False)
    post_id = Column(Integer,ForeignKey("Posts.id",ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    user = relationship("User", lazy="joined", innerjoin=True)
    post = relationship("Post", lazy="joined", innerjoin=True)


class Follow(Base):
    __tablename__ = "Follows"

    id = Column(Integer, primary_key = True, nullable = False, autoincrement = True)
    follower_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable = False)
    following_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable = False)
    __table_args = (UniqueConstraint("follower_id","following_id", name="unique_follow"),)


class Message(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, server_default='FALSE', nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], lazy="joined")
    receiver = relationship("User", foreign_keys=[receiver_id], lazy="joined")
