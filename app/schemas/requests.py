from pydantic import BaseModel, EmailStr
from typing import Optional


class PostCreateRequest(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostUpdateRequest (BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class VoteRequest(BaseModel):
    post_id: int
    direction: int
