from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from app.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer
from app import models, database
from sqlalchemy.orm import Session


def hash_password(pwd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_context.hash(pwd)
    return hashed_pwd


def verify_password(plain_pwd, hashed_pwd):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_pwd, hashed_pwd)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Utility function to create JWT token
# data: dict should contain user identification data, e.g., {"user_id": user.id}
def create_access_token(data: dict):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    data_to_encode = {
        "exp": expire,
        "sub": data["user_id"]
    }
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Utility function to decode and verify JWT token
# Raises credentials_exception if token is invalid
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid credentials1",
                                headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials2",
                            headers={"WWW-Authenticate": "Bearer"})
    return token_data


# Dependency to get current user based on JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    user_id = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == int(user_id.user_id)).first()
    return user
