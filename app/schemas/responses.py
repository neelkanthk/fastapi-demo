from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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
    vote_count: Optional[int] = 0

    class Config:
        from_attributes = True
