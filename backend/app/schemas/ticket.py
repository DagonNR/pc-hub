from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class TicketStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    waiting_parts = "waiting_parts"
    cancelled = "cancelled"
    ready = "ready"
    delivered = "delivered"

class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TicketServiceType(str, Enum):
    repair = "repair"
    maintenance = "maintenance"
    diagnostic = "diagnostic"
    build = "build"
    upgrade = "upgrade"

class TicketCreate(BaseModel):
    device_id: Optional[int]
    title: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.medium
    service_type: TicketServiceType = TicketServiceType.repair
    estimated_cost: Optional[Decimal] = None

class TicketUpdate(BaseModel):
    device_id: Optional[int]
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    service_type: Optional[TicketServiceType] = None
    estimated_cost: Optional[Decimal] = None
    final_cost: Optional[Decimal] = None


class TicketOut(BaseModel):
    id: int
    device_id: Optional[int]
    title: str
    description: Optional[str] = None
    status: TicketStatus
    priority: TicketPriority
    service_type: TicketServiceType
    estimated_cost: Optional[Decimal] = None
    final_cost: Optional[Decimal] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True