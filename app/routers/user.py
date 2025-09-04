from app import models, database, utils
from app.schemas.requests import UserRegisterRequest
from app.schemas.responses import UserResponse
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, Depends, APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def store_user(payload: UserRegisterRequest, db: Session = Depends(database.get_db)):
    payload.password = utils.hash_password(payload.password)
    data = payload.model_dump()
    user = models.User(**data)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    db.refresh(user)
    return user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id {id} not found.")
    return user
