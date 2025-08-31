from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.auth import LoginRequest, Token, TokenData
from app import models, database, utils
from sqlalchemy.orm import Session
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/login')
def login(creds: LoginRequest, db: Session = Depends(database.get_db)):
    email = creds.email
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not utils.verify_password(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect login credentials", headers={"WWW-Authenticate": "Bearer"})
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        if access_token_expires:
            expire = datetime.now(timezone.utc) + access_token_expires
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        data_to_encode = {
            "exp": expire,
            "sub": {"user_id": user.id}
        }

        encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")
