from sqlalchemy import Column,Integer, String
from database import Base 

class NoteModel(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

