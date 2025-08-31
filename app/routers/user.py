from app import models, database
from app.schemas.requests import UserRegisterRequest
from app.schemas.responses import UserResponse
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, Depends, APIRouter, HTTPException
from passlib.context import CryptContext

router = APIRouter()


@router.post('/users/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def store_user(payload: UserRegisterRequest, db: Session = Depends(database.get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_context.hash(payload.password)
    payload.password = hashed_pwd
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


@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_class=UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    return user
