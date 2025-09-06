from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.auth import Token
from app import models, database, utils
from sqlalchemy.orm import Session
import app.utils as utils
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.requests import UserRegisterRequest
from app.schemas.responses import UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def store_user(payload: UserRegisterRequest, db: Session = Depends(database.get_db)):
    payload.password = utils.hash_password(payload.password)
    data = payload.model_dump()
    user = models.User(**data)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        print(str(e))
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    db.refresh(user)
    return user


@router.post('/login')
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == creds.username).first()
    if not user or not utils.verify_password(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect login credentials", headers={"WWW-Authenticate": "Bearer"})
    else:
        encoded_jwt = utils.create_access_token(data={"user_id": str(user.id)})
        return Token(access_token=encoded_jwt, token_type="bearer")
