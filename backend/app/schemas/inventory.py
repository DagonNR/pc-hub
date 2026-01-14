from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class InventoryCategory(str, Enum):
    other = "other"
    cpu = "cpu"
    motherboard = "motherboard"
    ram = "ram"
    gpu = "gpu"
    storage = "storage"
    psu = "psu"
    case = "case"
    cooling = "cooling"
    thermal = "thermal"
    cables_adapters = "cables_adapters"
    peripherals = "peripherals"
    networking = "networking"
    tools = "tools"
    consumables = "consumables"
    replacement_parts = "replacement_parts"

class InventoryCreate(BaseModel):
    name: str
    category: InventoryCategory = InventoryCategory.other
    brand: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    stock: Optional[int] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[InventoryCategory] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    stock: Optional[int] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None


class InventoryOut(BaseModel):
    id: int
    name: Optional[str] = None
    category: Optional[InventoryCategory] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    stock: Optional[int] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True