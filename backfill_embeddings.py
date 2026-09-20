

from models import NoteModel
from tools import get_embedding
from database import SessionLocal
import time

db = SessionLocal()

notes = db.query(NoteModel).filter(NoteModel.embedding.is_(None)).all()

for note in notes:
    new_embedding = get_embedding(f"{note.title}\n{note.content}")
    note.embedding = new_embedding
    time.sleep(20)

db.commit()