from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class InventoryMovementMovementType(str, Enum):
    inside = "inside"
    out = "out"
    adjustment = "adjustment"

class InventoryMovementReason(str, Enum):
    purchase = "purchase"
    sell = "sell"
    used_in_ticket = "used_in_ticket"
    returned = "returned"
    damaged = "damaged"
    correction = "correction"
    other = "other"

class InventoryMovementAdjustmentDirection(str, Enum):
    increase = "increase"
    decrease = "decrease"

class InventoryMovementCreate(BaseModel):
    inventory_id: Optional[int] = None
    ticket_id: Optional[int] = None
    movement_type: InventoryMovementMovementType = InventoryMovementMovementType.inside
    adjustment_direction: InventoryMovementAdjustmentDirection = InventoryMovementAdjustmentDirection.increase
    quantity: int
    reason: InventoryMovementReason = InventoryMovementReason.purchase
    description: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None

class InventoryMovementOut(BaseModel):
    id: int
    inventory_id: Optional[int] = None
    ticket_id: Optional[int] = None
    movement_type: InventoryMovementMovementType = InventoryMovementMovementType.inside
    adjustment_direction: InventoryMovementMovementType = InventoryMovementMovementType.inside
    quantity: int
    reason: InventoryMovementReason = InventoryMovementReason.purchase
    description: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    created_at: datetime

    class Config:
        from_attributes = True