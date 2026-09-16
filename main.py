from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import NoteModel, Conversation, Message
from claude_client import client
from fastapi.responses import StreamingResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)


class Note(BaseModel): 
    title: str
    content: str

class ChatRequest(BaseModel):
    message:str
    conversation_id: int | None = None



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
def chat(request:ChatRequest, db : Session = Depends(get_db)):
    if request.conversation_id is None:
        new_conversation = Conversation()
        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)
        conversation_id = new_conversation.id
    else:
        conversation_id = request.conversation_id

    new_message = Message(role="user", content=request.message, conversation_id = conversation_id)
    db.add(new_message)
    db.commit()

    history = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.id).all()
    message_for_claude = [{'role':msg.role, "content":msg.content} for msg in history]

    def generate():
        with client.messages.stream(
            model='claude-sonnet-5',
            max_tokens=1024,
            messages= message_for_claude
        ) as stream:
            full_response =''
            for text in stream.text_stream:
                full_response += text
                yield text
        new_response = Message(role="assistant", content=full_response, conversation_id = conversation_id)
        db.add(new_response)
        db.commit()
    return StreamingResponse(generate(), media_type='text/plain')
