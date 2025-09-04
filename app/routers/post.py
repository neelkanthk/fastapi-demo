from app import models, database
from app.schemas.requests import PostCreateRequest, PostUpdateRequest, VoteRequest
from app.schemas.responses import PostResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, Depends, HTTPException, APIRouter
import app.utils as utils
from datetime import datetime, timezone

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
def index(db: Session = Depends(database.get_db), published: bool = True, limit: int = 10):
    posts = db.query(models.Post).filter(models.Post.published == published).limit(limit).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def store(payload: PostCreateRequest, db: Session = Depends(database.get_db), logged_in_user=Depends(utils.get_current_user)):
    data = payload.model_dump()
    new_post = models.Post(**data)
    new_post.user_id = int(logged_in_user.id)  # Associate post with the user from token
    db.add(new_post)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating post.")
    db.refresh(new_post)
    return new_post


@router.get('/search', response_model=List[PostResponse], status_code=status.HTTP_200_OK)
def search(db: Session = Depends(database.get_db), keyword: Optional[str] = ""):
    query = db.query(models.Post).filter(models.Post.title.contains(
        keyword)).filter(models.Post.published == True)

    print(query)
    return query.all()


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def show(id: int, db: Session = Depends(database.get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found.")
    else:
        return data


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db), logged_in_user=Depends(utils.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    if post.user_id != int(logged_in_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post.")
    else:
        query.delete()
        db.commit()


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def update(id: int, payload: PostUpdateRequest, db: Session = Depends(database.get_db), logged_in_user=Depends(utils.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found.")
    if post.user_id != int(logged_in_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post.")
    else:
        data = payload.model_dump()
        data['updated_at'] = datetime.now(timezone.utc)
        query.update(data)
        db.commit()
        return query.first()


def post_exists(id: int, db: Session = Depends(database.get_db)):
    post = db.query(post.Post).filter(post.Post.id == id).first()
    exists = False if post is None else True
    return exists
