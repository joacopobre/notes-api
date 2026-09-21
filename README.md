# Notes API

A FastAPI backend combining traditional CRUD operations with LLM-powered features: streaming chat, persistent conversation memory, and retrieval-augmented generation (RAG) over user notes using semantic search.

## Features

- **CRUD API** for notes (create, read, update, delete) backed by PostgreSQL via SQLAlchemy
- **Streaming chat** with the Claude API (`POST /chat`) — responses stream token-by-token via `StreamingResponse`
- **Persistent conversation memory** — full message history is stored per conversation and replayed on each request, so context carries across separate HTTP calls
- **Tool use / function calling** (`POST /chat-with-tools`) — Claude can autonomously call backend functions to search notes, handling multiple concurrent tool calls in a single turn
- **RAG (Retrieval-Augmented Generation)** — notes are embedded with Voyage AI and stored in PostgreSQL via `pgvector`, enabling semantic search that matches by meaning rather than exact keywords

## Tech Stack

| Purpose | Technology |
|---|---|
| API framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Text generation / reasoning | Anthropic Claude API |
| Embeddings | Voyage AI (`voyage-3.5`) |
| Vector storage & similarity search | pgvector |

## Architecture

Three specialized services, each doing the part it's built for:
- **Voyage AI** generates embeddings (text → 1024-dimension vectors capturing meaning)
- **pgvector** stores those vectors alongside relational data and performs cosine-similarity search directly in Postgres
- **Claude** handles reasoning and text generation, and can request tool calls (keyword search or semantic search) mid-conversation to ground its answers in real data

## API Overview

- `GET /notes`, `POST /notes`, `GET /notes/{id}`, `PUT /notes/{id}`, `DELETE /notes/{id}` — standard CRUD, each note is embedded on creation
- `POST /chat` — streaming chat with persistent memory (`conversation_id` optional; omit to start a new conversation)
- `POST /chat-with-tools` — non-streaming chat where Claude can call `search_notes` (keyword match) or `semantic_search` (embedding similarity) to answer questions grounded in the user's notes

## Setup

1. Create a virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Set up PostgreSQL with the `pgvector` extension:
```
createdb notes_db
psql notes_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```
3. Create a `.env` file:
```
DATABASE_URL=postgresql://<user>@localhost/notes_db
ANTHROPIC_API_KEY=your_key_here
VOYAGE_API_KEY=your_key_here
```

4. Run the server:

```python3 -m uvicorn main:app --reload```

5. Explore the API at `http://127.0.0.1:8000/docs`

## Project Structure

main.py # FastAPI app, routes
models.py # SQLAlchemy models (Note, Conversation, Message)
database.py # DB engine, session management
claude_client.py # Anthropic client setup
voyageai_client.py # Voyage AI client setup
tools.py # Tool functions (search_notes, semantic_search) and embedding helper
backfill_embeddings.py # One-off script to embed pre-existing notes
