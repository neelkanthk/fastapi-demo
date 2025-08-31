from app import models, database
from app.schemas.requests import PostCreateRequest, PostUpdateRequest
from app.schemas.responses import PostResponse
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, Depends, HTTPException, APIRouter

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def index(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).filter(models.Post.published == True).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def store(payload: PostCreateRequest, db: Session = Depends(database.get_db)):
    data = payload.model_dump()
    new_post = models.Post(**data)
    db.add(new_post)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating post.")
    db.refresh(new_post)
    return new_post


@router.get('/{id}', status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(database.get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found.")
    else:
        return {"data": data}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    data = db.query(models.Post).filter(models.Post.id == id)
    if data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    else:
        data.delete()
        db.commit()


@router.put('/{id}', status_code=status.HTTP_200_OK)
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
