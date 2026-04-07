from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Book Schemas
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field("want_to_read", pattern="^(want_to_read|reading|completed)$")
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    notes:Optional[str] = Field(None, max_length=1000)
    is_favorite: Optional[bool] = False

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, pattern="^(want_to_read|reading|completed)$")
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    notes:Optional[str] = Field(None, max_length=1000)
    is_favorite: Optional[bool] = False

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str]
    status: str
    rating: Optional[float]
    notes: Optional[str]
    is_favorite: bool
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int

    class Config:
        from_attributes = True