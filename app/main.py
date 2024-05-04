from pathlib import Path
from typing import Annotated
import sqlite3

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from jinja2_fragments.fastapi import Jinja2Blocks


ROOT = Path.cwd()
TEMPLATE_PATH = ROOT / 'templates'
STATIC_DIR = ROOT / 'public' / 'static'
DB_PATH = ROOT / 'todox.sqlite3'


app = FastAPI()
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
templates = Jinja2Blocks(directory=TEMPLATE_PATH)


class Todo(BaseModel):
    id: int
    value: str
    completed: bool = False


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.autocommit = False
    conn.row_factory = sqlite3.Row
    return conn


def _create_todo(value: str) -> Todo:
    conn = get_conn()
    c = conn.cursor()
    stmt = """
        INSERT INTO todo (value, completed) VALUES (?, 0)
    """
    c.execute(stmt, (value,))
    try:
        conn.commit()
        return Todo(id=c.lastrowid, value=value, completed=False)
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


def _get_todos() -> list[Todo]:
    conn = get_conn()
    c = conn.cursor()
    stmt = """
        SELECT * FROM todo
    """
    results = c.execute(stmt).fetchall()
    conn.close()
    return [Todo(**dict(r)) for r in results]


def _toggle_todo(todo_id: int) -> Todo:
    conn = get_conn()
    stmt = """
        UPDATE todo
        SET completed = CASE WHEN completed = 0 THEN 1 ELSE 0 END
        WHERE id = ?
    """
    conn.cursor().execute(stmt, (todo_id,))
    try:
        conn.commit()
        select_stmt = """
            SELECT * FROM todo WHERE id = ?
        """
        todo = conn.cursor().execute(select_stmt, (todo_id,)).fetchone()
        return Todo(**dict(todo))
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


def _delete_todo(todo_id: int) -> None:
    conn = get_conn()
    statement = """
        DELETE FROM todo WHERE id = ?;
    """
    try:
        conn.cursor().execute(statement, (todo_id,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    todos = _get_todos()
    return templates.TemplateResponse(
        "index.html.jinja",
        {"todos": todos, "request": request}
    )


@app.post("/todos/create")
async def create_todo(request: Request, value: Annotated[str, Form(min_length=1)]):
    todo = _create_todo(value)
    return templates.TemplateResponse(
        "index.html.jinja",
        {"todo": todo, "request": request},
        block_name="todo_item"
    )


@app.get("/todos/{todo_id}/toggle")
async def toggle_todo(request: Request, todo_id: int):
    todo = _toggle_todo(todo_id)
    return templates.TemplateResponse(
        "index.html.jinja",
        {"request": request, "todo": todo},
        block_name="todo_item"
    )


@app.delete("/todos/{todo_id}")
async def delete_todo(request: Request, todo_id: int):
    _delete_todo(todo_id)
    return Response(status_code=200)
