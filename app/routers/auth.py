from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.auth import Token
from app import models, database, utils
from sqlalchemy.orm import Session
import app.utils as utils
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/login')
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == creds.username).first()
    if not user or not utils.verify_password(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect login credentials", headers={"WWW-Authenticate": "Bearer"})
    else:
        encoded_jwt = utils.create_access_token(data={"user_id": str(user.id)})
        return Token(access_token=encoded_jwt, token_type="bearer")
