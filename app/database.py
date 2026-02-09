from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os


load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


try:
    with engine.connect() as conn:
        print("Database connection successful (SQLAlchemy)")
except SQLAlchemyError as e:
    print("Database connection failed!")
    print("Error:", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()