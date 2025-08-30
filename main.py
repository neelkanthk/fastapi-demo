from fastapi import FastAPI, status, Depends, HTTPException
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


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return JSONResponse(content="Posts API", status_code=status.HTTP_200_OK)


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(database.get_db)):
    return {"status": "success"}


@app.get('/posts', status_code=status.HTTP_200_OK)
def index(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


class NewPostRequest(BaseModel):
    title: str
    content: str
    author: str
    published: Optional[bool] = True


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def save(payload: NewPostRequest, db: Session = Depends(database.get_db)):
    data = payload.model_dump()
    new_post = models.Post(**data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get('/posts/{id}', status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(database.get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found.")
    else:
        return {"data": data}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    data = db.query(models.Post).filter(models.Post.id == id)
    if data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    else:
        data.delete()
        db.commit()


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update(id: int, payload: NewPostRequest, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    else:
        post.update(payload.model_dump())
        db.commit()
        return {"data": post.first()}


def post_exists(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    exists = False if post is None else True
    return exists
