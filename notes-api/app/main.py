import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Response
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field


# salasana tulee docker secretistä
def get_password():
    path = os.environ.get("DB_PASSWORD_FILE")
    if path:
        with open(path) as f:
            return f.read().strip()
    return os.environ.get("DB_PASSWORD", "")


DB_URL = (
    f"host={os.environ.get('DB_HOST', 'db')} "
    f"port={os.environ.get('DB_PORT', '5432')} "
    f"dbname={os.environ.get('DB_NAME', 'notes')} "
    f"user={os.environ.get('DB_USER', 'notes')} "
    f"password={get_password()}"
)

pool = None


@asynccontextmanager
async def lifespan(app):
    global pool
    pool = ConnectionPool(DB_URL, min_size=1, max_size=5, kwargs={"row_factory": dict_row})
    pool.wait(timeout=30)
    yield
    pool.close()


app = FastAPI(title="Notes API", root_path="/api", lifespan=lifespan)


class NoteIn(BaseModel):
    author: str = Field(min_length=1, max_length=50)
    topic: str = Field(default="yleinen", min_length=1, max_length=50)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(default="", max_length=10000)


class Note(NoteIn):
    id: int
    created_at: datetime
    updated_at: datetime


@app.get("/health")
def health():
    with pool.connection() as conn:
        conn.execute("SELECT 1")
    # hostname näyttää mikä kontti vastas (skaalauksen testaus)
    return {"status": "ok", "hostname": os.environ.get("HOSTNAME")}


@app.get("/notes", response_model=list[Note])
def get_notes(author: str = None, topic: str = None):
    sql = "SELECT * FROM notes WHERE TRUE"
    params = []
    if author:
        sql += " AND author = %s"
        params.append(author)
    if topic:
        sql += " AND topic = %s"
        params.append(topic)
    sql += " ORDER BY updated_at DESC LIMIT 500"
    with pool.connection() as conn:
        return conn.execute(sql, params).fetchall()


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    with pool.connection() as conn:
        note = conn.execute("SELECT * FROM notes WHERE id = %s", (note_id,)).fetchone()
    if not note:
        raise HTTPException(404, "ei löydy")
    return note


@app.post("/notes", response_model=Note, status_code=201)
def add_note(note: NoteIn):
    with pool.connection() as conn:
        return conn.execute(
            "INSERT INTO notes (author, topic, title, body) VALUES (%s, %s, %s, %s) RETURNING *",
            (note.author, note.topic, note.title, note.body),
        ).fetchone()


@app.put("/notes/{note_id}", response_model=Note)
def edit_note(note_id: int, note: NoteIn):
    with pool.connection() as conn:
        row = conn.execute(
            "UPDATE notes SET author=%s, topic=%s, title=%s, body=%s, updated_at=now() WHERE id=%s RETURNING *",
            (note.author, note.topic, note.title, note.body, note_id),
        ).fetchone()
    if not row:
        raise HTTPException(404, "ei löydy")
    return row


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with pool.connection() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    if cur.rowcount == 0:
        raise HTTPException(404, "ei löydy")
    return Response(status_code=204)


# etusivun luvut
@app.get("/stats")
def stats():
    with pool.connection() as conn:
        return conn.execute(
            "SELECT count(*) AS notes, count(DISTINCT author) AS authors, count(DISTINCT topic) AS topics FROM notes"
        ).fetchone()
