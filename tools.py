
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
} },{
    "name":"semantic_search", "description": "Search the user's saved notes by embeddings, matching by meaning, not exact wording.Good when the user describes something conceptually rather than by its literal title", "input_schema":{
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "what to semantically search"
        }
    },
    "required": ["query"]}
}]

def search_notes(query: str, db: Session):
    matches = db.query(NoteModel).filter(NoteModel.title.contains(query)).all()
    return matches 



def get_embedding(text:str) -> list[float]:
    result = voyage_client.embed(texts=[text], model='voyage-3.5')
    return result.embeddings[0]

def semantic_search(query:str, db: Session):
    query_embedding = get_embedding(query)
    results = db.query(NoteModel).order_by(NoteModel.embedding.cosine_distance(query_embedding)).limit(3).all()
    return results

def get_response_text(response):
    for block in response.content:
        if block.type == "text":
            return block.text
