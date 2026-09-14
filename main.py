from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import NoteModel

app = FastAPI()
Base.metadata.create_all(bind=engine)

class Note(BaseModel): 
    title: str
    content: str



@app.get("/notes")
def list_notes(db : Session = Depends(get_db)):
    return db.query(NoteModel).all()

@app.post("/notes")
def create_note(note : Note, db : Session = Depends(get_db)):
    new_note = NoteModel(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes/{note_id}")
def get_note(note_id: int, db : Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if note is None: 
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}")
def change_note(note_id : int, note_data:Note, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_data.title
    note.content = note_data.content
    db.commit()
    return note 

@app.delete("/notes/{note_id}")
def delete_note(note_id:int, db : Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted", "id": note_id}
