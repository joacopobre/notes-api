from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel 
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import NoteModel
from claude_client import client
from fastapi.responses import StreamingResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)


class Note(BaseModel): 
    title: str
    content: str

class ChatRequest(BaseModel):
    message:str



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


# anthropic endpoint
@app.post('/chat')
def chat(request:ChatRequest):
    def generate():
        with client.messages.stream(
            model='claude-sonnet-5',
            max_tokens=1024,
            messages=[{'role':"user", 'content':request.message}]
        ) as stream:
            for text in stream.text_stream:
                yield text
    return StreamingResponse(generate(), media_type='text/plain')
