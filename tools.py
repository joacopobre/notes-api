
from sqlalchemy.orm import Session

from models import NoteModel

from voyageai_client import voyage_client

tools = [{"name":"search_notes", "description":"Search the user's saved notes by keyword, matching against note titles. Use this when the user asks about something they may have written down before.", "input_schema":{
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "what to search for in note titles"
        }
    },
    "required": ["query"]
} }]

def search_notes(query: str, db: Session):
    matches = db.query(NoteModel).filter(NoteModel.title.contains(query)).all()
    return matches 



def get_embedding(text:str) -> list[float]:
    result = voyage_client.embed(texts=[text], model='voyage-3.5')
    return result.embeddings[0]
