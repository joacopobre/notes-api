from dotenv import load_dotenv
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import  declarative_base, sessionmaker



load_dotenv()
database = os.environ.get("DATABASE_URL")
engine = create_engine(database)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    try:
        session = SessionLocal()
        yield session 
    finally:
        session.close()
