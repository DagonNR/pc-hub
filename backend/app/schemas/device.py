from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class DeviceDeviceType(str, Enum):
    laptop = "laptop"
    pc = "pc"
    all_in_one = "all_in_one"
    other = "other"

class DeviceCreateAndUpdate(BaseModel):
    #client_id: Optional[int]
    device_type: DeviceDeviceType = DeviceDeviceType.other
    brand: str
    model: str
    notes: Optional[str] = None

# Como para crear y modificar tenemos los mismos valores, no necesitamos actualmente las dos class
"""class DeviceUpdate(BaseModel):
    device_type: DeviceDeviceType = DeviceDeviceType.other
    brand: str
    model: str
    notes: Optional[str] = None"""

class DeviceOut(BaseModel):
    id: int
    #client_id: Optional[int]
    device_type: DeviceDeviceType = DeviceDeviceType.other
    brand: str
    model: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True