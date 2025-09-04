from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True
