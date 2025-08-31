
from passlib.context import CryptContext


def hash_password(pwd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_pwd = pwd_context.hash(pwd)
    return hashed_pwd


def verify_password(plain_pwd, hashed_pwd):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_pwd, hashed_pwd)
