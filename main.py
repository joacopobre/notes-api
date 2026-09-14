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

@app.put("/notes/{note_id}")
def change_note(note_id : int, note:Note):
    for curr_note in notes:
        if curr_note['id'] == note_id:
            curr_note["title"] = note.title
            curr_note["content"] = note.content
            return curr_note

    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}")
def delete_note(note_id:int):
    for note in notes:
        if note['id'] == note_id:
            notes.remove(note)
            return {"message": "Note deleted", "id": note_id}
    raise HTTPException(status_code=404, detail="Note not found")
