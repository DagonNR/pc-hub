from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.device import DeviceOut, DeviceCreate, DeviceUpdate
from app.schemas.user import UserRole
from sqlalchemy.orm import Session
from app.core.deps import get_database, require_roles
from app.models.device import Device
from typing import List

router = APIRouter(prefix="/devices", tags=["devices"], dependencies=[Depends(require_roles(UserRole.admin, UserRole.tech))])

@router.get("/", response_model=List[DeviceOut])
def list_devices(db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin, UserRole.tech))):
    devices = db.query(Device).order_by(Device.created_at.desc()).all()
    return devices

@router.get("/{devices_id}", response_model=DeviceOut)
def get_device(device_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin, UserRole.tech))):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code= 404, detail= "Dispositivo no encontrado")
    return device

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin, UserRole.tech))):
    device = Device(
        device_type = payload.device_type.value,
        brand = payload.brand,
        model = payload.model,
        notes = payload.notes
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.patch("/{devices_id}", response_model=DeviceOut)
def update_device(payload: DeviceUpdate, device_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin))):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code= 404, detail= "Dispositivo no encontrado")
    
    data = payload.model_dump(exclude_unset=True)

    if "device_type" in data and data["device_type"] is not None:
        data["device_type"] = data["device_type"].value
    
    for key, value in data.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin))):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code= 404, detail= "Dispositivo no encontrado")
    
    db.delete(device)
    db.commit()
    return None