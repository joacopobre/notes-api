from sqlalchemy import Column,Integer, String, ForeignKey
from database import Base 

class NoteModel(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer,primary_key=True)
    role = Column(String)
    content = Column(String)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
