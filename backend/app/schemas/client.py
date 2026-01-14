from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ClientCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    rfc: str
    email: str
    phone_number: Optional[str] = None
    street_adress: str
    interior_number: Optional[str] = None
    outer_number: str
    postal_code: str
    city: str
    state: str

class ClientUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    rfc: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    street_adress: Optional[str] = None
    interior_number: Optional[str] = None
    outer_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class ClientOut(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    rfc: str
    email: str
    phone_number: str
    street_adress: str
    interior_number: Optional[str] = None
    outer_number: str
    postal_code: str
    city: str
    state: str
    created_at: datetime
    update_at: Optional[datetime] = None

class Config:
    from_attributes = True