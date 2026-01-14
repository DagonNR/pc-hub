
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserRole(str, Enum):
    admin = "admin"
    tech = "tech"
    client = "client"

class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[UserRole] = UserRole.client

class UserOut(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True