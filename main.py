from fastapi import FastAPI, status, Depends, HTTPException

from fastapi.responses import JSONResponse
import logging
from app.schemas.requests import PostCreateRequest, PostUpdateRequest, UserRegisterRequest
from app.schemas.responses import PostResponse, UserResponse
import app.models as models
import app.database as database
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# Create DB tables if not exist
models.Base.metadata.create_all(bind=database.engine)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return JSONResponse(content="Posts API", status_code=status.HTTP_200_OK)


@app.get('/posts', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def index(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).filter(models.Post.published == True).all()

    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def store(payload: PostCreateRequest, db: Session = Depends(database.get_db)):
    data = payload.model_dump()
    new_post = models.Post(**data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


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
def update(id: int, payload: PostUpdateRequest, db: Session = Depends(database.get_db)):
    post = db.query(post.Post).filter(post.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    else:
        post.update(payload.model_dump())
        db.commit()
        return {"data": post.first()}


def post_exists(id: int, db: Session = Depends(database.get_db)):
    post = db.query(post.Post).filter(post.Post.id == id).first()
    exists = False if post is None else True
    return exists


@app.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def store_user(payload: UserRegisterRequest, db: Session = Depends(database.get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_context.hash(payload.password)
    payload.password = hashed_pwd
    data = payload.model_dump()
    user = models.User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_class=UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    return user
