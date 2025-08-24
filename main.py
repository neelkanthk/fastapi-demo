from fastapi import FastAPI, status, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from typing import Optional
import models
import database
from sqlalchemy.orm import Session

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# Create DB tables if not exist
models.Base.metadata.create_all(bind=database.engine)

try:
    dbconn = psycopg2.connect(host="localhost", database="db_fastapi", user="postgres",
                              password="postgres", cursor_factory=RealDictCursor)
    cursor = dbconn.cursor()
    logger.info("Database connection successful.")

except Exception as e:
    logger.error("Connecting to database failed.")


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return JSONResponse(content="Posts API", status_code=status.HTTP_200_OK)


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(database.get_db)):
    return {"status": "success"}


@app.get('/posts', status_code=status.HTTP_200_OK)
def index():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


class NewPostRequest(BaseModel):
    title: str
    content: str
    author: str
    published: Optional[bool] = True


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def save(payload: NewPostRequest):
    cursor.execute("""
        INSERT INTO posts (title, content, author, published) VALUES (%s, %s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.author, payload.published))
    new_post = cursor.fetchone()
    dbconn.commit()
    return {"data": new_post}


@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
def show(id: int):
    query = """ SELECT * FROM posts WHERE id = %s """
    cursor.execute(query, (id,))
    post = cursor.fetchone()
    return {"data": post}


@app.delete('/posts/{id}')
def delete(id: int):
    if post_exists(id):
        query = """ DELETE FROM posts WHERE id = %s """
        cursor.execute(query, (id,))
        dbconn.commit()
        return {"data": f"Post {id} has been deleted."}
    else:
        return JSONResponse(content=f"Post {id} not found.", status_code=status.HTTP_404_NOT_FOUND)


@app.put('/posts/{id}')
def update(id: int, payload: NewPostRequest):
    if post_exists:
        cursor.execute(""" UPDATE posts SET title = %s, content = %s, author = %s, published = %s, updated_at = NOW() WHERE id = %s RETURNING *""",
                       (payload.title, payload.content, payload.author, payload.published, id,))
        updated_post = cursor.fetchone()
        dbconn.commit()
        return {"data": updated_post}
    else:
        return JSONResponse(content=f"Post {id} not found.", status_code=status.HTTP_404_NOT_FOUND)


def post_exists(id: int):
    query = """ SELECT COUNT(*) FROM posts where id = %s"""
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    return True if result['count'] == 1 else False
