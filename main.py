from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel): 
    title: str
    content: str

notes = []
next_id = 1

@app.get("/notes")
def list_notes():
    return notes

@app.post("/notes")
def create_note(note : Note):
    global next_id
    new_note = {"id":next_id , "title":note.title, "content":note.content}
    notes.append(new_note)
    next_id += 1
    return new_note

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note['id'] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")