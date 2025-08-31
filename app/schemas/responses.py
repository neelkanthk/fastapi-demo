from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
