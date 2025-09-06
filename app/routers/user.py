from app import models, database, utils
from app.schemas.responses import UserResponse
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, Depends, APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id {id} not found.")
    return user
