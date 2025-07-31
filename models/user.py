from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True
    
    @field_validator('username')
    def validate_username(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: bool
    created_at: datetime
